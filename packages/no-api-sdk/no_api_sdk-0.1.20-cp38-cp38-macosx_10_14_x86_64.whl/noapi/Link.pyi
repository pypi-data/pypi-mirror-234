import logging
from . import Field as Field, GetResult as GetResult, PropertyValue as PropertyValue
from .Item import Item as Item
from .List import List as List
from .msg import msg as msg
from typing import Any, Dict, Optional

console = logging

class Link:
    def __init__(self, localdb: Dict, of_item: Item, relation: str, internal: bool = ...) -> None: ...
    def on_update(self, f: Any) -> None: ...
    def __iter__(self) -> None: ...
    def recall(self) -> Optional[Item]: ...
