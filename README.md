# py-token-bucket

A suite of thread-safe and asynchronous rate limiting algorithms in pure Python.

## Implementations
- **TokenBucket**: Burst-tolerant rate limiter with fractional token replenishment.
- **LeakyBucket**: Constant-rate traffic shaping for outbound requests.
- **SlidingWindowRateLimiter**: Rolling-window timestamp queue with zero boundary anomalies.
- **AsyncTokenBucket**: Non-blocking `asyncio` rate limiter with calculated deficit sleep.

## Running Tests
```bash
python -m unittest tests/test_rate_limiters.py
```
