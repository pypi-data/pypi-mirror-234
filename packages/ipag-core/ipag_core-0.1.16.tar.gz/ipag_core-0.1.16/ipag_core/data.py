from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
import numpy as np 
from ipag_core.define import DataReader, DataWriter,  MetadataLike 
from ipag_core.metadata import new_metadata 
from ipag_core.io.base import read, write 

@dataclass
class DataContainer(DataReader, DataWriter):
    """ Data & Metadata Container 

    The load method is used as an update of the data and metadata

    Atributes:
        data: Any object representing the data 
        metadata: dictionary like object 
        io: a DataIo object used by load method 
        on_data_changed: a List of callable with signature f(data, metadata)
            All function will be called when a new data is received.
            The functions are not triggered when the data property is changed manually 
            But only when ``load`` or ``write`` are called 

    """
    data: Any | None = None  
    metadata: MetadataLike = field(default_factory=dict)
    io: DataReader| DataWriter | None = None 
    on_data_changed: list[Callable]  = field(default_factory=list) 

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

    def load(self, io: DataReader = None):
        """ load data and metadata internaly 
        
        Args:
            io (DataIo, optional): the io used to read data & metadata 
                If not given the object io attribute is used. If no io is defined 
                Exception is raise. 
        """
        io = io or self.io 
        if io is None:
            raise ValueError("This data container has no default io, provide one")
        if not isinstance( io, DataReader):
            raise IOError( "Io is not readable. Cannot read data" )
        metadata = new_metadata() 
        data = read( io.read, metadata=metadata) 
        self.write( data, metadata=metadata )
                    
    def save(self, io: DataWriter = None):
        """ write internal data and metadata
        
        Args:
            io (DataIo, optional): the io used to write data & metadata 
                If not given the object io attribute is used. If no io is defined 
                Exception is raise. 
        """
        io = io or self.io 
        if io is None:
            raise ValueError("This data container has no default io, provide one")
        if not isinstance( io, DataWriter):
            raise IOError( "Io is not writable. Cannot save data" )

        write( io.write, self.data, self.metadata)
    
    def read(self, metadata:MetadataLike|None= None) -> Any:
        """ Return the data  of this Container 
        
        Args:
            metadata: output, metadata will be writen there on inplace 
        """
        if metadata is not None and self.metadata:
            metadata.update( self.metadata )
        return self.data  

    def write(self, data: Any, metadata: MetadataLike | None = None) -> None:
        self.data = data 
        self.metadata = metadata
        for callback in self.on_data_changed:
            callback( data, metadata)

    def __array__(self):
        return self.data 
    


# TODO: move this zelda speciffic stuff 
def _dp(index):
    return property( lambda self: self.data[0][index])

class Centering(DataContainer):
    """ Data with property of centering information """
    current_x_0_cred = _dp(0)
    current_y_0_cred = _dp(1)
    current_x_0_slm  = _dp(2)
    current_y_0_slm  = _dp(3)
    current_theta    = _dp(5)
    current_grand_x  = _dp(6)
    current_grand_y  = _dp(7)



