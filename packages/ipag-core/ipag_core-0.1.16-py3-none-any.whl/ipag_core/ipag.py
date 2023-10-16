""" This is the public API for the ipag_core package """

from ipag_core.log import init_logger, get_logger

from ipag_core.define import (
    DataProcessor,
    DataReader, 
    DataTuple,
    DataWriter, 
    DataReaderAndWriter, 
    PathGetter,
    MetadataLike, 
    SupportsUpdate, 
    SuportsSetup, 
    MetaSetter, 
    MetaGetter, 
    MetaGetterSetter, 
    MetadataPopulator, 
)

from ipag_core.io.base import (
    DataPipe
)

from ipag_core.io.fits import (
    FitsIo,
    FitsReader, 
    FitsWriter, 
    FitsFilesReader, 
)

from ipag_core.io.array import (
     RandomDataReader, OnesDataReader, ZerosDataReader
)

from ipag_core.data import( 
    DataContainer
)

from ipag_core.log import ( 
    init_logger, 
    get_logger,
)

from ipag_core.processor import (
    AxisLooper, 
    DataReducer, 
    DataSubstractor,
    MetadataAdder, 
    ImageTransformer
)

from ipag_core.path import (
    Path, 
    AutoPath, 
    UniquePath, 
    TodayPath, 
    ResourcePath
)

#place holder of an IPAG configured BaseModel 
from ipag_core.pydantic import (
    Field, 
    UserModel, 
    StateModel, 
    user_model_config, 
    merge_model
)

from ipag_core.metadata import (
    new_metadata, 
    flatten_metadata_model, 
    MetaVal, 
    MetaNamedVal, 
    MetaObj,
    MetaXYArray, 
    MetaMatrix, 
    MetaList
)

from ipag_core.yaml import IpagLoader 
from ipag_core.cli import build_cli 

from ipag_core import types
from ipag_core import metadata_model 


