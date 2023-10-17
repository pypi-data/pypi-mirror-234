# -*- coding: utf-8 -*-

"""

"""

import typing as T

from .constants import SHOW_ITEMS_LIMIT, SCROLL_SPEED
from .item import T_ITEM


class Dropdown:
    """
    Simulate a item dropdown menu. User can move cursor up and down and scroll
    up and down the list, hit enter to perform action on the selected item.

    :param items: All items in this dropdown menu. We only show ``SHOW_ITEMS_LIMIT``
        items in the UI at a time
    :param n_items: total number of items, it is a cache of ``len(items)``.
    :param selected_item_index: the selected item index, the value can be larger
        than ``SHOW_ITEMS_LIMIT`` if we have many items.
    :param cursor_position: the selected item cursor position in the dropdown UI,
        it is a value from 0 to ``SHOW_ITEMS_LIMIT - 1``.
    """

    def __init__(self, items: T.List[T_ITEM]):
        self.items: T.List[T_ITEM] = items
        self.n_items: int = len(items)
        self.selected_item_index: int = 0
        self.cursor_position: int = 0
        self._show_items_limit = min(SHOW_ITEMS_LIMIT, self.n_items)

    def update(self, items: T.List[T_ITEM]):
        self.items = items
        self.n_items = len(items)
        self.selected_item_index = 0
        self.cursor_position = 0
        self._show_items_limit = min(SHOW_ITEMS_LIMIT, self.n_items)

    @property
    def selected_item(self) -> T_ITEM:
        return self.items[self.selected_item_index]

    def _press_down(self):
        # already the last item
        if self.selected_item_index == self.n_items - 1:
            pass
        else:
            self.selected_item_index += 1
        # already the last item in the UI
        if self.cursor_position == self._show_items_limit - 1:
            pass
        else:
            self.cursor_position += 1

    def press_down(self, n: int = 1):
        if n >= (self.n_items - 1 - self.selected_item_index):
            self.selected_item_index = self.n_items - 1
            self.cursor_position = self._show_items_limit - 1
            return
        for _ in range(n):
            self._press_down()

    def _press_up(self):
        if self.selected_item_index == 0:
            pass
        else:
            self.selected_item_index -= 1
        if self.cursor_position == 0:
            pass
        else:
            self.cursor_position -= 1

    def press_up(self, n: int = 1):
        if n >= self.selected_item_index:
            self.selected_item_index = 0
            self.cursor_position = 0
            return
        for _ in range(n):
            self._press_up()

    def scroll_down(self, n: int = 1):
        self.press_down(n * SCROLL_SPEED)

    def scroll_up(self, n: int = 1):
        self.press_up(n * SCROLL_SPEED)

    @property
    def menu(self) -> T.List[T.Tuple[T_ITEM, bool]]:
        """
        Example: ``ali|ce`` -> line = alice
        """
        # print(self.selected_item_index)
        # print(self.cursor_position)
        lower_index = self.selected_item_index - self.cursor_position
        upper_index = self.selected_item_index + (
            self._show_items_limit - self.cursor_position
        )
        menu = list()
        for ind, item in enumerate(self.items[lower_index:upper_index]):
            if ind == self.cursor_position:
                menu.append((item, True))
            else:
                menu.append((item, False))
        return menu
