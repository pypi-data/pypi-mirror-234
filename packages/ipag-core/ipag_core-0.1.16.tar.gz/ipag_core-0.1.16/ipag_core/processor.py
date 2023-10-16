from __future__ import annotations
from dataclasses import dataclass, field
from functools import partial
from inspect import signature
from typing import Any, Callable
from typing_extensions import Protocol

import numpy as np
from ipag_core.define import DataProcessor,  MetaSetter, MetadataLike 
from ipag_core.metadata import new_metadata



@dataclass 
class DataReducer:
    """ Reduce data with a function f(data, axis=) as e.g. np.mean 

    Parameters:
        reducer: reduce function, default is np.mean 
        axis: axis number to reduce 'a la numpy'  
    """
    
    reducer: Callable = field( default= np.mean)# method to collapse the first cube dimension 
    """ method of signature f(a, axis=) to reduce the data. Default is np.mean  """
    
    axis: int | tuple = 0 
    """ Which axis is being reduced """

    def process(self, data):
        return self.reducer(np.asarray(data), axis=self.axis)

@dataclass 
class DataSubstractor:
    """ Processor substracted a Dark to data """
    offset:  float | np.ndarray 
    enabled: bool = True 
    def process(self, data):
        if self.enabled:
            return np.asarray(data)-np.asarray(self.offset)
        return np.asarray(data)


def _modulo_take( a:np.ndarray, index: int, axis: int =0):
    l = a.shape[axis]
    return np.take( a, index%l , axis)


@dataclass
class AxisLooper:
    """ This processor is looping over one axis of the input array

    The returned array will have one dimension less. 
    When the axis length is exhausted it will restart from index 0
    """

    axis: int = 0
    """ axis number to iter on """

    _iteration = 0 
    def process(self, data:np.ndarray, metadata:MetadataLike|None =None) -> np.ndarray:
        new_data =  _modulo_take(data, self._iteration, self.axis )
        self._iteration += 1
        return new_data


@dataclass 
class MetadataAdder:
    """ Transform the metadata by adding information from a state object 
    
    The metadata is copied unless copy is false 

    Args:
        state: A data structure 
        setter: a MetaSetter appropriate for the state data 
        prefix: optional prefix added to metadata keys
        copy: if True (default) the returned metadata is copied otherwise 
            it is transformed in place 
    """
    state: Any
    setter: MetaSetter
    prefix: str = ""
    enabled: bool = True 
    
    def process(self, data, metadata:MetadataLike|None=None)->np.ndarray:
        if metadata is None or not self.enabled:
            return data 
        
        self.setter.set_to_metadata( metadata, self.state, prefix=self.prefix )
        return data
    
    def new_metadata(self):
        metadata = new_metadata()
        self.setter.set_to_metadata( metadata, self.state, prefix=self.prefix )
        return metadata

@dataclass 
class ImageTransformer(DataProcessor):
    """ A simple Image data processor to flip and transpose image 

    Args:
        flip_cols: if True, columns (second dimension) is flipped
        flip_rows: if True, rows (first diemnsion) is flipped 
        transpose: if True the table is transposed (after the flip !!)
        enabled:  set to False to disable the data process
    """
    flip_cols: bool = False 
    flip_rows: bool = False 
    transpose: bool = False 
    enabled: bool = True 

    def process(self, data, metadata=None) -> np.ndarray:
        if not self.enabled:
            return data 
        if self.flip_cols:
            data = data[:,::-1]
        if self.flip_rows:
            data = data[::-1,:]
        if self.transpose:
            data = data.transpose()
        return data  




