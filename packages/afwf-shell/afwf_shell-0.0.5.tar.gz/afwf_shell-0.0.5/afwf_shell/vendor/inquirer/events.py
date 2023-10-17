# -*- coding: utf-8 -*-

import typing as T
import readchar


class Event:
    """
    Base class for all event.
    """

    pass


class KeyPressed(Event):
    """
    Keyboard event.
    """

    def __init__(self, value):
        self.value = value


class KeyEventGenerator:
    """
    Keyboard event generator, it
    """

    def __init__(self, key_generator: T.Optional[T.Callable] = None):
        self._key_gen = key_generator or readchar.readkey

    def next(self):
        return KeyPressed(self._key_gen())
