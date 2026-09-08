import time
import threading
from collections import deque

class TokenBucket:
    """Thread-safe high-throughput Token Bucket rate limiter."""
    def __init__(self, capacity, refill_rate):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = float(refill_rate)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def consume(self, tokens=1):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def time_until_available(self, tokens=1):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            current_tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            if current_tokens >= tokens:
                return 0.0
            deficit = tokens - current_tokens
            return deficit / self.refill_rate


class LeakyBucket:
    """Leaky bucket rate limiter enforcing a constant outbound processing rate."""
    def __init__(self, capacity, leak_rate):
        self.capacity = int(capacity)
        self.leak_rate = float(leak_rate) # units per second
        self.water = 0.0
        self.last_leak = time.monotonic()
        self.lock = threading.Lock()

    def push(self, volume=1):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_leak
            self.water = max(0.0, self.water - elapsed * self.leak_rate)
            self.last_leak = now
            if self.water + volume <= self.capacity:
                self.water += volume
                return True
            return False


class SlidingWindowRateLimiter:
    """Sliding log rate limiter for strict precision over rolling time windows."""
    def __init__(self, limit, window_seconds=1.0):
        self.limit = limit
        self.window = window_seconds
        self.timestamps = deque()
        self.lock = threading.Lock()

    def allow_request(self):
        with self.lock:
            now = time.monotonic()
            cutoff = now - self.window
            while self.timestamps and self.timestamps[0] <= cutoff:
                self.timestamps.popleft()
            if len(self.timestamps) < self.limit:
                self.timestamps.append(now)
                return True
            return False
