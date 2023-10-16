from __future__ import annotations
from dataclasses import dataclass, field
import enum
import inspect
from typing import Any, Callable

from ipag_core.define import DataReader, DataTuple, DataWriter, DataProcessor,  MetadataLike
from ipag_core.metadata import new_metadata

class PipelineType(enum.Enum):
    WRITER = enum.auto()
    PROC = enum.auto()

def _read(obj, metadata, analyses):
    return obj.read()
def _read_with_analyses(obj, metadata, analyses):
    return obj.read(analyses=analyses)
def _read_with_metadata(obj, metadata, analyses):
    return obj.read(metadata=metadata)
def _read_with_metadata_and_analyses(obj, metadata, analyses):
    return obj.read(metadata=metadata, analyses=analyses)

def _process(obj, data, metadata, analyses):
    return obj.process(data)
def _process_with_analyses(obj, data, metadata, analyses):
    return obj.process(data, analyses=analyses)
def _process_with_metadata_and_analyses(obj, data, metadata, analyses):
    return obj.process(data, metadata=metadata, analyses=analyses)
def _process_with_metadata(obj, data, metadata, analyses):
    return obj.process(data, metadata=metadata)

def _process_func(func, data, metadata, analyses):
    return func(data)
def _process_func_with_analyses(func, data, metadata, analyses):
    return func(data, analyses=analyses)
def _process_func_with_metadata_and_analyses(func, data, metadata, analyses):
    return func(data, metadata=metadata, analyses=analyses)
def _process_func_with_metadata(func, data, metadata, analyses):
    return func(data, metadata=metadata)


def _write(obj, data, metadata, analyses):
    obj.write(data)
    return data
def _write_with_analyses(obj, data, metadata, analyses):
    obj.write(data, analyses=analyses)
    return data 
def _write_with_metadata_and_analyses(obj, data, metadata, analyses):
    obj.write(data, metadata=metadata, analyses=analyses)
    return data 
def _write_with_metadata(obj, data, metadata, analyses):
    obj.write(data, metadata=metadata)
    return data 

_callers = {'reader': {
                'empty': _read , 
                'analyses': _read_with_analyses, 
                'metadata': _read_with_metadata, 
                'metadata+analyses':_read_with_metadata_and_analyses
            }, 
            'processor': {
                'empty': _process , 
                'analyses': _process_with_analyses, 
                'metadata': _process_with_metadata, 
                'metadata+analyses':_process_with_metadata_and_analyses
            }, 
            'func': {
                'empty': _process_func , 
                'analyses': _process_func_with_analyses, 
                'metadata': _process_func_with_metadata, 
                'metadata+analyses':_process_func_with_metadata_and_analyses
            }, 
            'writer': {
                'empty': _write , 
                'analyses': _write_with_analyses, 
                'metadata': _write_with_metadata, 
                'metadata+analyses':_write_with_metadata_and_analyses
            }
        }

def _get_caller( method: Callable, group: str):
    s = inspect.signature( method ) 
    parameters = s.parameters
    callers_dict  = _callers[group]

    if "metadata" in parameters and parameters["metadata"].default is not s.empty:
        if "analyses" in parameters and parameters["analyses"].default is not s.empty:
            return callers_dict['metadata+analyses']
        else:
            return  callers_dict['metadata']
    elif "analyses" in parameters and parameters["analyses"].default is not s.empty:
         return callers_dict['analyses']
    else:
        return callers_dict['empty']


def _parse_reader( reader: DataReader)->tuple[DataReader, Callable]:
    return reader, _get_caller( reader.read, 'reader')
      
def _parse_processor( processor: DataProcessor):
    if isinstance( processor, DataProcessor):
        return processor, _get_caller( processor.process, 'processor')
    if hasattr( processor, "__call__"):
        return processor, _get_caller( processor, 'func')
    if hasattr( processor, "__iter__"):
        return DataPipe(*processor), _callers['processor']['metadata+analyses']
    raise ValueError("Invalid Processor, expecting an object with process method, a function or an iterable" )


def _parse_writer( writer: DataWriter)->tuple[DataWriter, Callable]:
    return writer, _get_caller( writer.write, 'writer')   

def read(reader: DataReader, metadata:MetadataLike|None = None, analyses:object|None=None):
    reader, caller = _parse_reader( reader )
    return caller( reader, metadata, analyses )

def write(writer: DataWriter, data: Any, metadata:MetadataLike|None = None, analyses:object|None=None):
    writer, caller = _parse_writer( writer )
    return caller( writer, metadata, analyses )

def process( processor :DataProcessor , data: Any, metadata:MetadataLike|None = None, analyses:object|None=None):
    processor, caller = _parse_processor( processor )
    return caller( processor, metadata, analyses )

