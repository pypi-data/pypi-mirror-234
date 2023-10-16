
from __future__ import annotations
from datetime import date, datetime

from typing import Callable
from typing_extensions import Annotated

from pydantic import AfterValidator, BeforeValidator


def build( before: tuple[Callable]|None|Callable, type_:type, after: tuple[Callable]|None|Callable):
    """ Helper function to build Annotated type 
    
    Args:
        before: before validator functions, expecting a strict tuple, if not it is converted to (before,)
            None is an empty tuple
        type_: annotated type
        after: after validator functions, expecting a strict tuple, if not it is converted to (after,)
            None is an empty tuple 

    Exemple:: 

        build( (b1, b2), str, (a1, a2) )
        # is equivalent to 
        Annotated[ str , AfterValidator(a1), AfterValidator(a2), BeforeValidator(b2), BeforeValidator(b1)]
        
        build( None, str, (a1, a2) )
        # is equivalent to 
        Annotated[ str , AfterValidator(a1), AfterValidator(a2)]

        build( (b1, b2),  str, None )
        # is equivalent to 
        Annotated[ str , BeforeValidator(b2), BeforeValidator(b1)]

        build( b1, str, a1)
        # is equivalent to 
        Annotated[ str , AfterValidator(a1),  BeforeValidator(b1)]


    """
    if before is None:
        before = tuple()
    elif not isinstance( before , tuple):
        before = (before,)
    if after is None:
        after = tuple()
    elif not isinstance( after, tuple):
        after = (after, )
    
    annotate: tuple =  tuple( [type_]+[AfterValidator(a) for a in after]+[BeforeValidator(a) for a in reversed(before)] ) 
    return Annotated[annotate] 

def to_string(type_):
    """ Return a Annotated type into a tring 
    
        Annotated[type_, AfterValidator(str)]

    """
    return Annotated[type_, AfterValidator(str)]


def valueof(enum):
    """ Annotated type that use an Enum member type but parse the value """
    return Annotated[enum, AfterValidator(lambda e:e.value)]



DateTimeStr = str 
DateStr = str
DateTime = datetime
Date = date 


if __name__ == "__main__":
    from pydantic import TypeAdapter
    
    assert TypeAdapter(  build(str, str, lambda x:x+"E1")).validate_python( 2) == "2E1"
    assert TypeAdapter( Annotated[str, AfterValidator( lambda x:x+"E1"), BeforeValidator(str) ] ).validate_python( 2) == "2E1"

    assert TypeAdapter( build( (str,lambda x:x+"A", lambda x:x+"B"), str, (lambda x:x+"C", lambda x:x+"D") ) ).validate_python("") == "ABCD"
    assert TypeAdapter( build( None, str, (lambda x:x+"C", lambda x:x+"D") ) ).validate_python("") == "CD"
    
    print( DateTimeStr )
    TypeAdapter( DateTimeStr).validate_python( datetime.now() ) 
