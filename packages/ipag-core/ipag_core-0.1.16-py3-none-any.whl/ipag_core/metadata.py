from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Type, Union, Any
from typing_extensions import Annotated

from pydantic import AfterValidator, BaseModel, RootModel, TypeAdapter
from ipag_core import types

from ipag_core.define import MetaGetterSetter, MetadataLike, _Empty, MetaSetter, MetaGetter, MetadataPopulator, MetadataUpdator
from astropy.io import fits 

import math

def fix_meta_key(key):
    if len(key)>8 or " " in key:
        return "HIERARCH "+key 
    return key

def join_meta_keys(*keys):
    return " ".join( k for k in keys if k )

def _passthrue(x):
    return x

class _Empty:
    ...


def _get_meta_value( key, metadata, default):
    try:
        return metadata[key]
    except KeyError:
        if default is _Empty:
            raise ValueError( f"{key} is not part of the metadata. Provide a default to avoid error" )
        return default 

def _set_meta_value( metadata,  key, value, comment):
    try:
        setter = metadata.set 
    except AttributeError:
        # support for normal dictionary 
        metadata[key] = value 
    else:
        setter( key, value, comment) 


_default_parsers = {
    str:str, 
    float:float, 
    int:int, 
    bool:bool, 
    complex:complex, 
    bytes:bytes, 
    Any: _passthrue
}
def _type2parser(vtype):
    try:
        return _default_parsers[vtype]
    except KeyError:
        return TypeAdapter( vtype ).validate_python


def _vtype2parsers(vtype):
    try:
        pin,pout = vtype
    except (TypeError, ValueError):
        if isinstance(vtype, type) and issubclass( vtype, Enum):
            return _type2parser( types.valueof(vtype) ), vtype
        return _type2parser(vtype), _passthrue 
    
    return _type2parser(pin), _type2parser(pout)


@dataclass
class MetaVal( MetaGetterSetter):
    metakey: str 
    description: str = ""
    vtype: Callable|type|tuple = Any    

    def set_to_metadata(self,  metadata: MetadataLike, value: Any,prefix:str = "")-> None:
        if isinstance(value, float) and  math.isnan(value):
            return 
        key = fix_meta_key(  join_meta_keys( prefix, self.metakey ) )
        parse,_ = _vtype2parsers( self.vtype ) 
        _set_meta_value( metadata, key, parse(value), self.description )
    
    def get_from_metadata(self, metadata: MetadataLike, prefix: str ="", default: Any=_Empty )->None:
        key = join_meta_keys( prefix, self.metakey )
        _, parse = _vtype2parsers( self.vtype ) 
        return parse( _get_meta_value( key, metadata, default) )

@dataclass
class MetaNamedVal(MetaGetterSetter):
    metakey: str 
    name: str
    description: str = ""
    vtype: Callable|type|tuple = Any    
    unit: str | None = None

    def set_to_metadata(self,  metadata: MetadataLike, value: Any,prefix: str =""):
         if isinstance(value, float) and  math.isnan(value):
            return 
         key = fix_meta_key(  join_meta_keys( prefix, self.metakey, "VAL" ) )
         parse,_ = _vtype2parsers( self.vtype ) 
   
         _set_meta_value(metadata,  key, parse(value), self.description)

         key = fix_meta_key(  join_meta_keys( prefix, self.metakey, "NAME" ) )
         _set_meta_value(metadata,  key, self.name, f"name of {self.metakey} value")
         if self.unit:
            key = fix_meta_key(  join_meta_keys( prefix, self.metakey, "UNIT" ) )
            _set_meta_value(metadata,  key,  self.unit, f"Unit of {self.metakey} value") 
        
    def get_from_metadata(self,  metadata: MetadataLike, prefix: str = "", default: Any=_Empty ):
        _, parse = _vtype2parsers( self.vtype ) 
        key = join_meta_keys( prefix, self.metakey, "VAL" )
        return parse( _get_meta_value( key, metadata, default) )

class Extra(str, Enum):
    Ignore = "ignore"
    Allow = "allow"
    Forbid = "forbid"

