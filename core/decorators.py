import functools
import time
import logging

# Configure enterprise-grade logging
logger = logging.getLogger("EnterpriseCore")

def optimized_execution(retries=3, backoff_factor=0.5):
    """
    Decorator to ensure function execution resilience with exponential backoff.
    Used for critical microservice communication.
    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            x = 0
            while x < retries:
                try:
                    start_time = time.perf_counter()
                    value = func(*args, **kwargs)
                    end_time = time.perf_counter()
                    logger.debug(f"Execution time: {end_time - start_time:.4f}s")
                    return value
                except Exception as e:
                    sleep_time = backoff_factor * (2 ** x)
                    time.sleep(sleep_time)
                    x += 1
            return None
        return wrapper_retry
    return decorator_retry
