import json

from typing import Dict, Optional

from cffi import FFI

from .lib.node import *
from .lib.clib import clib


ffi = FFI()


def initialize(
        variable_values: Dict,
        fallback_init_data: Optional[Dict],
        token: Optional[str],
        query_code: str,
        query: Dict,
        language: str, 
        endpoints: str,
    ) -> NodeProps:
    return NodeProps(clib.initialize(
        ffi.new("char[]", json.dumps(variable_values).encode()),
        ffi.new("char[]", json.dumps(fallback_init_data).encode()) if fallback_init_data else ffi.NULL,
        ffi.new("char[]", json.dumps(token).encode()) if token else ffi.new("char[]", ffi.NULL),
        ffi.new("char[]", query_code.encode()),
        ffi.new("char[]", json.dumps(query).encode()),
        ffi.new("char[]", language.encode()),
        ffi.new("char[]", endpoints.encode()),
    ))
