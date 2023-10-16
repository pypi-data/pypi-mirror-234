from __future__ import annotations
from typing import TypeAlias, Any


MessageContentSimpleType: TypeAlias = int | float | str | bool
MessageContentType: TypeAlias = MessageContentSimpleType | bytes | list["MessageContentType"] | dict[MessageContentSimpleType, "MessageContentType"]
MessageContentBaseType: Any = (int, float, str, bool, bytes, list, dict)
