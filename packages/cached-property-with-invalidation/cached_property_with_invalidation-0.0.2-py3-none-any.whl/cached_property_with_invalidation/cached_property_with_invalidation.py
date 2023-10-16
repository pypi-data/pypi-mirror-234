from typing import Optional


def cached_property_with_invalidation(
    invalidation_variable_name: str,
    verbose: bool = False,
    maxsize: Optional[int] = 1,
):
    """Decorator to create cached_property that can be invalidated when invalidation variable is updated

    Args:
        invalidation_variable_name (str): instance variable name that will be used to invalidate the cached_property if updated to new value
        verbose (bool): whether to print out when recomputing or using cache
        maxsize (Optional[int]): maximum number of invalidation variable values to store in cache. If None, then no limit.
    """

    assert (
        maxsize is None or maxsize == 1
    ), "maxsize must be None or 1. TODO: implement maxsize > 1 with LRU cache"

    def decorator(property_method):
        # Dict of dicts to store cache
        # First key: property name
        # Second key: invalidation variable value
        CACHE_DICT_NAME = "_cached_property_with_invalidation_dict"

        @property
        def wrapped_method(self):
            property_name = property_method.__name__

            assert hasattr(
                self, invalidation_variable_name
            ), f"Instance variable {invalidation_variable_name} does not exist"
            invalidation_variable = getattr(self, invalidation_variable_name)

            if not hasattr(self, CACHE_DICT_NAME):
                setattr(self, CACHE_DICT_NAME, {})
            cache_dict = getattr(self, CACHE_DICT_NAME)

            if not property_name in cache_dict:
                cache_dict[property_name] = {}

            if invalidation_variable not in cache_dict[property_name]:
                if verbose:
                    print(f"Recomputing for {property_name}")

                # Update cache
                new_value = property_method(self)

                if maxsize == 1:
                    cache_dict[property_name] = {}
                    cache_dict[property_name][invalidation_variable] = new_value
                elif maxsize is None:
                    cache_dict[property_name][invalidation_variable] = new_value
                else:
                    raise NotImplementedError(
                        "TODO: implement maxsize > 1 with LRU cache"
                    )
                return new_value
            else:
                if verbose:
                    print(f"Using cache for {property_name}")

                # Use cache
                return cache_dict[property_name][invalidation_variable]

        return wrapped_method

    return decorator
