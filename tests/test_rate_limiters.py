import unittest
import time
from token_bucket import TokenBucket, LeakyBucket, SlidingWindowRateLimiter

class TestRateLimiters(unittest.TestCase):
    def test_token_bucket_burst_and_refill(self):
        tb = TokenBucket(capacity=5, refill_rate=10) # 10 tokens/sec
        self.assertTrue(tb.consume(5))
        self.assertFalse(tb.consume(1))
        time.sleep(0.2) # should refill ~2 tokens
        self.assertTrue(tb.consume(1))

    def test_leaky_bucket_drain(self):
        lb = LeakyBucket(capacity=4, leak_rate=10)
        self.assertTrue(lb.push(4))
        self.assertFalse(lb.push(1))
        time.sleep(0.25)
        self.assertTrue(lb.push(2))

    def test_sliding_window_precision(self):
        limiter = SlidingWindowRateLimiter(limit=3, window_seconds=0.2)
        self.assertTrue(limiter.allow_request())
        self.assertTrue(limiter.allow_request())
        self.assertTrue(limiter.allow_request())
        self.assertFalse(limiter.allow_request())
        time.sleep(0.25)
        self.assertTrue(limiter.allow_request())

if __name__ == '__main__':
    unittest.main()
