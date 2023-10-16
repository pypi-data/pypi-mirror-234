from tenacity import (Retrying,
                      RetryCallState,
                      retry_if_result,
                      stop_after_delay
                      )
from tenacity.wait import wait_base
import time
import random
import logging

logger = logging.getLogger(__name__)

class wait_random_plus_long_pauses(wait_base):
    """Wait strategy that retries every base_wait_time_second + random.uniform(0, wait_time_jitter_second).
    And every longer_pause_after does a longer pause of random.uniform(0, longer_pause_max_duration_second)*60
    """
    def __init__(self, base_wait_time_second: int, 
                       wait_time_jitter_second: float, 
                       longer_pause_after_second: int = None,
                       longer_pause_max_duration_second: int = None) -> None:
        if (not longer_pause_after_second) ^ (not longer_pause_max_duration_second):
            raise ValueError("longer_pause_after_second is set but longer_pause_max_duration_second is not set")
        
        self.base_wait_time_second = base_wait_time_second
        self.wait_time_jitter_second = wait_time_jitter_second
        self.longer_pause_after_second = longer_pause_after_second
        self.longer_pause_max_duration_second = longer_pause_max_duration_second
        self.n_longer_pause = 1

    def __call__(self, retry_state: RetryCallState) -> float:
        wait_time = self.base_wait_time_second + random.uniform(0, self.wait_time_jitter_second)
        elapsed_time = time.monotonic() - retry_state.start_time
        if self.longer_pause_after_second and \
            (elapsed_time - (self.n_longer_pause*self.longer_pause_after_second)) > 0:
            wait_time = random.uniform(0, self.longer_pause_max_duration_second)
            logger.info(f'Taking a longer break. Elapsed time: {elapsed_time}. This is the {self.n_longer_pause}th longer break so far')
            self.n_longer_pause += 1
        logger.info(f'Will wait for {wait_time} seconds.')
        return wait_time
    
def get_available_station_search_retryer(base_wait_time_second: int, 
                                   wait_time_jitter_second: int, 
                                   expiration_time_second: int, 
                                   longer_pause_after_second: int, 
                                   longer_pause_max_duration_second: int) -> Retrying:
    retryer = Retrying(
        retry=retry_if_result(lambda x: len(x) == 0),
        wait=wait_random_plus_long_pauses(base_wait_time_second, wait_time_jitter_second, longer_pause_after_second, longer_pause_max_duration_second),
        stop=stop_after_delay(expiration_time_second),
        after=log_total_elapsed_time
    )
    return retryer

def log_total_elapsed_time(retry_state):
    elapsed_time = time.monotonic() - retry_state.start_time
    logger.info(f'Total elapsed time: {elapsed_time:.2f} seconds')

def available_station_search_test(success_proba=0.05):
    stations_whithin_radius = []
    if random.uniform(0, 1) > 1 - success_proba:
        stations_whithin_radius.append(1)
    return stations_whithin_radius


