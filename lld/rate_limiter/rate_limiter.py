'''
How it works:
Token Generation: Tokens are added to the bucket at a fixed rate. This rate defines the long-term average rate at which operations are allowed. 

Bucket Capacity: The bucket has a maximum capacity, meaning it can only hold a finite number of tokens. If tokens are added when the bucket is full, the excess tokens are discarded. This capacity determines the system's ability to handle bursts of requests. 

Token Consumption: When an operation or request arrives, it attempts to consume a token from the bucket.

If a token is available, the request is allowed, and a token is removed from the bucket.
If the bucket is empty, the request is either rejected immediately or delayed until a token becomes available.

Classes:

RateLimiter — public API
TokenBucket — bucket with tokens + refill logic
'''
import time
from threading import Lock, Thread


class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refilled = time.time()
        self.lock = Lock()  # Lock to protect bucket operations

    def refill(self):
        curr_date = time.time()
        time_since_lastt_refill = curr_date - self.last_refilled
        tokens_to_add = time_since_lastt_refill * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refilled = curr_date

    def allow_request(self):
        with self.lock:  # acquire before modifying shared state        
            self.refill() # no need to hold lock while checking tokens — each bucket has its own lock
            if self.tokens > 0:
                self.tokens -= 1
                return True
            return False


class RateLimiter:
    def __init__(self, user_capacity, user_refill_rate):
        self.user_capacity = user_capacity
        self.user_refill_rate = user_refill_rate
        self.buckets = {}
        self.lock = Lock()

    def is_allowed(self, user_id):
        with self.lock: # avoid race creating multiple buckets
            if user_id not in self.buckets:
                self.buckets[user_id] = TokenBucket(
                    self.user_capacity, self.user_refill_rate)
        # no need to hold lock while checking tokens — each bucket has its own lock
        return self.buckets[user_id].allow_request()


if __name__ == "__main__":
    # 5 requests, refill 1/sec
    rl = RateLimiter(user_capacity=5, user_refill_rate=1)

    user = "anna"

    '''
    for i in range(10):
        allowed = rl.is_allowed(user)
        print(f"Request {i}: {'allowed' if allowed else 'blocked'}")
        time.sleep(0.2)
    '''

    global_count = 0
    lock = Lock()
    threads = []

    def make_request(user):
        with lock:        
            if rl.is_allowed(user):        # avoid race updating global_count
                global global_count
                global_count +=1


    for _ in range(20):
        t = Thread(target=make_request, args=(user,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Global count: {global_count}")
