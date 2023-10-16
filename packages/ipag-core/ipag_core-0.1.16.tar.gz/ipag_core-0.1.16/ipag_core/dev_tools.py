from functools import partial, wraps
from warnings import warn 

def deprecated(alt="", version="??"):
    """ decorator for deprecated method 

    Exemple::
    
        class A:
            def new_method(self):
                pass

            @deprecated("Use ``new_method instead", "0.1")
            def old_method(self):
                return self.new_method() 

        @deprecated
    """
    return partial(deprecate_method, alt=alt, version=version)

def deprecate_method(func, alt="", version="??"):
    @wraps(func)
    def new_func(*args, **kwargs):
        warn( f"{func.__name__} is deprecated {alt}", DeprecationWarning, stacklevel=2 )
        return func(*args, **kwargs)

    if not func.__doc__:
        doc =  f"\n.. deprecated:: {version}\n\n"
        doc += f"   {alt}\n"
        new_func.__doc__ = doc
    func.__deprecated__ = True 
    return new_func 


