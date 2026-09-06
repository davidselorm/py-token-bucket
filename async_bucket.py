import asyncio
import time

class AsyncTokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = float(refill_rate)
        self.last_refill = time.monotonic()
    async def acquire(self, tokens=1):
        while True:
            now = time.monotonic()
            self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.refill_rate)
            self.last_refill = now
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            await asyncio.sleep(0.01)
