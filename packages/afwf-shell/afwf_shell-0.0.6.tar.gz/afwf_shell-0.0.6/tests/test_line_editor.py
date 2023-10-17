# -*- coding: utf-8 -*-

from afwf_shell.line_editor import LineEditor


def _test_press_key():
    le = LineEditor()
    le.press_key("a")
    assert le.line == "a"
    assert le.value == "a"


def _test_enter_text():
    le = LineEditor()
    le.enter_text("abc")
    assert le.line == "abc"
    assert le.value == "abc"


def _test_press_backspace():
    le = LineEditor()
    le.enter_text("abc")
    le.press_backspace()
    assert le.line == "ab"
    assert le.value == "ab"

    le.press_backspace(2)
    assert le.line == ""
    assert le.value == ""

    le.press_backspace(5)
    assert le.line == ""
    assert le.value == ""


def _test_press_left():
    le = LineEditor()
    le.enter_text("alice")

    le.press_left()
    assert le.line == "alice"
    assert le.value == "alic"

    le.press_backspace()
    assert le.line == "alie"
    assert le.value == "ali"

    le.press_left()
    assert le.line == "alie"
    assert le.value == "al"

    le.press_key("X")
    assert le.line == "alXie"
    assert le.value == "alX"


def _test_press_home():
    le = LineEditor()
    le.enter_text("alice")

    le.press_home()
    assert le.line == "alice"
    assert le.value == ""

    le.press_left()
    assert le.line == "alice"
    assert le.value == ""


def _test_press_delete():
    le = LineEditor()
    le.enter_text("abcde")
    le.press_delete()
    assert le.line == "abcde"
    assert le.value == "abcde"

    le.press_left(2)

    le.press_delete()
    assert le.line == "abce"
    assert le.value == "abc"

    le.press_delete()
    assert le.line == "abc"
    assert le.value == "abc"

    le.press_delete()
    assert le.line == "abc"
    assert le.value == "abc"

    le.press_home()
    le.press_delete(5)
    assert le.line == ""
    assert le.value == ""


def _test_press_right():
    le = LineEditor()
    le.enter_text("alice")

    le.press_right()
    assert le.line == "alice"
    assert le.value == "alice"

    le.press_home()
    le.press_right()
    assert le.line == "alice"
    assert le.value == "a"


def _test_press_end():
    le = LineEditor()
    le.enter_text("alice")

    le.press_home()
    le.press_end()
    assert le.line == "alice"
    assert le.value == "alice"

    le.press_left()
    le.press_end()
    assert le.line == "alice"
    assert le.value == "alice"


def _test_clear_line():
    le = LineEditor()
    le.enter_text("alice")
    le.clear_line()
    assert le.line == ""
    assert le.value == ""

    le.enter_text("alice")
    le.press_left()
    le.clear_line()
    assert le.line == ""
    assert le.value == ""


def _test_clear_backward():
    le = LineEditor()
    le.enter_text("alice")
    le.press_left(2)
    le.clear_backward()
    assert le.line == "ce"
    assert le.value == ""


def _test_clear_forward():
    le = LineEditor()
    le.enter_text("alice")
    le.press_left(3)
    le.clear_forward()
    assert le.line == "al"
    assert le.value == "al"


def _test_move_word():
    le = LineEditor()
    text = " hello world alice bob "

    # --- move backward
    le.replace_text(text)
    le.move_word_backward()
    assert le.line == text
    assert le.value == " hello world alice "

    le.replace_text(text)
    le.press_left(1)
    le.move_word_backward()
    assert le.line == text
    assert le.value == " hello world alice "

    le.replace_text(text)
    le.press_left(2)
    le.move_word_backward()
    assert le.line == text
    assert le.value == " hello world alice "

    le.replace_text(text)
    le.press_left(7)
    le.move_word_backward()
    assert le.line == text
    assert le.value == " hello world "

    le.replace_text(text)
    le.move_to_start()
    le.move_word_backward()
    assert le.line == text
    assert le.value == ""

    le.replace_text("    ")
    le.move_word_backward()
    assert le.line == "    "
    assert le.value == ""

    # --- move forward
    le.replace_text(text)
    le.move_to_start()
    le.move_word_forward()
    assert le.line == text
    assert le.value == " hello"

    le.replace_text(text)
    le.move_to_start()
    le.press_right(1)
    le.move_word_forward()
    assert le.line == text
    assert le.value == " hello"

    le.replace_text(text)
    le.move_to_start()
    le.press_right(2)
    le.move_word_forward()
    assert le.line == text
    assert le.value == " hello"

    le.replace_text(text)
    le.move_to_start()
    le.press_right(7)
    le.move_word_forward()
    assert le.line == text
    assert le.value == " hello world"

    le.replace_text(text)
    le.move_to_end()
    le.move_word_forward()
    assert le.line == text
    assert le.value == text

    le.replace_text("    ")
    le.move_word_forward()
    assert le.line == "    "
    assert le.value == "    "


def test():
    print("")
    _test_press_key()
    _test_enter_text()
    _test_press_backspace()
    _test_press_left()
    _test_press_home()
    _test_press_delete()
    _test_press_right()
    _test_press_end()
    _test_clear_line()
    _test_clear_backward()
    _test_clear_forward()
    _test_move_word()


if __name__ == "__main__":
    from afwf_shell.tests import run_cov_test

    run_cov_test(__file__, "afwf_shell.line_editor", preview=False)
