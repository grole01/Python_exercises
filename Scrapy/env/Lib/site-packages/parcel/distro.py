import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, sudo, with_settings
from fabric.contrib.files import append
from fabric.colors import green

from . import versions
from .cache import cache
from .tools import rsync
from .defaults import debian as debian_defaults
from .defaults import centos as centos_defaults

#
# Used to represent the remote build distribution
#

class Distro(object):
    """The base class for Distro classes. If use_sudo is true, then super user commands
    will be run using fabric's sudo call. If sudo is false, super user access is gained by
    getting fabric to connect as root user."""

    space = '.parcel-build-temp'
    pip_download_cache = '/tmp/pip-download-cache/'

    def __init__(self, use_sudo=False):
        """Construct a Distro instance. If use_sudo is true, then super user commands
        will be run using fabric's sudo call. If sudo is false, super user access is gained by
        getting fabric to connect as root user."""
        self.use_sudo = use_sudo

    def mkdir(self, remote):
        """Make a directory on the remote"""
        return run('mkdir -p "%s" && cd "%s" && pwd'%(remote,remote))

    def su(self, *args, **kwargs):
        """Method to perform a remote task as a super user. Takes same arguments as fabric.api.run        or fabric.api.sudo. Can be overridden to provide your own super user execution hook."""
        if self.use_sudo:
            return sudo(*args, **kwargs)

        with settings(user='root'):
            return run(*args, **kwargs)

    def update_packages(self):
        """This method should update the packages on the remote box.
        """
        raise NotImplementedError

    def build_deps(self, deps):
        """This method should install the build dependencies on the remote box.
        """
        raise NotImplementedError

    def version(self,package):
        """Look at the distro's packaging system for the package and return a version"""
        raise NotImplementedError
	
    def push_files(self,pathlist,dst):
        """Push all the files in pathlist into dst directory on remote."""
        for path in pathlist:
            put(path, os.path.join(dst,os.path.basename(path)))
    	
    def check(self):
        """Check the remote build host to see if the relevant software to build packages is installed"""
        raise NotImplementedError
    
    def setup(self):
        """This method should set up a remote box for parcel package building.
        It should install fpm.
        """
        raise NotImplementedError

    def install_package(self, pkg):
        """Installs package on the host using apt-get install bypassing
        authentication. This method should be used for testing package
        installation before using push_to_repo."""
        raise NotImplementedError

    def _cleanup(self):
        run("rm -rf '%s'"%self.space)  

    def _setup(self, clean=True):
        # first cleanup any broken stale previous builds
        if clean:
            self._cleanup()

        # make fresh directories
        base_dir = self.mkdir(self.space)
        src_dir = self.mkdir(self.space+"/src")
        build_dir = self.mkdir(self.space+"/build")
        return base_dir, src_dir, build_dir


