from typing import Any, Dict, List
from pydantic import (
    BaseModel, Field, RootModel, ConfigDict 
)

user_model_config = ConfigDict(validate_assignment = True, extra="forbid")
""" A configuration for any model which will be modified by user """

state_model_config = ConfigDict()


class UserModel(BaseModel):
    model_config = user_model_config

class StateModel(BaseModel):
    model_config = state_model_config


def merge_model(base_model: BaseModel, *args: List[BaseModel], **kwargs: Dict[str,Any])->BaseModel:
    """ merge pydantic models into one """
    d = {}
    for m in args:
        d.update( m.model_dump( exclude_unset = True) )
    new_model = base_model.model_copy(update=d) 
   
    for key,value in kwargs.items():
        setattr(new_model, key, value) 
    return new_model  
    
