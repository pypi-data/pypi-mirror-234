""" So base model for metadata """


from ipag_core.metadata import MetaVal
from ipag_core import types



datetime = MetaVal( "DATETIME", "ISO Date time", (types.DateTimeStr, types.DateTime) )
date = MetaVal("DATE" , "ISO Date", (types.Date, types.Date)  )
dit = MetaVal('DIT',  "[s] Detector integration time", float)
ndit = MetaVal('NDIT', "# Number of integration", int)

if __name__ == "__main__":
    from ipag_core.metadata import new_metadata
    m = new_metadata()
    datetime.set_to_metadata(m,types.datetime.now())
    print( repr(m))

