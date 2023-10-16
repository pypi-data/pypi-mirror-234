# emacs mycoding: utf-8
# type: ignore
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

import asyncio
from .List import Iterator
from typing import Optional, Any, TYPE_CHECKING, Union, Dict
from itertools import islice, dropwhile, tee
from collections import deque
import asyncio
from .msg import msg

if TYPE_CHECKING:
    from .List import List
    from .Item import Item
from .await_async import _await_async
import inspect


class Slice:
    _callbacks: callable = []

    def __init__(
        self,
        of_list: "List",
        localdb: dict,
        start_item: Optional["Item"],
        size: int,
        search_term: Optional[Union[str, float, "Item"]],
        search_field: Optional[str],
        internal: bool = False,
    ):
        if not internal:
            msg._tell_dev(msg.M519_called_class_constructor, {})
        self.of_list = of_list
        self._localdb = localdb
        self.start_item = start_item
        self.slice_size = size
        self.search_field = search_field or "name"
        self.search_term = search_term
        self.sliced_list = self._slice_list()
        self.filtered_sliced_list = self._filter_list()
        self._MAX_ITEM_WITHOUT_PAGING = 1024

    def _slice_list(self):
        iterator = self.of_list.__iter__()
        if self.start_item is None:
            self.start_item = list(self.of_list)[0]
            if self.slice_size > 0:
                return islice(iterator._of_List, 0, self.slice_size)
            else:
                last_items = deque(maxlen=abs(self.slice_size))
                for item in iterator._of_List:
                    last_items.append(item)
                return last_items
        else:
            new_list = dropwhile(
                lambda x: x != self.start_item, iterator._of_List)
            return islice(new_list, 0, self.slice_size)

    def _filter_list(self):
        if self.search_term is None:
            return self.sliced_list
        else:
            return (
                item
                for item in self.sliced_list
                if item[self.search_field] == self.search_term
            )

    def __iter__(self) -> Union[islice, deque]:
        return self.filtered_sliced_list

    def forward(self, steps: Optional[int] = 1) -> None:
        list_iterator = self.of_list.__iter__()
        of_List_size = list_iterator._of_List.__len__()
        if steps < of_List_size:
            # get index of start_item from original list
            for i, item in enumerate(list_iterator._of_List):
                if item == self.start_item:
                    start_item_indx = i
                    break
            if steps > 0:
                new_start_item_indx = start_item_indx + steps
                # If next item is not in list, return the last (slice_size} items
                if new_start_item_indx < of_List_size:
                    self.sliced_list = islice(
                        list_iterator._of_List,
                        new_start_item_indx,
                        new_start_item_indx + self.slice_size,
                    )
                    self.start_item = list(self.of_list)[new_start_item_indx]
                else:
                    last_items = deque(maxlen=abs(self.slice_size))
                    for item in list_iterator._of_List:
                        last_items.append(item)
                    self.sliced_list = last_items.__iter__()
                    self.start_item = list(self.of_list)[of_List_size - steps]
            self.filtered_sliced_list = self._filter_list()
        else:
            # last_items = deque(maxlen=abs(self.slice_size))
            # for item in list_iterator._of_List:
            #     last_items.append(item)
            # self.sliced_list = last_items
            raise Exception(
                f"Number of steps exceded list size of {list_iterator._of_List.__len__()}")

    def set_search(self, search_term: Union[str, int], search_field: Optional[str] = None) -> None:
        # TODO search_term type should match type of search_field items
        if search_field is not None:
            self.search_field = search_field
        self.filtered_sliced_list = (
            item for item in self.sliced_list if item[self.search_field] == search_term)

    def reset_search(self) -> None:
        self.search_field = "name"
        self.search_term = None
        self.filtered_sliced_list = self.sliced_list

    def on_update(self, call_back: callable) -> None:
        self._callbacks.append(call_back)

    @classmethod
    async def _updated(cls, newItem: "Item") -> None:
        callbacks = cls._callbacks
        if not callbacks:
            return
        for func in callbacks:
            task = asyncio.create_task(cls._call_callback(func, newItem))
            await asyncio.gather(task)

    @staticmethod
    async def _call_callback(func: callable, newItem: "Item") -> None:
        result = func(newItem)
        # If the call back was defined async, then await it.
        if inspect.isawaitable(result):
            await result

    def count(self) -> int:
        return self.slice_size

    def set_size(self, new_size: int) -> None:
        if new_size > 0:
            self.slice_size = new_size
            self.sliced_list = self._slice_list()
            self.filtered_sliced_list = self._filter_list()

    def backward(self, steps: Optional[int] = 1) -> None:
        list_iterator = self.of_list.__iter__()
        if steps < list_iterator._of_List.__len__():
            # find start_item index in org list
            for i, item in enumerate(list_iterator._of_List):
                if item == self.start_item:
                    start_item_indx = i
                    break
            if steps > 0:
                new_item_index = start_item_indx - steps
                if new_item_index > 0:
                    # get new starting item index
                    first_s_lst_itm = list(self.of_list)[new_item_index]
                    self.start_item = first_s_lst_itm
                    self.sliced_list = islice(
                        list_iterator._of_List, new_item_index, self.slice_size + new_item_index)
                else:
                    self.start_item = list(self.of_list)[0]
                    self.sliced_list = islice(
                        list_iterator._of_List, 0, self.slice_size)
            self.filtered_sliced_list = self._filter_list()
        else:
            raise Exception(
                f"Number of steps exceded list size of {list_iterator._of_List.__len__()}")
        
    def first(self) -> "Optional[Item]":
        return self.start_item
    
    