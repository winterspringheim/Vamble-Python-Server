from functools import wraps
import time
import helpers.constants as constants

def async_wrapper(func):
    """
    A decorator to ensure a function is awaited when called.
    """
    @wraps(func)
    async def with_async_wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return with_async_wrapper
        
def performance_tester(func): 
    """
    A decorator to measure and print the execution time of a function.
    """
    @wraps(func)    
    def with_performance_test(*args, **kwargs):
        start = time.time()
        returned_value = func(*args, **kwargs)
        print("Calling function " + func.__name__ + " took: " + str(time.time() - start) + " seconds")
        return returned_value
    
    return with_performance_test

def async_error_handler(func):
    """
    A decorator to handle errors in asynchronous functions, with a limit on the number of retries.
    """
    @wraps(func)
    async def with_error_handling(*args, **kwargs): 
        error_count = 0 
        while error_count < constants.ERROR_LIMIT:
            try:
                returned_value = await func(*args, **kwargs)
                return returned_value
            except Exception as e:
                print("Error in function " + func.__name__ + ": " + str(e))
                error_count += 1
        print("Error limit reached in function " + func.__name__)
        return None
    return with_error_handling
