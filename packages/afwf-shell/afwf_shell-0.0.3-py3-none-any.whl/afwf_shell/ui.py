# -*- coding: utf-8 -*-

"""
Alfred Workflow UI simulator.
"""

import typing as T

import readchar

from . import exc
from . import events
from .item import T_ITEM, Item
from .line_editor import LineEditor
from .dropdown import Dropdown
from .render import UIRender
from .debug import debugger


key_to_name = {
    readchar.key.CTRL_C: "CTRL_C",
    readchar.key.TAB: "TAB",
    readchar.key.CTRL_X: "CTRL_X",
    readchar.key.UP: "UP",
    readchar.key.DOWN: "DOWN",
    readchar.key.CTRL_E: "CTRL_E",
    readchar.key.CTRL_D: "CTRL_D",
    readchar.key.CTRL_R: "CTRL_R",
    readchar.key.CTRL_F: "CTRL_F",
    readchar.key.LEFT: "LEFT",
    readchar.key.RIGHT: "RIGHT",
    readchar.key.HOME: "HOME",
    readchar.key.END: "END",
    readchar.key.CTRL_H: "CTRL_H",
    readchar.key.CTRL_L: "CTRL_L",
    readchar.key.CTRL_G: "CTRL_G",
    readchar.key.CTRL_K: "CTRL_K",
    readchar.key.BACKSPACE: "BACKSPACE",
    readchar.key.DELETE: "DELETE",
    readchar.key.ENTER: "ENTER",
    readchar.key.CR: "CR",
    readchar.key.LF: "LF",
    readchar.key.CTRL_A: "CTRL_A",
    readchar.key.CTRL_W: "CTRL_W",
    readchar.key.CTRL_P: "CTRL_P",
}


