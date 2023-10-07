# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import typing as T
import sys

from blessed import Terminal

from .item import T_ITEM
from .line_editor import LineEditor
from .dropdown import Dropdown


class Render:
    """
    Generic console render.
    """

    def __init__(self):
        # blessed terminal
        self.terminal = Terminal()

        # _line_number stores the current line number position of the cursor
        # if 0, means it is at the first line
        # if 1, means it is at the second line
        self._line_number = 0

    def print_str(
        self,
        str_tpl: str,
        new_line=False,
        **kwargs,
    ) -> str:
        """
        打印一个字符串, 可以选择是否换行.

        :param str_tpl: string template, 一个字符串模板.
        :param new_line: 如果是 True, 那么会自动换行, 否则不会. 默认不会.
        :param kwargs: 额外的传递给 str_tpl 的参数.
        """
        if new_line:
            self._line_number += 1
        content = str_tpl.format(**kwargs)
        print(content, end="\n" if new_line else "")
        sys.stdout.flush()
        return content

    def print_line(
        self,
        str_tpl: str,
        new_line: bool = True,
        **kwargs,
    ) -> str:
        """
        打印一行, 默认自动换行.

        :param str_tpl: string template, 一个字符串模板.
        :param new_line: 如果是 True, 那么会自动换行, 否则不会. 默认自动换行.
        :param kwargs: 额外的传递给 str_tpl 的参数.
        """
        return self.print_str(
            str_tpl + self.terminal.clear_eol(),
            new_line=new_line,
            **kwargs,
        )

    def _force_initial_column(self) -> str:
        """
        用回车符 (注意! 不是换行符) 把光标移动到本行初始位置.
        """
        return self.print_str("\r")

    def move_to_start(self) -> int:
        """
        把光标移动到初始位置. 本质上是把光标向上回退移动到第一行, 然后再用回车符把光标移动到本行初始位置.
        """
        n = self._line_number
        print(n * self.terminal.move_up, end="")
        print("\r", end="")
        sys.stdout.flush()
        self._line_number = 0
        return n

    def move_down(self, n: int):
        """
        把光标移动到初始位置. 本质上是把光标向上回退移动到第一行, 然后再用回车符把光标移动到本行初始位置.
        """
        print(n * self.terminal.move_down, end="")
        sys.stdout.flush()
        self._line_number += n

    def clear_n_lines(self, n: int):
        """
        把光标以上的 n 行清空, 并把光标移动到行首. 常用于清除掉已经打印过的内容.
        """
        if n > self._line_number:
            raise ValueError
        for _ in range(n):
            print(self.terminal.move_up, end="")
            print(self.terminal.clear_eol(), end="")
        self._force_initial_column()
        self._line_number -= n

    def clear_all(self):
        """
        清除所有内容, 并把光标移动到行首.
        """
        self.clear_n_lines(n=self._line_number)

    @property
    def width(self):
        return self.terminal.width or 80

    @property
    def height(self):
        return self.terminal.width or 24


class UIRender(Render):
    """
    The UI Render.

    See below example: ``|`` represents the cursor.

    .. code-block::

        [Query]: user query here|
        [x] item 1 title here
              item 1 subtitle here
        [ ] item 2 title here
              item 2 subtitle here
        [ ] item 3 title here
              item 3 subtitle here

    The first line ``[Query]: user query here|`` is the user input box, it always
    starts with ``[Query]: ``, and user can enter any text input after that.
    The cursor cannot go beyond the ``: `` part.

    User can use ``Left``, ``Right``, ``Backspace`` and ``Delete`` keys to edit the
    user input box.

    Below the first line is the items drop down menu. Each item has two lines.

    The first line is the title, it always starts with ``[x] `` or ``[ ] ``.
    ``[x] `` means the item is selected, ``[ ] `` means the item is not selected.
    You can only select one item at a time, and by default the first item is selected.
    There always be one item selected.

    The second line is the subtitle, it has 2 indent spaces comparing to the title.

    User can use the ``UP`` and ``DOWN`` keys to navigate the items drop down menu.

    The dropdown menu can show up to 10 items at a time, if the dropdown menu
    has more than 10 items, user can scroll down to see the rest of the items using
    the ``DOWN`` key. The ``CTRL + UP`` and ``CTRL + DOWN`` key can scroll up and down
    10 items at a time.
    """
    def print_line_editor(self, line_editor: LineEditor) -> str:
        """
        Render the line editor, the ``[Query]: user query here|`` part.
        """
        return self.print_line(
            "{t.bold}{t.cyan}[Query]: {t.normal}{line_editor.line}",
            line_editor=line_editor,
            t=self.terminal,
        )

    def _process_title(self, title: str, line_width: int):
        space = line_width - 4 - 1
        if len(title) > space:
            half = (space - 3) // 2
            return title[:half] + "..." + title[-half:]
        else:
            return title

    def _process_subtitle(self, subtitle: str, line_width: int):
        space = line_width - 6 - 1
        if len(subtitle) > space:
            half = (space - 3) // 2
            return subtitle[:half] + "..." + subtitle[-half:]
        else:
            return subtitle

    def print_item(self, item: T_ITEM, selected: bool, line_width: int):
        if selected:
            color = self.terminal.cyan
            symbol = "[x]"
        else:
            color = self.terminal.normal
            symbol = "[ ]"

        self.print_line(
            "{t.bold}{color}{symbol} {color}{title}{t.normal}",
            color=color,
            symbol=symbol,
            title=self._process_title(item.title_text, line_width),
            t=self.terminal,
        )
        self.print_line(
            "{pad}{t.normal}{subtitle}",
            pad=" " * 6,
            subtitle=self._process_subtitle(item.subtitle_text, line_width),
            t=self.terminal,
        )

    def print_dropdown(self, dropdown: Dropdown, line_width: int) -> int:
        """
        Render the dropdown menu, it looks like::

            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here
        """
        menu = dropdown.menu
        for item, selected in dropdown.menu:
            self.print_item(item, selected=selected, line_width=line_width)
        n_item = len(menu)
        return n_item

    def move_cursor_to_line_editor(self, line_editor: LineEditor) -> T.Tuple[int, int]:
        """
        After the :meth:`Dropdown.print_dropdown` is called, the cursor is at the
        end of the UI. This method moves the cursor back to the user input box,
        so user can keep typing.

        ::

            [Query]: user query here| <- want to move to here
            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here
            | <- cursor is currently here

        :return: n_vertical is the number of line to move up, n_horizontal is
            the number of character to move right.
        """
        n_vertical = self.move_to_start()
        n_horizontal = 9 + line_editor.cursor_position
        self.print_str(self.terminal.move_right(n_horizontal), end="")
        return n_vertical, n_horizontal

    def print_ui(self, line_editor: LineEditor, dropdown: Dropdown) -> int:
        """
        Render the entire UI, and move the cursor to the right position.
        """
        self.print_line_editor(line_editor)
        n_items = self.print_dropdown(dropdown, line_width=self.terminal.width)
        self.move_cursor_to_line_editor(line_editor)
        return n_items

    def move_to_end(self, n_items: int):
        """
        Move the cursor to the end, this method will be used before exit.
        """
        move_down_n_lines = n_items * 2 + 1 - self._line_number
        self.print_str(move_down_n_lines * self.terminal.move_down, end="")
        self._line_number += move_down_n_lines