def _get_fields(obj):
    try: # pydantic model 
        return list(obj.model_fields) 
    except AttributeError:
        pass 

    try: # dataclasses 
        return list( obj.__dataclass_fields__)
    except AttributeError:
        pass 
    
    try: # NemedTuple
        return list(obj._fields)
    except AttributeError:
        pass 
    raise ValueError(f"Cannot get field nmaes of {obj}") 


@dataclass
class MetaXYArray(MetaGetterSetter):
    """ set/get to metadata a (small) array of points  """

    name: str = "POINT"
    
    def set_to_metadata(self, metadata, nodes, prefix= ""):
        _set_meta_value (metadata,  join_meta_keys( prefix, f'N{self.name}'), len(nodes), f'number of {self.name}')
        for i,(x,y) in enumerate(nodes):
            _set_meta_value(metadata,  join_meta_keys( prefix, f'{self.name}{i}_X'), x, f'x pos of {self.name} {i}')
            _set_meta_value(metadata,  join_meta_keys( prefix, f'{self.name}{i}_Y'), y, f'y pos of {self.name} {i}')
    
    def get_from_metadata(self, metadata, default=None, prefix=""):
        try: 
            n = metadata[ join_meta_keys(prefix, f'N{self.name}')] 
        except KeyError:
            if default is None:
                raise ValueError( f"cannot extract {self.name} from header" )
            return default 

        node_list = []
        for i in range(n):
            x = metadata[ join_meta_keys( prefix, f'{self.name}{i}_X') ]
            y = metadata[ join_meta_keys( prefix, f'{self.name}{i}_Y') ]
            node_list.append( [x,y] )
        return node_list


@dataclass
class MetaList(MetaGetterSetter):
    """ set/get to metadata a (small) array of points  """

    name: str = "LIST"
    vtype: Callable|type|tuple = Any    

    def set_to_metadata(self, metadata, lst, prefix= ""):
        key = join_meta_keys( prefix, self.name) 
        parse,_ = _vtype2parsers( self.vtype ) 
 
        lst = parse(lst)
        _set_meta_value (metadata,  f'{key}N', len(lst), f'number of {self.name}')
        for i, x in enumerate(lst):
            _set_meta_value(metadata,  f'{key}{i}', x, f' list {self.name} member {i}')
            
    
    def get_from_metadata(self, metadata, default=None, prefix=""):
        key = join_meta_keys( prefix, self.name) 

        try: 
            n = metadata[ f'{key}N' ] 
        except KeyError:
            if default is None:
                raise ValueError( f"cannot extract {self.name} from header" )
            return default 

        lst = []
        for i in range(n):
            x = metadata[ f'{key}{i}' ]
            lst.append( x )
        _, parse = _vtype2parsers( self.vtype )  
        return parse( lst )





@dataclass
class MetaMatrix(MetaGetterSetter):
    """ set/get to metadata a (small) array of points  """

    name: str = "MAT"
    
    
    def set_to_metadata(self, metadata, nodes, prefix= ""):

        def _k(k):
            return join_meta_keys( prefix, k) 

        _set_meta_value (metadata,  _k(f'N{self.name}'), len(nodes), f'number of row of {self.name}')
        if len(nodes):
            M = len(nodes[0])
            
        else: 
            M = 0 
        
        _set_meta_value (metadata,  _k(f'M{self.name}'), M, f'number col of {self.name}')

        for i,values in enumerate(nodes):
            for j,value in enumerate( values):
                _set_meta_value(metadata, _k(f'{self.name}{i}_{j}'), value, f'val of {self.name}[{i},{j}]')
    
    def get_from_metadata(self, metadata, default=None, prefix=""):

        def _k(k):
            return join_meta_keys( prefix, k) 

        try: 
            n = metadata[ _k(f'N{self.name}')] 
            m = metadata[ _k(f'M{self.name}')] 

        except KeyError:
            if default is None:
                raise ValueError( f"cannot extract {self.name} from header" )
            return default 

        return [ [metadata[ _k(f'{self.name}{i}_{j}')] for j in range(m)] for i in range(n) ]


