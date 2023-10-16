from __future__ import annotations
from typing import Any, Union, NamedTuple
from typing_extensions import Protocol, runtime_checkable
from abc import abstractmethod
import numpy as np 


class MetadataLike(Protocol):
    def __getitem__(self, item):
        """ header keys should be accessisble """
    def __setitem__(self, item , value):
        """ header keys should be updatable """
    
    def copy(self):
        """ Header must copy itself """
    
    def set(self, key:str, value: Any, comment: str):
        """ set value to metadata """
        ...

class DataTuple(NamedTuple):
    """ Named tuple holding data and metadata """
    data: Any 
    metadata: MetadataLike
    def __array__(self):
        return np.asanyarray(self.data)

    def __float__(self):
        return float(self.data)

    def __int__(self):
        return int(self.data) 
    
    def __str__(self):
        return str(self.data)
    
    def __bytes__(self):
        return bytes(self.data) 
    
    def __complex__(self):
        return complex(self.data) 

class DataContainerProtocol(Protocol):
    data: Any
    metadata: MetadataLike
    
    def get_data(self):
        """ Should have a get_data method """

class _Empty:
    """ Represent an _Empty value, when None is not suitable """
    ...


@runtime_checkable
class DataProcessor(Protocol):
    """ Protocol. a DataProcessor must have this defined  methodd  """
    def process(self, data, metadata=None)->DataTuple:
        """ process data and return (new data, new metadta)
        meta data can just also pass thrue 
        """


@runtime_checkable
class Processor(Protocol):
    """ Processor transform any data into new data """
    def process(self, data)->Any:
        """ process data and return data """

@runtime_checkable
class MetadataProcessor(Protocol):
    """ Tranformer transform any metadata into new metadata """
    def process_metadata(self, metadata:MetadataLike)->MetadataLike:
        """ process metadata and return a new one """



@runtime_checkable
class PathGetter(Protocol):
    """ Protocol. A PathGetter object must define these methods 
    
    The role of a PathGetter is to resolve an absolute path from 
    a relative file name. 
    """
    def get_directory(self)->str:
        """ must return the directory """

    def get_path(self, file: str)->str:
        """ must return a resolved complete path from a file path """

@runtime_checkable
class DataReaderAndWriter(Protocol):
    def write(self, data, header=None):
        """ A Io can write data """
        
    def read(self)->tuple[Any, MetadataLike]:
        """ An Io can read """

@runtime_checkable
class DataReader(Protocol):
    """ Protocol. The role of a DataReader is to read data and metadata from any source """
    @abstractmethod
    def read(self)->DataTuple:
        """ Read data and return in a DataTuple(data, metadata) """ 

@runtime_checkable
class DataWriter(Protocol):
    """Protocol. A DataWriter write date and metadata to any target (file, plots, device, ...) """
    @abstractmethod
    def write(self, data: Any, metadata: MetadataLike | None = None)->None:
        """ Write data and optional metadata """
        ...

@runtime_checkable
class SuportsSetup(Protocol):
    """ An object dedicated to the setup of something, like a device """
    @abstractmethod
    def setup(self, obj: Any):
        """ run the setup """

@runtime_checkable
class SupportsUpdate(Protocol):
    """ An object dedicted to update a current state """
    @abstractmethod
    def update(self, obj: Any):
        """ update to self any real state """


@runtime_checkable
class MetaSetter(Protocol):
    """ Object to set a value into metadata object """
    def set_to_metadata(self, metadata: MetadataLike, value: Any, prefix:str = "")->None:
        ... 
        
@runtime_checkable
class MetaGetter(Protocol):
    """ Object to get a value from  metadata object """
    def get_from_metadata(self,metadata: MetadataLike, default=_Empty,  prefix: str = "")->None:
        ...

@runtime_checkable
class MetaGetterSetter(Protocol):
    """ Object to get/set a value or object  from/to a metadata """
    def get_from_metadata(self,metadata: MetadataLike, default=_Empty,  prefix: str = "")->None:
        ...
    def set_to_metadata(self, metadata: MetadataLike, value: Any, prefix:str = "")->None:
        ... 


@runtime_checkable
class MetadataPopulator(Protocol):
    """ Object having the capability to update metadata from itself """
    def populate_metadata(self, metadata: MetadataLike, prefix: str = "")->None:
        ... 

@runtime_checkable
class MetadataUpdator(Protocol):
    """ Object having the capability to update metadata from itself """
    def update_from_metadata(self, metadata: MetadataLike, prefix: str = "")->None:
        ... 


