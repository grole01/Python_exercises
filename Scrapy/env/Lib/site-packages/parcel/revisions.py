import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings
from fabric.contrib.files import sed


class Hg(object):
    """An interface to Mercurial source repositories."""
    def __init__(self,path):
        """Initialise the Hg object to a repository on disk."""
        #: The base path of the Mercurial repository.
        self.path = path

    def branch(self):
        """A property that is the present checked out branch"""
        with lcd(self.path):
            return local('hg branch',capture=True).strip()

    def log(self):
        """A property that is the latest log entry. Returns a dictionary with the following keys:
        changeset: The hash number of the lastest changeset.
        date: The date and time of the latest changeset.
        user: Who committed the change
        summary: The commit message
        tag: if this commit is tagged, this is the tag."""
        with lcd(self.path):
            return dict([
                (a.strip(),b.strip()) 
                for a,b in [
                    line.split(':',1) for line in local('hg log | head -6', capture=True).splitlines()
                ]
            ])
		
    def logs(self):
        """Returns all the log entries as a list of dictionaries. Each dictionary 
        is of the format returned by log."""
        with lcd(self.path):
            logs = local('hg log', capture=True).split("\n\n")
            return [
                dict([
                    (a.strip(),b.strip()) 
                    for a,b in [
                        line.split(':',1) for line in chunk.split('\n')
                    ]
                ]) for chunk in logs
            ]
	
    def pull(self):
        """Issue a hg pull on the repository"""
        with lcd(self.path):
            return local('hg pull',capture=True).splitlines()
    
    def update(self):
        """Issue a hg update on the repository"""
        with lcd(self.path):
            return dict([
                (cat,int(num))
                for num,cat in [
                    str.split(' files ') 
                    for str in local('hg update',capture=True).split(', ')
                ]
            ])

    def describe(self, template='{latesttag}-{latesttagdistance}-{node|short}'):
        """Create a vesrion tag composed of the latest tag, the tag distance,
        and the short hash. For example:

        0.5.1-23-d63d252639de

        composed of the tag 0.5.1, from which we are 23 commits forwards of, with
        a latest changeset of hash d63d252639de
        """
        with lcd(self.path):
            return local('hg log -r . --template %r'%template, capture=True).strip()

    def clone(self, repo):
        """hg clone a repo or path to the present repo location.
        The Hg path and object this is called on should be clean. In other words
        you should call clone() immedately after construction of the Hg object and
        make sure that the Hg object is constructed on an empty path.
        
        eg.

        hg = Hg("build/clone")
        hg.clone("hg+ssh://bitbucet.org/project")
        """
        with lcd(self.path):
            return local('hg clone "{0}" .'.format(repo), capture=True).strip()


class GitException(Exception):
    """This exception is raised when:
    - force_tag is set to true during a describe, when the repository is not on a tag.
    """
    pass


class Git(object):
    """An abstraction of Git Repositories."""

    def __init__(self,path):
        """Initialise a Git object based apon this path."""
        self.path = path

    def branch(self):
        """Return which branch the repository is checked out on."""
        with lcd(self.path):
            return local('git branch',capture=True).strip()[2:]

    def checkout(self, target):
        """Use git checkout to bring the repository to a particular point"""
        with lcd(self.path):
            return local('git checkout '+target, capture=True)

    def log(self):
        """Return all the git logs in a list"""
        with lcd(self.path):
            git_log = local('git log', capture=True)
            return [{
                    'changeset': changeset[0],
                    'date': changeset[2].strip("Date:").strip(),
                    'author': changeset[1].strip("Author: "),
                    'summary': changeset[4].strip()
                    } for changeset in (x.split("\n") for x in ("\n" + git_log).split('\ncommit ')[1:])]

    def pull(self):
        """Execute a git pull in the repository"""
        with lcd(self.path):
            return local('git pull', capture=True)
        
    def describe(self, force_tag=False):
        """Use git describe to create a version tag describing the repository at this point."""
        with lcd(self.path):
            if not force_tag:
                return local('git describe', capture=True)

            # force_tag = True
            with settings(warn_only=True):
                version = local('git describe --exact-match --tags HEAD', capture=True) # this fails if the present working tree is not exactly on a tag

                if version.return_code == 0:
                    return version

                raise GitException("Repository is not checked-out exactly on a tag")

    def clone(self, repo):
        """git clone a repo or path to the present repo location.
        The Git path and object this is called on should be clean. In other words
        you should call clone() immedately after construction of the Git object and
        make sure that the Git object is constructed on an empty path.
        
        eg.

        git = Git("build/clone")
        git.clone("git://github.org/project")
        """
        with lcd(self.path):
            return local('git clone "{0}" .'.format(repo), capture=True).strip()


def repo(path):
    content = os.listdir(path)
    if '.hg' in content:
        return Hg(path)
    if '.git' in content:
        return Git(path)
    return repo(os.path.realpath(path+'/..'))			# recurse back a directory
