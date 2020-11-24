# helper utils
from fabric.api import env, local, run, put, get
from fabric.colors import green,blue
import requests
import os, tempfile, uuid

BLOCK_SIZE = 8192

def dl(url,filename):
    """download a url from the net and saves it as filename.
    
    Data is streamed so large files can be saved without exhausting memory
    """
    r=requests.get(url)
    assert r.status_code==200
    
    with open(filename,'wb') as fh:
        for data in r.iter_content(BLOCK_SIZE):
            fh.write(data)

def rsync(sources,dest,rsync_ignore=None,color_files=True):
    if type(sources)==str:
        sources = [sources]
    run('mkdir -p "%s"'%dest)

    command = []
    command.append('rsync')
    command.append('-av')

    custom_port = int(env.port) if env.port is not None and env.port != '22' else None
    if env.key_filename is not None or custom_port is not None or env.disable_known_hosts:
        ssh_arguments = []

        # use specified port if it is a non-standard port
        if custom_port is not None:
            ssh_arguments.append("-p {0.port}".format(env))

        if env.disable_known_hosts:
            ssh_arguments.append("-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no")

        # use specified identity file to connect
        keyfiles = []
        if type(env.key_filename) in (str, unicode): 
            keyfiles = [env.key_filename]
        elif env.key_filename:
            assert type(env.key_filename) in (list, tuple), "malformed env.key_filename: %r"%(env.key_filename)
            keyfiles = env.key_filename
        if keyfiles:
            ssh_arguments.append("-l {0}".format(env.user))
            ssh_arguments += ['-i "{0}"'.format(keyfile) for keyfile in keyfiles]

        ssh_command = "'ssh {0}'".format(" ".join(ssh_arguments))
        command.extend(['-e',ssh_command])

    command.extend("'%s'"%s for s in sources)
    command.append("'%s@%s:%s'"%(env.user,env.host,dest))
                
    if rsync_ignore:
        if os.path.isfile(rsync_ignore):
            command.append('--exclude-from=%s'%rsync_ignore)
    
    if not color_files:   
        return local(" ".join(command))
        
    data = local(" ".join(command),capture=True)
    lines = data.splitlines()
    lines = lines[1:]
    i=0
    while lines[i]:
        print blue(lines[i])
        i+=1
    for line in lines[i:]:
        print line     
    
def write_contents_to_remote(data,filename):
    """creates a file on remote 'filename' that has contents 'data'
    """
    # write a teporary file
    fd,name = tempfile.mkstemp()
    with open(name,'w') as fh:
        fh.write(data)
        
    # copy it
    try:
        run('mkdir -p "%s"'%os.path.dirname(filename))
        put(name,filename)
    finally:
        os.unlink(name)
    
def read_contents_from_remote(remote):
    """returns the data in the remote file. WARNING: reads into ram. only small control files"""
    # copy back to temporary file
    fd,name = tempfile.mkstemp()
    os.unlink(name)
    get(remote,name)
    
    with open(name,'r') as fh:
        data = fh.read()
        
    os.unlink(name)
    return data

def quiet_run(command):
    """Issues a run with the command but pipes the output to a temp file
    then reads the tempfile back here to be presented as data
    """
    remote_temp = "/tmp/%s.tmp"%uuid.uuid4()
    
    run(command+" 1> '%s'"%remote_temp)
    
    data = read_contents_from_remote(remote_temp)
    
    run('rm -f "%s"'%remote_temp)
    
    return data
    
    
    