class Debian(Distro):
    def __init__(self, *args, **kwargs):
        self.defaults = debian_defaults
        Distro.__init__(self,*args,**kwargs)

    def update_packages(self):
        self.su("apt-get update -qq")

    def build_deps(self, deps):
        self.su("apt-get install -qq %s"%(' '.join(deps)))

    def version(self,package):
        """Look at the debian apt package system for a package with this name and return its version.
        Return None if there is no such package.
        """
        with settings(warn_only=True):
            vstring = run('apt-cache show %s 2>/dev/null | sed -nr "s/^Version: ([0-9]+)(-.+)?/\\1/p"'%(package))
            if vstring.return_code:
                # error fetching package info. Assume there is no such named package. Return None
                return None
            return versions.Version(vstring)

    def check(self):
        """Check the remote build host to see if the relevant software to build packages is installed"""
        with settings(warn_only=True):
            # check for fpm
            result = run('which fpm')
            if result.return_code:
                raise Exception("Build host does not have fpm installed and on the executable path")
            
            # check for checkinstall
            result = run('which checkinstall')
            if result.return_code:
                raise Exception("Build host does not have checkinstall installed and on the executable path")

    def setup(self):
        """this method sets up a remote debian box for parcel package building.
        Installs fpm, easyinstall and some libraries.
        """
        self.build_deps(['libyaml-ruby','libzlib-ruby','ruby','ruby-dev','checkinstall'])
            
        base_dir, src_dir, build_dir = self._setup()

        # get rubygems and copy it across
        path = cache.get("http://production.cf.rubygems.org/rubygems/rubygems-1.8.24.tgz")
        self.push_files([path],src_dir)
        filename = os.path.basename(path)

        with cd(build_dir):
            run("tar xvfz ../src/%s"%filename)
            with cd("rubygems-1.8.24"):
                run("ruby setup.rb")
        run("gem1.8 install fpm")

    def install_package(self, pkg):
        """Installs package on the host using apt-get install bypassing
        authentication. This method should be used for testing package
        installation before using push_to_repo."""
        base_dir, src_dir, build_dir = debian._setup(clean=False)
        pkg_dir = self.mkdir(base_dir+"/pkg_dir")
        rsync(pkg,pkg_dir)
        with cd(pkg_dir):
            print green(append("/etc/apt/sources.list", "deb file://{0} /".format(pkg_dir))) 
            print green(run("dpkg-scanpackages . /dev/null | gzip -c -9 > Packages.gz"))
            pkg_name = run("dpkg -f {0} | grep '^Package: ' | sed -e 's/Package: //'".format(pkg))
            pkg_version = run("dpkg -f {0} | grep '^Version: ' | sed -e 's/Version: //'".format(pkg))
            print green(run("apt-get update -qq"))
            print green(run("apt-get install {0}={1} -qq --allow-unauthenticated".format(pkg_name,pkg_version)))


    def build_package(self, deployment=None):
        """
        Runs architecture specific packaging tasks
        """
        assert deployment
        
        with cd(deployment.root_path):
            rv = run(
                'fpm -s dir -t deb -n {0.pkg_name} -v {0.version} '
                '-a all -x "*.git" -x "*.bak" -x "*.orig" {0.hooks_str} '
                '--description "Automated build. '
                'No Version Control." '
                '{0.deps_str} {0.dirs_str}'
                .format(deployment)
            )

            filename = rv.split('"')[-2]
            get(filename, './')
            run("rm '%s'"%filename)
            print green(os.path.basename(filename))


class Ubuntu(Debian):

    def setup(self):
        """this method sets up a remote ubuntu box for parcel package building.
        Installs fpm and also rubygems if not present.
        """
        self.build_deps(['rubygems', 'python-virtualenv', 'python-dev'])
        self.su("gem install fpm")


class Centos(Distro):

    def __init__(self, *args, **kwargs):
        self.defaults = centos_defaults
        Distro.__init__(self, *args, **kwargs)

    def update_packages(self):
        self.su("yum update -y")

    def build_deps(self, deps):
        self.su("yum install -y %s"%(' '.join(deps)))

    def version(self,package):
        """Look at the debian apt package system for a package with this name and return its version.
        Return None if there is no such package.
        """
        with settings(warn_only=True):
            vstring = run('rpm -qi %s 2>/dev/null | sed -nr "s/^Version.+: ([0-9]+)(-.+)?/\\1/p"' % (package))
            if vstring.return_code:
                # error fetching package info. Assume there is no such named package. Return None
                return None

            # remove vender part of string
            vstring = vstring.split()[0]
            return versions.Version(vstring)

    def check(self):
        """Check the remote build host to see if the relevant software to build packages is installed"""
        with settings(warn_only=True):
            # check for fpm
            result = run('which fpm')
            if result.return_code:
                raise Exception("Build host does not have fpm installed and on the executable path")

    def setup(self):
        """this method sets up a remote centos box for parcel package building.
        Installs fpm and also rubygems if not present.
        """
        self.su("yum install rubygems -y")
        self.su("gem install fpm")
        self.su("yum install rpm-build -y")
        self.su("yum install rsync -y")            

    def build_package(self, deployment=None):
        """
        Runs architecture specific packaging tasks
        """
        assert deployment
        
        with cd(deployment.root_path):
            rv = run(
                'fpm -s dir -t rpm -n {0.pkg_name} -v {0.version} '
                '-a all -x "*.git" -x "*.bak" -x "*.orig" {0.hooks_str} '
                '--description "Automated build. '
                'No Version Control." '
                '{0.deps_str} {0.dirs_str}'
                .format(deployment)
            )

            filename = rv.split('"')[-2]
            get(filename, './')
            run("rm '%s'"%filename)
            print green(os.path.basename(filename))



# the distribution module instances
debian = Debian()
ubuntu = Ubuntu()
centos = Centos()
