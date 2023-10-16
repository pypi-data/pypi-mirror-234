from __future__ import annotations
from functools import partial
import inspect
from typing import Callable, Type
from pydantic import BaseModel
from ipag_core.yaml import IpagLoader
import yaml 
import sys 
import json 
import class_doc 

usage = """{name} dump|check|run [file_name] [--key1=val1] [--key2=val2] ... 
{name} help  

Commands:
    dump  [conf_file] [--options..] : print out a new yaml configuration edited with 
                                      configuration fron conf_file and inline options
    check  [conf_file] [--options..] : dry run just check if all arguments are okay  
    run [conf_file] [--options..]:    run the script 
    help:  print out a list of options, default value, type and eventual description
"""


def build_cli(Setup: BaseModel, runner: Callable, name="program")->Callable:
    """ A basic cli maker for ipag scripts taking a BaseModel and a runner 

    This cli should evolve but its usage shall be kept simple 

    Exemple::

        from ipcag_core import ipag 
        from pydantic import BaseModel 
        import sys 

        class MySetup(BaseModel):
            message: str = ""
            n_time: int = 1

        def run(setup:MySetup):
            for i in range( setup.n_time):
                print( setup.message)

        main = ipag.build_cli( MySetup, run, "my_script")
        if __name__ == "__main__":
            main()

    The programm can then be executed as :

        my_script run --message='Some message' --n_time=4 

    Or a setup file can be created and edited  

        my_script dump > my_script_setup.yaml  
        my_script run my_script_setup.yaml 
    
    Options can also be changed on top of a configuration file:

         my_script run my_script_setup.yaml --n_time=10 
    
    The command 'check' allows to check if all arguments are parsed correctly 
    without running the program 
        

        my_script check  --n_time=10 

    """
    narg = _get_number_of_args( runner) 
    def cli_runner():
        sys.exit( _run_cli(Setup, runner, name=name, extras=narg>1))
    return cli_runner 



def _parse_argv( argv ):
    new_argv = []
    options = []
        
    n = len(argv)
    i = 0
    while i<n:
        arg = argv[i]
        arg = arg.strip()
        i+=1 

        if arg.startswith("--"):
            arg = arg[2:]
            name, _, value = arg.partition("=")
            if not value:
                if arg.endswith("="):
                    try:
                        value = argv[i]
                    except IndexError:
                        raise ValueError(f"incomplete option missing value for {arg}")

                    i+=1
                else:
                    try:
                        next_arg = argv[i]
                    except IndexError:
                        raise ValueError(f"incomplete option. nothing after {arg}")
                    next_arg = next_arg.strip()
                    i+=1
                    if next_arg == "=":
                        try:
                            value = argv[i]
                        except IndexError:
                            raise ValueError(f"incomplete option missing value for {arg}")
                        i+=1 
                    else:
                        _, _, value = next_arg.partition("=")
                        if not value:
                            raise ValueError(f"incomplete option {arg}, {next_arg}")
            # options.append( (name, json.loads(value)))
            options.append( (name, value) )
        else:
            new_argv.append( arg )

    return new_argv, options 
                 
def _modify( model: BaseModel, key, value):
    keys = key.split(".") 
    for k in keys[:-1]:
        model = getattr(model, k)
    setattr(model, keys[-1], value)

def _build_setup( Setup: Type[BaseModel], argv:list[str]):
    argv, options = _parse_argv(argv)
    if argv:
        file = argv.pop(0)
        if file:
            with open(file) as f:
                setup = Setup.model_validate( yaml.load( f, IpagLoader))
        else:
            setup = Setup()
    else:
        setup = Setup()

    for key, value in options:
        _modify(setup, key, value)
    return setup, argv 

def _get_number_of_args(runner):
    sig = inspect.signature( runner )
    return sum(1 for param in sig.parameters.values() if (param.kind == param.POSITIONAL_OR_KEYWORD and param.default == param.empty))



def _join(*args):
    return ".".join( a for a in args if a)

def _fields_help( Setup:Type[BaseModel], helps:list[str], prefix:str):
    try:
        cl_docs = class_doc.extract_docs_from_cls_obj(Setup)
    except ValueError:
        cl_docs = {}

    for field, field_info in Setup.model_fields.items():
        if isinstance (field_info.default, BaseModel):
            _fields_help( field_info.default.__class__, helps, _join(prefix, field))
        else:
            key = _join(prefix, field)
            description = field_info.description 
            if description is None:
                description =  ("\n"+" "*45).join ( cl_docs.get(field, []))
            
            keyval =  f'--{key} = {field_info.default}'
            helps.append( f'{keyval:40s} [{field_info.annotation!r}] {description}' )

def help(  Setup:Type[BaseModel] )->str:
    helps =[ ]
    _fields_help( Setup, helps, "")
    return "\n".join( helps)






def _run_cli(Setup: Type[ BaseModel ], runner: Callable, name="program", extras=False)->Callable:
    
    argv = sys.argv[1:]

    def error():
        print( usage.format(name=name) )
        return 1
    
    

    if not argv:
        return error() 
    
    cmd = argv.pop(0)
    if cmd == "help":
        print( help( Setup ) )
        return 1  
    elif cmd == "dump":
        setup, extra_args = _build_setup(Setup, argv)
        if not extras and extra_args:
            print(f"This script does not take any extra argument {extra_args}")
            return error() 
        
        yaml_setup = yaml.dump( setup.model_dump() )
        print(yaml_setup)
        return 0 

    elif cmd == "check":
        _, extra_args = _build_setup( Setup, argv)  
        if not extras and extra_args:
            print(f"This script does not take any extra argument {extra_args}")
            return error() 

        return 0 

    elif cmd == "run":
        setup, extra_args = _build_setup( Setup, argv)
        if not extras and extra_args:
            print(f"This script does not take any extra argument {extra_args}")
            return error() 
        if extras:
            runner(setup, extra_args)
        else:
            runner(setup)
        return 0
    
    return error()



