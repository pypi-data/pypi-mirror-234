from typing import Callable
from pysimplelog import Logger

logger = Logger('cli_companion')
logger.set_log_file_basename('log/companion')
# logger.set_minimum_level(logger.logLevels['debug'])
logger.set_minimum_level(logger.logLevels['info'])
logger.set_maximum_level(100,fileFlag=False)

logger.add_log_type("prompt", name="PROMPT", 
                    level=200, color='red', )

logger.add_log_type("response", name="RESPONSE", 
                    level=200, color='blue', )

logger.add_log_type("summary", name="SUMMARY", 
                    level=200, color='green', )

def new_log_level(name:str)-> Callable:
    def log_(msg:str,*args,**kwargs):
        logger.log(name, f'{msg}\n{"#"*10}', *args, **kwargs)
    return log_

logger.response = new_log_level('response')
logger.prompt = new_log_level('prompt')
logger.summary = new_log_level('summary')