def read_all(  reader: DataReader ):
    metadata = new_metadata()
    data = read( reader, metadata=metadata)
    return DataTuple( data, metadata) 
    


class DataPipe(DataReader, DataWriter, DataProcessor):
    """ Create a pipeline of data 
    
    The pipeline can be made of: 
        - one DataReader (must be the first argument)
        - none, one or several data processors 
        - none one or several DataWriter 
    
    A processor in the pipeline  can be:
        - a DataProcessos with signature obj.process(data)->newdata
            Also the method accept a `metadata=` kw to transform metadata 
                in place. And a `anaylses` where new analysis object are 
                added in place.
        - a callable with f(data)->data signature  
        - a list of one of the above
    
    """
    def __init__(self, *args: DataReader|DataWriter|DataProcessor):
        self._reader = None 
        self._reader_caller = None 
        self._pipeline = []
        self._pipeline_types = []
        self._has_writer = False 
        if args:
            if isinstance( args[0],  DataReader):
                self._reader, self._reader_caller = _parse_reader( args[0] )
                args = args[1:]
        self.extend( args ) 
    
    def _check_if_has_writer(self):
        self._has_writer = any( t==PipelineType.WRITER for t,_ in  self._pipeline_types)
    
    def _iter_pipe(self):
        for ptype, obj in zip(self._pipeline_types, self._pipeline):
            yield ptype, obj
    
    def read(self, metadata:MetadataLike|None = None, analyses:object|None = None) -> Any:
        if self._reader is None:
            raise ValueError( "This Data Pipe has no DataReader")
        
        data = self._reader_caller( self._reader, metadata, analyses)    
        

        for (_,caller), obj in self._iter_pipe():
            data = caller( obj, data, metadata, analyses) 
        return data 

    def write(self, data: Any, metadata:MetadataLike|None = None, analyses:object|None = None):
        if not self._has_writer:
            raise ValueError( "This Data Pipe has no DataWriter defined" )
        
        for (_,caller), obj in self._iter_pipe():
            data = caller( obj, data, metadata, analyses)
                    
    def process(self, data, metadata:MetadataLike|None = None, analyses:object|None = None) -> Any:
        for (ptype,caller),  obj in self._iter_pipe():
            if ptype == PipelineType.WRITER: continue 
            data = caller( obj, data, metadata, analyses)
        return data 
    

    def append(self, proc_or_writer: DataWriter | DataProcessor)->None:
        """ Append a new DataWriter or DataProcessor to the pipeline """
        if isinstance( proc_or_writer, DataWriter):
            writer, caller = _parse_writer( proc_or_writer) 
            self._pipeline.append(writer)
            self._pipeline_types.append( (PipelineType.WRITER, caller) ) 
            self._has_writer = True
        else:
            processor, caller = _parse_processor( proc_or_writer)
            self._pipeline.append(processor)
            self._pipeline_types.append( (PipelineType.PROC, caller) ) 
       
    def extend(self, proc_or_writer_list : list[ DataWriter|DataProcessor ] ):
        """ Extend a new DataWriters or DataProcessors to the pipeline """

        for obj in proc_or_writer_list:
            self.append( obj )

    def insert(self, index, proc_or_writer: DataWriter | DataProcessor)->None:
        """ Insert  a new DataWriter or DataProcessor to the pipeline at given index """
        if isinstance( proc_or_writer, DataWriter):
            writer, caller = _parse_writer( proc_or_writer) 

            self._pipeline.insert(index, writer)
            self._pipeline_types.insert(index, (PipelineType.WRITER, caller) ) 
            self._has_writer = True 
        else:
            processor, caller = _parse_processor( proc_or_writer)

            self._pipeline.insert(index,  processor )
            self._pipeline_types.insert(index, (PipelineType.PROC, caller) ) 
    
    def purge(self, *types):
        """ remove all processor matching any of the given types """
        for obj in list(self._pipeline):
            if isinstance( obj, types):
                self.remove( obj )

    def pop(self, index=-1):
        """ Pop pipeline element at given index (default is the last one) """
        robj = self._pipeline.pop(index) 
        self._pipeline_types.pop(index)
        self._check_if_has_writer()
        return robj 
    
    def remove(self, obj):
        """ Remove a given object on the pipeline """
        i = self._pipeline.index(obj)
        self._pipeline.remove(obj)
        self._pipeline_types.pop(i) 
    
    def index(self, obj):
        """ Return pipeline index of the given object """
        return self._pipeline.index(obj)
    
    def clear(self):
        """ Clear the pipeline (The DataReader, if any, stays)"""
        self._pipeline.clear()
        self._pipeline_types.clear()

    def copy(self):
        """ copy this pipeline to a new one """
        if self._reader:
            return self.__class__(self._reader, *self._pipeline)
        else:
            return self.__class__( *self._pipeline)
    
    

