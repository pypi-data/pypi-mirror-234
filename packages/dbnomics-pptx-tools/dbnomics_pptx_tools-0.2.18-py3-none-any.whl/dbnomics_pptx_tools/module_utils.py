from collections.abc import Callable
from importlib import import_module
from typing import Any

import daiquiri
from parsy import regex, seq, string

logger = daiquiri.getLogger(__name__)


def load_function_from_module(function_name: str, *, module_name: str) -> Callable[..., Any] | None:
    module = import_module(module_name)
    return getattr(module, function_name, None)


def parse_callable(callable_ref: str) -> Callable[..., Any] | None:
    module_name = regex(r"(\w|\.)+").desc("module name")
    function_name = regex(r"(\w|\.)+").desc("function name")
    parser = seq(module_name << string(":"), function_name)
    module_name, function_name = parser.parse(callable_ref)
    return load_function_from_module(function_name, module_name=module_name)
