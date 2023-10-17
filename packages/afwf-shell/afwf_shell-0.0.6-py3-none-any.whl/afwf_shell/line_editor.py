# -*- coding: utf-8 -*-

import blessed

SEP_LIST = "!@#$%^&*()-_+={[}]|\\:;"'<,>.?/'


class LineEditor:
    """
    Simulate a user input line editor. User can type characters, move cursor,
    backspace, delete, clear line, etc ...

    :param chars: a list of characters, representing the current line.
    :param cursor_position: the current cursor position. 0 means the cursor is
        at the beginning of the line. 1 means it is after the first character.
        when cursor_position == len(chars), it means the cursor is at the end.
    """

    def __init__(self):
        self.chars = []
        self.cursor_position = 0

    def is_cursor_begin_of_line(self) -> bool:
        return self.cursor_position == 0

    def is_cursor_end_of_line(self) -> bool:  # pragma: no cover
        return self.cursor_position == len(self.chars)

    def enter_text(self, text: str):
        for char in text:
            self.press_key(key=char)

    def _press_key(self, key: str):
        if self.is_cursor_end_of_line():
            self.chars.append(key)
            self.cursor_position += 1
        else:
            self.chars.insert(self.cursor_position, key)
            self.cursor_position += 1

    def press_key(self, key: str, n: int = 1):
        for _ in range(n):
            self._press_key(key)

    def _press_backspace(self):
        if self.cursor_position == 0:
            pass
        elif self.cursor_position == len(self.chars):
            self.chars.pop()
            self.cursor_position -= 1
        else:
            self.cursor_position -= 1
            self.chars.pop(self.cursor_position)

    def press_backspace(self, n: int = 1):
        for _ in range(n):
            self._press_backspace()

    def _press_left(self):
        if self.cursor_position != 0:
            self.cursor_position -= 1

    def press_left(self, n: int = 1):
        for _ in range(n):
            self._press_left()

    def press_home(self):
        self.cursor_position = 0

    def _press_delete(self):
        if self.cursor_position == len(self.chars):
            pass
        else:
            self.chars.pop(self.cursor_position)

    def press_delete(self, n: int = 1):
        for _ in range(n):
            self._press_delete()

    def _press_right(self):
        if self.cursor_position != len(self.chars):
            self.cursor_position += 1

    def press_right(self, n: int = 1):
        for _ in range(n):
            self._press_right()

    def press_end(self):
        self.cursor_position = len(self.chars)

    def clear_line(self):
        self.chars.clear()
        self.cursor_position = 0

    def clear_backward(self):
        self.chars = self.chars[self.cursor_position:]
        self.cursor_position = 0

    def clear_forward(self):
        self.chars = self.chars[: self.cursor_position]
        self.cursor_position = len(self.chars)

    def replace_text(self, text: str):
        self.clear_line()
        self.enter_text(text)

    def move_to_start(self):
        self.cursor_position = 0

    def move_to_end(self):
        self.cursor_position = len(self.chars)

    def move_word_backward(self):
        # 先获得光标之前的字符串
        line = self.value
        # 按照空格分割开, words 里面的元素可以是空字符串
        words = line.split(" ")
        # print(f"before: words = {words}")
        # 从后往前找到第一个非空字符串的 index
        ind = None
        for i, word in enumerate(words[::-1]):
            if word:
                ind = i
                break
        # print(f"ind = {ind}")
        # 如果找到了非空字符串
        if ind is not None:
            # 那么保留所有非空字符串之前的 word, 并把最后一个非空字符串替换成空字符串
            # 这样即可算的 cursor position
            if ind:
                words = words[:-ind]
            words[-1] = ""
            # print(f"after: words = {words}")
            self.cursor_position = len(" ".join(words))
        # 如果找不到非空字符串, 则移动到行首
        else:
            self.cursor_position = 0

    def move_word_forward(self):
        # 先获得光标之后的字符串
        line = "".join(self.chars[self.cursor_position:])
        # 按照空格分割开, words 里面的元素可以是空字符串
        words = line.split(" ")
        # print(f"before: words = {words}")
        # 从前往后找到第一个非空字符串
        ind = None
        for i, word in enumerate(words):
            if word:
                ind = i
                break
        # print(f"ind = {ind}")
        # 如果找到了非空字符串, 则计算这个非空字符串起之前的所有字符串的总长度
        # 这个长度就是 cursor 要移动的距离
        if ind is not None:
            words = words[:(ind+1)]
            # print(f"after: words = {words}")
            self.cursor_position += len(" ".join(words))
        # 如果找不到非空字符串, 则移动到行尾
        else:
            self.cursor_position = len(self.chars)

    @property
    def line(self) -> str:
        """
        Example: ``ali|ce`` -> line = alice
        """
        return "".join(self.chars)

    @property
    def value(self) -> str:
        """
        Example: ``ali|ce`` -> value = ali
        """
        return "".join(self.chars[: self.cursor_position])
