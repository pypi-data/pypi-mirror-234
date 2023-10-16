from ratelimit import limits, sleep_and_retry, RateLimitException
import backoff
from decorator_composer import merge_decorators

avoid_ddos=merge_decorators(
        sleep_and_retry,
        limits(calls=15, period=30),
        backoff.on_exception(backoff.expo, RateLimitException))    
    
