# Rate Limiter - Low Level Design Problem

## Problem Statement

Design and implement a **Token Bucket Rate Limiter** that can limit the number of requests a client can make within a time window. The system should be thread-safe and handle concurrent requests efficiently.

---

## Functional Requirements

1. **Rate Limiting Algorithm**: Implement Token Bucket algorithm
   - Each client has a bucket with a maximum capacity (max tokens)
   - Tokens are refilled at a constant rate (tokens per second)
   - Request consumes 1 token
   - Request is allowed if token is available, rejected otherwise

2. **API**
   - `isAllowed(clientId: str) -> bool`: Check if request should be allowed
   - Returns `True` if token available, `False` otherwise
   - Consumes token if available

3. **Configuration**
   - `capacity`: Maximum tokens in bucket
   - `refillRate`: Tokens added per second

---

## Example

```
capacity = 5 tokens
refillRate = 2 tokens/second

Initial: [●●●●●] (5 tokens)

Request 1: [●●●●○] → Allowed (now 4 tokens)
Request 2: [●●●○○] → Allowed (now 3 tokens)
Request 3: [●●○○○] → Allowed (now 2 tokens)
Request 4: [●○○○○] → Allowed (now 1 token)
Request 5: [○○○○○] → Allowed (now 0 tokens)
Request 6: [○○○○○] → Rejected (no tokens)

After 1 second: [●●○○○] (2 tokens refilled)
Request 7: [●○○○○] → Allowed (now 1 token)
```

---

## Non-Functional Requirements

1. **Thread Safety**: Handle concurrent requests from multiple threads
2. **Performance**: O(1) for `isAllowed()` operation
3. **Memory**: Store only necessary client data

---

## Design Constraints

1. Use appropriate data structures (HashMap for client buckets)
2. Handle time-based token refill correctly
3. Thread-safe implementation (use locks or atomic operations)

---

## Edge Cases

1. Multiple requests arrive simultaneously
2. Client makes rapid burst of requests
3. Long idle period (bucket fully refilled)
4. Client doesn't exist (create new bucket)
5. Token refill calculation (handle partial seconds)

---

## Expected Deliverables

1. **RateLimiter class** with `isAllowed()` method
2. **TokenBucket class** to manage tokens for a client
3. **Thread-safe implementation**
4. **Test cases** demonstrating:
   - Normal flow (allow/reject)
   - Token refill
   - Burst handling
   - Concurrent requests

---

## Success Criteria

- ✅ Correctly implements Token Bucket algorithm
- ✅ Thread-safe for concurrent access
- ✅ Handles token refill accurately
- ✅ Clean, maintainable code
- ✅ Works for multiple clients independently

---

**Time Limit**: ~45 minutes implementation + 15 minutes discussion

**Hints**: Consider using a timestamp to track last refill time, calculate tokens based on elapsed time.

