import logging
import warnings
import functools
import time
from typing import Callable

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def retry_on_error(
    max_retries: int = 3,
    delay: int = 1,
):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(e)
                    attempts += 1
                    if attempts < max_retries:
                        logging.info(f'Retrying in {delay} seconds...')
                        time.sleep(delay)
                    else:
                        logging.info('Maximum retries reached.')
                        raise
        return wrapper_retry
    return decorator_retry
