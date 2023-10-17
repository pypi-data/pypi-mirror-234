# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from functools import wraps
from typing import (
    Any,
    Callable,
)

_REGISTRY = {}


def global_value(key: str) -> Callable:
    """
    Add values to a global registry. If the
    `key` already exists in the registry, the
    stored value is returned.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def customized_decorator() -> Any:
            try:
                value = _REGISTRY[key]
            except KeyError:
                value = func()
                _REGISTRY[key] = value

            return value

        return customized_decorator

    return decorator


def invalidate_global_value(*keys: str):
    """
    Remove the globally registered values, if they exist.
    """
    for key in keys:
        if key in _REGISTRY:
            del _REGISTRY[key]