class UI:
    """
    Alfred Workflow UI simulator.

    :param handler: a callable function that takes a query string as input and
        returns a list of items.
    """

    def __init__(
        self,
        handler: T.Callable[[str, T.Optional["UI"]], T.List[T_ITEM]],
        capture_error: bool = True,
    ):
        self.handler: T.Callable[[str, T.Optional["UI"]], T.List[T_ITEM]] = handler
        self.render: UIRender = UIRender()
        self.event_generator = events.KeyEventGenerator()

        # --- items related ---
        self.line_editor: LineEditor = LineEditor()
        self.dropdown: Dropdown = Dropdown([])
        self.n_items_on_screen: int = 0

        # --- controller flags ---
        self.need_clear_query: bool = True
        self.need_clear_items: bool = True
        self.need_print_query: bool = True
        self.need_print_items: bool = True
        self.need_run_handler: bool = True
        self.need_process_input: bool = True
        self.need_move_to_end: bool = True

        self.capture_error: bool = capture_error

    def _clear_query(self):
        """
        Clear the ``[Query]: {user_query}`` line
        """
        if self.render._line_number == 1:
            self.render.clear_n_lines(n=1)
            debugger.log(f"cleared")
        else:
            debugger.log(f"nothing happen")

    def clear_query(self):
        """
        A wrapper of the ``_clear_query()`` method, ensures that the
        ``need_clear_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("--- clear_query ---")
        try:
            if self.need_clear_query:
                self._clear_query()
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_clear_query = True

    def _clear_items(self):
        """
        Clear the item dropdown menu.
        """
        if self.render._line_number > 1:
            self.render.clear_n_lines(n=self.render._line_number - 1)
            debugger.log(f"cleared")
        else:
            debugger.log(f"nothing happen")

    def clear_items(self):
        """
        A wrapper of the ``_clear_items()`` method, ensures that the
        ``need_clear_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("--- clear_items ---")
        try:
            if self.need_clear_items:
                self._clear_items()
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_clear_items = True

    def _print_query(self):
        """
        Print the ``[Query]: {user_query}`` line
        """
        content = self.render.print_line_editor(self.line_editor)
        debugger.log(f"printed: {content!r}")

    def print_query(self):
        """
        A wrapper of the core logic for printint query, ensures that the
        ``need_print_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("--- print_query ---")
        try:
            if self.need_print_query:
                self._print_query()
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_print_query = True

    def _print_items(self, items: T.Optional[T.List[T_ITEM]] = None):
        """
        Core logic for printing items in the dropdown menu.

        :param items: normally, this argument should be None, we will call the
            handler function to get the items. If this is given, we will skip
            the handler call.
        """
        if self.need_run_handler:
            debugger.log("need to run handler")
            if items is None:
                debugger.log("run handler")
                items = self.handler(self.line_editor.line, self)
            else:
                debugger.log("explicitly give items, skip handler")
            self.dropdown.update(items)

            # the current terminal height may not be able to fit all items
            # so we may need to update the ``self.dropdown._show_items_limit``
            # to fit the terminal height
            terminal_height = self.render.terminal.height
            if terminal_height <= 9:
                raise exc.TerminalTooSmallError(
                    "Terminal height is too small to render the UI! "
                    "It has to have at least 8 lines."
                )
            terminal_items_limit = (terminal_height - 2) // 2
            self.dropdown._show_items_limit = min(
                self.dropdown._show_items_limit,
                terminal_items_limit,
            )

        terminal_width = self.render.terminal.width
        if terminal_width < 80:
            raise exc.TerminalTooSmallError(
                "Terminal width is too small to render the UI! "
                "It has to have at least 80 ascii character wide."
            )
        debugger.log("render dropdown")
        n_items_on_screen = self.render.print_dropdown(self.dropdown, terminal_width)
        self.n_items_on_screen = n_items_on_screen

    def print_items(self, items: T.Optional[T.List[T_ITEM]] = None):
        """
        A wrapper of the core logic for printint items, ensures that the
        ``need_print_items`` and ``need_run_handler`` flag is set to ``True``
        at the end regardless of whether an exception is raised.
        """
        debugger.log("--- print_items ---")
        try:
            if self.need_print_items:
                self._print_items(items=items)
        finally:
            debugger.log(f"move_cursor_to_line_editor ...")
            debugger.log(f"_line_number: {self.render._line_number}")
            n_vertical, n_horizontal = self.render.move_cursor_to_line_editor(
                self.line_editor
            )
            debugger.log(f"n_vertical: {n_vertical}")
            debugger.log(f"n_horizontal: {n_horizontal}")
            self.need_print_items = True
            self.need_run_handler = True

    def process_key_pressed_input(self, pressed: str):
        """
        Process user keyboard input.

        - UP: move up
        - DOWN: move down
        - LEFT: move left
        - RIGHT: move right
        - HOME: move to start of the line
        - END: move to end of the line

        - CTRL + E: move up
        - CTRL + D: move down
        - CTRL + R: scroll up
        - CTRL + F: scroll down
        - CTRL + H: move left
        - CTRL + L: move right
        - CTRL + G: move word left
        - CTRL + K: move word right

        - CTRL + X: clear input

        Actions:

        - Enter:
        - CTRL + A:
        - CTRL + W:
        - CTRL + P:
        """
        pressed_key_name = key_to_name.get(pressed, pressed)
        debugger.log(f"pressed: {pressed_key_name}")

        if pressed == readchar.key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed == readchar.key.TAB:
            self.line_editor.clear_line()
            selected_item = self.dropdown.selected_item
            if selected_item.autocomplete:
                self.line_editor.enter_text(selected_item.autocomplete)
            return

        if pressed == readchar.key.CTRL_X:
            self.line_editor.clear_line()
            return

        if pressed in (
            readchar.key.UP,
            readchar.key.DOWN,
            readchar.key.CTRL_E,
            readchar.key.CTRL_D,
            readchar.key.CTRL_R,
            readchar.key.CTRL_F,
        ):
            self.need_clear_query = False
            self.need_print_query = False
            self.need_run_handler = False

            if pressed in (readchar.key.UP, readchar.key.CTRL_E):
                self.dropdown.press_up()
            elif pressed in (readchar.key.DOWN, readchar.key.CTRL_D):
                self.dropdown.press_down()
            elif pressed == readchar.key.CTRL_R:
                self.dropdown.scroll_up()
            elif pressed == readchar.key.CTRL_F:
                self.dropdown.scroll_down()
            else:  # pragma: no cover
                raise NotImplementedError
            return

        if pressed in (
            readchar.key.LEFT,
            readchar.key.RIGHT,
            readchar.key.HOME,
            readchar.key.END,
            readchar.key.CTRL_H,
            readchar.key.CTRL_L,
            readchar.key.CTRL_G,
            readchar.key.CTRL_K,
        ):
            self.need_clear_query = False
            self.need_clear_items = False
            self.need_print_query = False
            self.need_print_items = False
            self.need_run_handler = False
            if pressed in (readchar.key.LEFT, readchar.key.CTRL_H):
                self.line_editor.press_left()
            elif pressed in (readchar.key.RIGHT, readchar.key.CTRL_L):
                self.line_editor.press_right()
            elif pressed == readchar.key.HOME:
                self.line_editor.press_home()
            elif pressed == readchar.key.END:
                self.line_editor.press_end()
            elif pressed == readchar.key.CTRL_G:
                self.line_editor.move_word_backward()
            elif pressed == readchar.key.CTRL_K:
                self.line_editor.move_word_forward()
            else:  # pragma: no cover
                raise NotImplementedError
            return

        if pressed == readchar.key.BACKSPACE:
            self.line_editor.press_backspace()
            return

        if pressed == readchar.key.DELETE:
            self.line_editor.press_delete()
            return

        if pressed in (
            readchar.key.ENTER,
            readchar.key.CR,
            readchar.key.LF,
            readchar.key.CTRL_A,
            readchar.key.CTRL_W,
            readchar.key.CTRL_P,
        ):
            if self.dropdown.n_items == 0:
                raise exc.EndOfInputError(
                    selection="select nothing",
                )
            else:
                self.move_to_end()
                selected_item = self.dropdown.selected_item
                if pressed in (
                    readchar.key.ENTER,
                    readchar.key.CR,
                    readchar.key.LF,
                ):
                    selected_item.enter_handler()
                elif pressed == readchar.key.CTRL_A:
                    selected_item.ctrl_a_handler()
                elif pressed == readchar.key.CTRL_W:
                    selected_item.ctrl_w_handler()
                elif pressed == readchar.key.CTRL_P:
                    selected_item.ctrl_p_handler()
                else:  # pragma: no cover
                    raise NotImplementedError
                raise exc.EndOfInputError(selection=selected_item)

        self.line_editor.press_key(pressed)

    def _process_input(self):
        """
        Core logic for processing input.
        """
        event = self.event_generator.next()
        if isinstance(event, events.KeyPressedEvent):
            self.process_key_pressed_input(pressed=event.value)

    def process_input(self):
        """
        A wrapper of the core logic for processing input, ensures that the
        ``need_process_input`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("--- process_input ---")
        try:
            if self.need_process_input:
                self._process_input()
        finally:
            self.need_process_input = True

    def move_to_end(self):
        debugger.log("--- move_to_end ---")
        try:
            self.render.move_to_end(n_items=self.n_items_on_screen)
        finally:
            self.need_move_to_end = True

    def event_loop(self):
        try:
            while True:
                debugger.log("=== new loop start ===")
                self.clear_items()
                self.clear_query()
                self.print_query()
                self.print_items()
                self.process_input()
                self.move_to_end()
        except exc.EndOfInputError as e:
            return e.selection
        except Exception as e:
            if self.capture_error:
                # if we capture error, we call move_to_end() method to finish
                # this loop, then run clear_items, clear_query, print_query,
                # print_items in a sequence to show the error
                # in the UI.
                # Then wait for user input and enter another event loop to
                # start over without exit.
                self.move_to_end()
                self.clear_items()
                self.clear_query()
                self.print_query()
                selected_item = self.dropdown.selected_item
                title = selected_item.title
                if title.startswith("Error on item: "):
                    title = title[len("Error on item: ") :]
                processed_title = self.render._process_title(
                    title,
                    self.render.terminal.width - 15,
                )
                self.print_items(
                    items=[
                        Item(
                            uid="uid",
                            title=f"Error on item: {processed_title}",
                            subtitle=f"{e!r}",
                        )
                    ]
                )
                self.process_input()
                self.move_to_end()
                return self.event_loop()
            else:
                raise e

    def run(self):
        try:
            return self.event_loop()
        finally:
            print("")
