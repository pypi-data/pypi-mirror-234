import logging

IPAG_LOGGER = "ipag"

def init_logger(level: int = logging.DEBUG)->logging.Logger:
    """ Initialize and configure the Ipag  logger 
    
    Args:
        level: logger level default is logging.DEBUG
    """
    logger = get_logger() 

    logger.setLevel(level)
    ch = logging.StreamHandler() 
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)    
    logger.addHandler(ch)
    return logger

def get_logger(child_log:str  = "")->logging.Logger:
    """ Return the ipag logger 
    
    Args:
        child_log: optional child log addded to the IPAG root logger (e.g. '.cred2') 
    """
    return logging.getLogger( ".".join(  (IPAG_LOGGER, child_log.strip(".")) ))

    
        
