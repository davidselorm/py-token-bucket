import asyncio
import time

class AsyncTokenBucket:
    """Non-blocking asynchronous token bucket with precise sleep scheduling."""
    def __init__(self, capacity, refill_rate):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = float(refill_rate)
        self.last_refill = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens=1):
        while True:
            async with self.lock:
                now = time.monotonic()
                elapsed = now - self.last_refill
                self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
                self.last_refill = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True
                deficit = tokens - self.tokens
                wait_time = deficit / self.refill_rate

            await asyncio.sleep(min(max(wait_time, 0.001), 1.0))
