import json

from enum import IntEnum
from typing import Any, Dict, Optional
from cffi import FFI

ffi = FFI()

from .clib import clib

NodeHandle = int

def get_string(sized_string) -> Optional[str]:
    if sized_string.length == 0:
        return None
    return bytes(sized_string.bytes[0:sized_string.length]).decode()

class NodePropsType(IntEnum):
    STRING = 0
    ENUM = 1
    INT = 2
    FLOAT = 3
    BOOL = 4
    OBJECT = 5
    VOID = 6
    UNKNOWN = 7

class NodeIteratorState(IntEnum):
    MAYBE_MORE = 0
    CONSUMED = 1

class NodeProps:
    handle: NodeHandle
    value: Optional[Any]
    object_type_name: Optional[str]
    type: NodePropsType

    def __init__(self, node_result):
        self.handle = node_result.id
        self.type = node_result.type

        value_string = get_string(node_result.value)
        if value_string is None:
            self.value = None
        else:
            self.value = json.loads(value_string)
        
        self.object_type_name = get_string(node_result.object_type_name)

class NodePropsIterable:
    def __init__(self, iterator_result):
        self.handle = iterator_result.id

    def __iter__(self):
        return self
    
    def __next__(self) -> NodeProps:
        next_result = clib.node_iterator_next(self.handle)
        if next_result.state == NodeIteratorState.CONSUMED:
            raise StopIteration()
        
        return NodeProps(next_result.node)

class Node:
    def __init__(self, props: NodeProps):
        self._props = props

    def _get_field(self, field: str, arguments: Dict[str, Any]) -> NodeProps:
        arguments_json = json.dumps(arguments)
        return NodeProps(clib.node_get_field(
            self._props.handle, field.encode(), arguments_json.encode()
        ))

    def _get_items(self, list_fallback_length) -> NodePropsIterable:
        return NodePropsIterable(clib.node_get_items(self._props.handle))

    def _evaluate(self) -> Optional[Any]:
        value_string = get_string(clib.node_evaluate(self._props.handle))
        if value_string is None:
            return None
        
        return json.loads(value_string)

    def _log_unexpected_type_error(self):
        pass

    def _log_unexpected_value_error(self, value):
        pass

class VoidNode(Node):
    def get(self) -> None:
        result = self._evaluate()
        if not isinstance(result, bool):
            if result == True:
                return
        
        self._log_unexpected_value_error(result)


class BooleanNode(Node):
    def get(self, fallback: bool) -> bool:
        result = self._evaluate()
        if not isinstance(result, bool):
            self._log_unexpected_value_error(result)
            return fallback
        
        return result

class IntNode(Node):
    def get(self, fallback: int) -> int:
        result = self._evaluate()
        if not isinstance(result, int):
            self._log_unexpected_value_error(result)
            return fallback

        return result

class FloatNode(Node):
    def get(self, fallback: float) -> float:
        result = self._evaluate()
        if not isinstance(result, float) or not isinstance(result, int):
            self._log_unexpected_value_error(result)
            return fallback
        
        return float(result)

class StringNode(Node):
    def get(self, fallback: str) -> str:
        result = self._evaluate()
        if not isinstance(result, str):
            self._log_unexpected_value_error(result)
            return fallback

        return result