@dataclass
class MetaObj(MetaGetterSetter):
    vtype: Type
    """ Accpeted type are BaseModel, dataclasses, NamedTuple 
    
    Other pydantic annotation are also accepted however in this case 
    a list of fields to considers must be provided. 
    """
    model: dict[str, MetaGetterSetter] =  field( default_factory=dict) 
    """ a dictionary of key->MetaGetterSetter 
    By default the named are matched with the object type fields. 
    """
    fields: list[str] | None = None
    """ An optional list of field names. """
    prefixes: dict[str,str] = field( default_factory=dict )
    """ A dictionary of field name-> prefix 
    This is used to add prefix to any members  
    """
    model_keys: dict[str, str] = field(default_factory=dict)
    """ A dictionary to trasnfor field name to model dictionary key 
    Can be usefull in case the given model is a generic one
    """
    extra: Extra =  Extra.Ignore
    """ extra define what to do when a field in the data is not in the model:
        "ignore": just ignore any set or get. This is the default. 
        "allow": try to set the value into the metadata. Works only for regular values
        "forbid": An error is raised 
    
    """
    
    def __getattr__(self, attr):
        try:
            return object.__getattribute__( self, attr)
        except AttributeError:
            try:
                return self.model[attr]
            except KeyError:
                raise AttributeError(f"{attr!r}")

    def __post_init__(self):
        if self.fields is None:
            try:
                self.fields = _get_fields( self.vtype)
            except ValueError as er: 
                raise ValueError(f"{er}. A possible fix is to set a list of members in this Metadta Setter") from er
    
    @property
    def vtype(self):
        return self._vtype 

    @vtype.setter
    def vtype(self, _vtype):
        self._vtype = _vtype
        self._validator  =  TypeAdapter( self._vtype ).validate_python 
     
    def _new_prefix(self, k,  prefix):
        try:
            p =  self.prefixes[k]
        except KeyError:
            return  prefix 
        else:
            return join_meta_keys(prefix, p)  

    def set_to_metadata(self, metadata: MetadataLike, obj: Any, prefix: str = "") -> None:
        obj = self._validator( obj )
        
        for kobj in self.fields:
            km = self.model_keys.get(kobj, kobj)
            p = self._new_prefix( kobj, prefix)
            set_to_metadata( 
                    metadata, km, self.model, 
                    getattr(obj, kobj), prefix=p, extra=self.extra 
                )

    def get_from_metadata(self,  metadata: MetadataLike, prefix: str = "", default:Any = None):
        if default:
            default = self._validator( default )
        vals = {}
        for kobj in self.fields:
            km = self.model_keys.get(kobj, kobj)
            try:
                field = self.model[km]
            except KeyError:
                if self.extra == Extra.Ignore:
                    continue 
                if self.extra == Extra.Allow:
                    key = fix_meta_key( join_meta_keys( self._new_prefix(kobj, prefix),   km.upper() ))
                    val = metadata[key]
                else:
                    raise ValueError( f"Cannot find member {km!r} inside the model" )
            else:
                p = self._new_prefix( kobj, prefix) 
                if default and hasattr(default, kobj):
                    val = field.get_from_metadata( metadata, prefix=p, default=getattr(default, kobj))
                else:
                    val = field.get_from_metadata( metadata, prefix=p)

            vals[kobj] = val 
        return self._validator(vals)

def flatten_metadata_model(model: dict)-> dict[str,MetaGetterSetter]:
    output = {}
    _flatten_model( output, model, "")
    return output

def _flatten_model( output, model, keys):
    for key, field in model.items():
        output.setdefault(key, field)
        if keys: 
            new_keys = ".".join( (keys, key)) 
            output.setdefault(new_keys, field)
        else:
            new_keys = key
        if hasattr(field, "model"):
            _flatten_model( output, field.model, new_keys) 


