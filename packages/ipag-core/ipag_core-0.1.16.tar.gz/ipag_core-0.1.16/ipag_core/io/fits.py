from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from astropy.io import fits
from ipag_core.define import  DataReader, DataWriter, MetadataLike ,  DataTuple, PathGetter
from ipag_core.path import Path 
from ipag_core.log import get_logger

import numpy as np 

log = get_logger()


def parse_meta_value( value ):
    """ Some conversion value for fits header """
    if isinstance( value, datetime):
        return str(value)
    return value 


def metadata2header( metadata: MetadataLike, model:fits.Header | None )->fits.Header:
    """ convert some metadata object into a fits header """
    if isinstance(metadata, fits.Header ):
        return metadata
    if metadata is None:
        metadata = {} 

    if model is None:
        return fits.Header( metadata )
     
    header = model.copy()
    if hasattr( metadata, "keys"):
        for key in metadata.keys():
            header[key] = parse_meta_value (metadata[key])
    else:
        for key, value in metadata:
            header[key] = parse_meta_value( value )
    return header

@dataclass
class FitsIo(DataReader, DataWriter):
    """ Fits file reader 
    
    This is a data reader and writer. This is problably more clean to use 
    instead a :class:`FitsReader` or a :class:`FitsWriter` object. 

    Args:
        file: file name, absolute or relative path 
        path: default is Path(".") curent directory 
        overwrite: if True (default) file is overwriten 
        extention: fits extention number or name 
        header_model: optional, a fits.Header object containing default 
            fits file header to write. Values are updated from metadata 
            to a model copy.
    """
    file: str 
    path: PathGetter = field(default_factory=Path)
    overwrite: bool = False
    extension: int | str = 0
    header_model: fits.Header | None = None 
    
    def write(self, data: Any, metadata: MetadataLike | None = None):
        """ Write data into fits file  """
        filename = self.path.get_path(self.file)
        
        fits.writeto(
                 filename, data, 
                 header=metadata2header(metadata, self.header_model),
                 overwrite=self.overwrite
            )
        log.info(f"Data file '{filename}' writen")

    def read(self, metadata: MetadataLike|None=None)->np.ndarray:
        filename = self.path.get_path(self.file)
        with fits.open( filename ) as fh_list:
            fh = fh_list[self.extension]
            if metadata is not None:
                metadata.update( fh.header ) 
            return fh.data.copy()


@dataclass
class FitsReader(DataReader):
    """ A Reader object dedicated for fits file (one extension) 

    Args:
        file: file name, absolute or relative path 
        path: default is Path(".") curent directory 
        extention: fits extention number or name 
        cash: if True the data is loaded only once. If file or path 
            is changed by the user and cash is True. User should 
            call the `clear_cash()` method. 
    
    Outputs:
        data: np.ndarray 
        metadata: fits.Header 

    """
    file: str 
    path: PathGetter = field(default_factory=Path)
    extension: int | str = 0
    cash: bool = True 
    
    _hdu_list = None 
    
    def _load_fits(self):
        filename = self.path.get_path(self.file)
            
        with fits.open( filename ) as fh_list:
            fh =  fh_list[self.extension]
        return fh
    
    def clear_cash(self):
        if self._hdu_list:
            self._hdu_list.close()
        self._hdu_list = None 
    
    def __del__(self):
        try:
            self.clear_cash()
        except Exception:
            pass 

    def read(self, metadata: MetadataLike|None=None) -> np.ndarray:
        if self.cash:
            if self._hdu_list is None:
                filename = self.path.get_path(self.file)
                self._hdu_list = fits.open( filename ) 
                
            fh = self._hdu_list[self.extension]
            if metadata is not None:
                metadata.update( fh.header ) 
            
            return fh.data.copy()

        else:
            filename = self.path.get_path(self.file)
            with fits.open( filename ) as fh_list:
                fhe =  fh_list[self.extension]
                if metadata is not None:
                    metadata.update( fhe.header ) 
                return fhe.data.copy()

@dataclass 
class FitsWriter(DataWriter):
    file: str 
    path: PathGetter = field(default_factory=Path)
    overwrite: bool = False 
    header_model: fits.Header | None = None 

    def write(self, data: Any, metadata: MetadataLike | None = None):
        """ Write data into fits file  """
        header = metadata2header(metadata, self.header_model)
        now = str(datetime.now()).replace(" ","T")
        filename = self.path.get_path( str(self.file).format( datetime=now,  **header )  )
        
        fits.writeto(
                 filename, data, 
                 header=header,
                 overwrite=self.overwrite
            )
        log.info(f"Data file '{filename}' writen")
   


@dataclass
class FitsFilesReader(DataReader):
    """ Fits DataReader using a list of fits file

    Fits file data are merged into one single array     
    The metadata (header) of individual file is lost 
    """
    files: list[str]
    path: PathGetter = field(default_factory=Path)
    extension: int = 0
    
    def read(self,  metadata: MetadataLike | None = None):
        files = (self.path.get_path(file) for file in self.files) 
        data = [] 
        for file in files:
            data.append( fits.getdata(file, self.extension) )
        data = np.asarray(data)
        return data


