# cached_property_with_invalidation

Decorator to create cached_property that can be invalidated when invalidation variable is updated

# Installing

Install:
```
pip install cached_property_with_invalidation
```

# Usage

Example usage comparing:

1. `cached_property_with_invalidation`

2. `cached_property`

3. `property`

This example demonstrates a common use case in which we have a slow computation that we want to cache temporarily, but we need to invalidate the cache when the class state updates. If we simply use `property`, no caching will be done, which hurts performance. If we simply use `cached_property`, caching will be done, but we will get incorrect values when the class state updates. In contrast, using `cached_property_with_invalidation` allows us to correctly compute the right values when the class state updates, but caches the value when it has not been updated.

This is a very common use-case in physics-based simulation, where we have a simulation physics state that is updated on each simulation step, and we have expensive computations on that physics state we want to cache.

```
from cached_property_with_invalidation import (
    cached_property_with_invalidation,
)
import time


try:
    from functools import cached_property
except ImportError:
    from functools import lru_cache

    def cached_property(func):
        @property
        @lru_cache()
        def wrapped_method(self):
            return func(self)

        return wrapped_method


SLOW_FUNCTION_TIME_MIN_SECONDS = 0.1
CACHE_ACCESS_TIME_MAX_SECONDS = 0.01
INVALIDATION_VARIABLE_NAME = "counter"


class ExampleClass:
    def __init__(self):
        self.counter = 0
        self.internal_state = [i for i in range(10)]

    def update_state(self):
        self.counter += 1
        self.internal_state = [i + 1 for i in self.internal_state]

    def slow_double_internal_state(self):
        time.sleep(SLOW_FUNCTION_TIME_MIN_SECONDS)
        return [i * 2 for i in self.internal_state]

    @cached_property_with_invalidation(INVALIDATION_VARIABLE_NAME)
    def slow_double_internal_state_with_cache_and_invalidation(self):
        return self.slow_double_internal_state()

    @cached_property
    def slow_double_internal_state_with_cache_no_invalidation(self):
        return self.slow_double_internal_state()

    @property
    def slow_double_internal_state_no_cache(self):
        return self.slow_double_internal_state()


def test_with_cache_and_invalidation():
    # Correct behavior and fast
    example_class = ExampleClass()

    t0 = time.time()
    output0 = example_class.slow_double_internal_state_with_cache_and_invalidation
    t1 = time.time()
    cached_output0 = (
        example_class.slow_double_internal_state_with_cache_and_invalidation
    )
    t2 = time.time()

    example_class.update_state()
    t3 = time.time()
    output1 = example_class.slow_double_internal_state_with_cache_and_invalidation
    t4 = time.time()
    cached_output1 = (
        example_class.slow_double_internal_state_with_cache_and_invalidation
    )
    t5 = time.time()

    compute_output0_time = t1 - t0
    compute_cached_output0_time = t2 - t1
    compute_output1_time = t4 - t3
    compute_cached_output1_time = t5 - t4

    assert output0 == cached_output0
    assert output0 != output1
    assert output1 == cached_output1

    assert compute_output0_time > SLOW_FUNCTION_TIME_MIN_SECONDS
    assert compute_cached_output0_time < CACHE_ACCESS_TIME_MAX_SECONDS
    assert compute_output1_time > SLOW_FUNCTION_TIME_MIN_SECONDS
    assert compute_cached_output1_time < CACHE_ACCESS_TIME_MAX_SECONDS


def test_with_cache_no_invalidation():
    # Fast but incorrect behavior
    example_class = ExampleClass()

    t0 = time.time()
    output0 = example_class.slow_double_internal_state_with_cache_no_invalidation
    t1 = time.time()
    cached_output0 = example_class.slow_double_internal_state_with_cache_no_invalidation
    t2 = time.time()

    example_class.update_state()
    t3 = time.time()
    output1 = example_class.slow_double_internal_state_with_cache_no_invalidation
    t4 = time.time()
    cached_output1 = example_class.slow_double_internal_state_with_cache_no_invalidation
    t5 = time.time()

    compute_output0_time = t1 - t0
    compute_cached_output0_time = t2 - t1
    compute_output1_time = t4 - t3
    compute_cached_output1_time = t5 - t4

    assert output0 == cached_output0
    assert output0 == output1
    assert output1 == cached_output1

    assert compute_output0_time > SLOW_FUNCTION_TIME_MIN_SECONDS
    assert compute_cached_output0_time < CACHE_ACCESS_TIME_MAX_SECONDS
    assert compute_output1_time < CACHE_ACCESS_TIME_MAX_SECONDS
    assert compute_cached_output1_time < CACHE_ACCESS_TIME_MAX_SECONDS


def test_no_cache():
    # Correct behavior but slow
    example_class = ExampleClass()

    t0 = time.time()
    output0 = example_class.slow_double_internal_state_no_cache
    t1 = time.time()
    uncached_output0 = example_class.slow_double_internal_state_no_cache
    t2 = time.time()

    example_class.update_state()
    t3 = time.time()
    output1 = example_class.slow_double_internal_state_no_cache
    t4 = time.time()
    uncached_output1 = example_class.slow_double_internal_state_no_cache
    t5 = time.time()

    compute_output0_time = t1 - t0
    compute_uncached_output0_time = t2 - t1
    compute_output1_time = t4 - t3
    compute_uncached_output1_time = t5 - t4

    assert output0 == uncached_output0
    assert output0 != output1
    assert output1 == uncached_output1

    assert compute_output0_time > SLOW_FUNCTION_TIME_MIN_SECONDS
    assert compute_uncached_output0_time > SLOW_FUNCTION_TIME_MIN_SECONDS
    assert compute_output1_time > SLOW_FUNCTION_TIME_MIN_SECONDS
    assert compute_uncached_output1_time > SLOW_FUNCTION_TIME_MIN_SECONDS


test_with_cache_and_invalidation()
test_with_cache_no_invalidation()
test_no_cache()
```