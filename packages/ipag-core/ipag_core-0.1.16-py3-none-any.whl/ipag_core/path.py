""" Tha Goal of Path objects is to resolve a file path string from a file name """

from __future__ import annotations
from dataclasses import dataclass, field
from  importlib import resources 
from ipag_core.define import PathGetter
from ipag_core.log import get_logger 

import datetime 
import os 


log = get_logger()

def create_dir(directory):
    if not os.path.exists( directory ):
        os.makedirs( directory )
        log.info(f"Directory '{directory}' created")

def directory( obj: str | PathGetter):
    try:
        gd = obj.get_directory 
    except AttributeError:
        return str(obj)
    else:
        return gd()


@dataclass
class Path:
    """ Basic PathGetter taking a root directory 
    
    If .get_path(file) recive a relative file the root directory is prefixed.
    If .get_path(file) recive an absolute path the root directory is ignored  
    
    Attributes:
        root: Root directory  "." by default.  
    """
    root: str | PathGetter = "." 
    def get_directory(self):
        return directory(self.root) 
    
    def get_path(self, path:str):
        return os.path.join( self.get_directory(), path) 

@dataclass
class AutoPath(Path):
    """ Same as Path but create the directories automaticaly if not exists """
    root: str | PathGetter = "."
    def get_directory(self):
        root = directory(self.root)
        create_dir(root)
        return root 


def unique_file(root: str | PathGetter, file_name, suffix_format="_%03d"):
    """ Return a unique path for the given directory and file_name
    
    Args:
        root: root directory (str or Path) 
        file_name:  file_name with extention 
        suffix_format (optional, str): suffix format for the file counter , default is "_%03d" 

    Note: for performance reason the first available file slot will be taken. If files
        has been removed this can lead to an un-intuitive result. 
    """
    root = directory(root)
    if not os.path.exists( os.path.join(root,file_name) ):
        return os.path.join(root,file_name) 
    core, ext = os.path.splitext( file_name)
    i=1
    while True:
        new = os.path.join(root, core+(suffix_format%i)+ext)
        if not os.path.exists(  new ):
            return new
        i += 1 
    

@dataclass 
class UniquePath:
    """ PathGetter. Make sure that a file is unique by adding a suffix counter onfile core 
    
    This is suitable for write only IO. It is an error to use it on read IO

    Note: for performance reason the first available file slot will be taken. If files
        has been removed this can lead to an un-intuitive result. 
    """
    root: str | PathGetter = "."
    suffix_format: str = "_%03d"
    def get_directory(self):
        return directory(self.root) 
    
    def get_path(self, path:str):
        return unique_file( self, path, self.suffix_format) 


@dataclass
class TodayPath(Path):
    """ PathGetter. Resolve file path as  root/yyyy-mm-dd/file  

    Attributes:
        root: root directory 
        date: default is datatime.now(). datetime or date object 
        date_format: default '%Y_%m_%d'
        makedir:  If True (default) missing directories are created 
    """
    root: str | PathGetter = "."
    date: datetime.datetime = field( default_factory= datetime.datetime.now )
    date_format: str = '%Y_%m_%d'
    makedir: bool = True

    def get_directory(self):
        path = os.path.join( directory(self.root), self.date.strftime(self.date_format) )
        if self.makedir: create_dir(path)
        return path 
    

@dataclass
class ResourcePath:
    """ A PathGetter object, it will try to resolve the path from a resource file name 

    Its accept an OS environ variable name (containing a list of ':' separated directories).
    And an optional pkg_name and pkg_resource_dir to be explored. 
    """

    env: str = ""
    """ Environment variable containing resource directories """
    pkg_name: str = ""
    """ Package name. If provided resource will be search in package resources """
    pkg_directories: list[str] = field(default_factory=list)
    """ A list of relative directories located inside the python package  """

    def get_directory(self):
        raise ValueError("ResourcePath cannot return one single directory")

    def _get_env_directories(self):
        if self.env:
            return [d.strip() for d in  os.environ.get(self.env,"").split(":") if d.strip()]
        return [] 

    def get_path(self, filename: str)->str:
        env_directories = self._get_env_directories()

        for root in env_directories: # TODO: Check the order of directory
            if root.strip() and os.path.exists( os.path.join(root, filename)):
                return os.path.join(root, filename)

        if self.pkg_name:
            for pkg_dir in self.pkg_directories:
                path = os.path.join(pkg_dir, filename)
                target = resources.files(self.pkg_name).joinpath( path) 
                if target.is_file():
                    return str(target)
                        
            pkg_error = f" Neither is package resource {target} "
        else:
            pkg_error = ""
        raise ValueError( f"Cannot find resource '{filename}' in any of: {env_directories} {pkg_error}" )

