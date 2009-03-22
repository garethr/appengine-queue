import logging
import traceback

def log_exception():
    logging.log(logging.ERROR, "Error: %s", traceback.format_exc())

class ApiException(Exception):
    def __init__(self):
        log_exception()

class ApiTaskExpired(ApiException):
    pass
    
class ApiNoTasks(ApiException):
    pass
    
class ApiMethodUnavailable(ApiException):
    pass
    
class ApiLockError(ApiException):
    pass
    
class ApiTaskDoesntExist(ApiException):
    pass