def set_to_metadata(
        metadata: MetadataLike, 
        field_name: str, 
        model: dict[str,MetaGetterSetter], 
        value: Any, 
        prefix:str = "", 
        extra: Extra = Extra.Ignore
    )->None:
    try:
        meta_field = model[field_name]
    except KeyError:
        if extra == Extra.Ignore:
            return 
        if extra == Extra.Allow:
            _set_meta_value( metadata, join_meta_keys(prefix, field_name.upper()), value, "")
        else:
            raise ValueError( "no fields found with the name {field_name} in the metadata model" )
    else:
        meta_field.set_to_metadata( metadata, value, prefix=prefix)

def get_from_metadata(
        metadata: MetadataLike, 
        field_name: str, 
        model : dict[str,MetaGetterSetter], 
        default = _Empty, 
        prefix:str =""
    )->Any:
    try:
        meta_field = model[field_name]
    except KeyError:
        return _get_meta_value(join_meta_keys(prefix, field_name), metadata, default)
    else:
        return meta_field.get_from_metadata( metadata, default, prefix=prefix)



   



@dataclass
class MetadataIo:
    model: dict[str, MetaGetterSetter] = field(default_factory=dict )
    extra: Extra = Extra.Ignore 
    
    def set_to(self, metadata: MetadataLike, field_name: str, value: Any, prefix:str = "")->None:
        try:
            meta_field = self.model[field_name]
        except KeyError:
            if self.extra == Extra.Ignore:
                return 
            if self.extra == Extra.Allow:
                _set_meta_value( metadata, join_meta_keys(prefix, field_name.upper()), value, "")
            else:
                raise ValueError( "no fields found with the name {field_name} in the metadata model" )
        else:
            meta_field.set_to_metadata( metadata, value, prefix=prefix)
    
    def get_from(self, metadata: MetadataLike, field_name: str, default = _Empty, prefix:str ="")->Any:
        try:
            meta_field = self.model[field_name]
        except KeyError:
            return _get_meta_value(join_meta_keys(prefix, field_name), metadata, default)
        else:
            return meta_field.get_from_metadata( metadata, default, prefix=prefix)




def new_metadata()->MetadataLike:
    """ create a new Metadata dictionary like object 
    
    .. note::

        So far this is a fits.Header, but this can change in future
    """
    return fits.Header()



if __name__ == "__main__":

    m = new_metadata()
    
    model = dict( dit = MetaVal('DIT', description="Detector Integration Time", vtype=float), 
                  toto = MetaVal('TOTO', vtype=float)
                 )
    class Data(BaseModel):
        dit: float = 0.0
        dot: float = 10.0
    
    MetaObj(Data,model,  model_keys={'dot':'toto'}).set_to_metadata(  m, Data(dit=1.2), "Z")
    print(repr(m))
    print( MetaObj(Data, model).get_from_metadata( m, "Z") )
    

    xy = [[1,2], [3,4], [5,6]]
    MetaXYArray('NODE').set_to_metadata( m, xy)
    xy2 =  MetaXYArray('NODE').get_from_metadata(m) 
    assert xy==xy2
    
    MetaMatrix('MT').set_to_metadata( m, xy)
    xy2 =  MetaMatrix('MT').get_from_metadata(m) 
    assert xy==xy2

    MetaList( 'L').set_to_metadata(m , [1,2,3])
    assert [1,2,3] == MetaList('L').get_from_metadata( m ) 
    print(repr(m))

    MetaList( 'L').set_to_metadata(m , [1,2,3], prefix="A")
    assert [1,2,3] == MetaList('L').get_from_metadata( m , prefix="A") 
    print(repr(m))


    # print( DIT._type_parsers )
    # DIT.set_to(m, 3.45, prefix='DET')
    # TEMP1 = MetaNamedField( "TEMP1", "board", description="temperature [celcius]", unit="c")
    # TEMP1.set_to(m,  6.7, prefix='SENS1')
    # print(repr(m))
    # assert DIT.get_from(m, prefix='DET') == 3.45
    # assert TEMP1.get_from(m,  prefix='SENS1') == 6.7
    
    # from pydantic import NonNegativeInt
    # w = WithParser()
    # w.vtype = NonNegativeInt 
    # w.vtype = (str, float)
    # print( w._parsers) 
    


