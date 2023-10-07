# -*- coding: utf-8 -*-

import typing as T
import readchar


class Event:
    pass


class KeyPressedEvent(Event):
    def __init__(self, value):
        self.value = value


class RepaintEvent(Event):
    pass


class KeyEventGenerator:
    def __init__(
        self,
        key_generator: T.Optional[T.Callable[[], str]] = None,
    ):
        self._key_generator = key_generator or readchar.readkey

    def next(self) -> KeyPressedEvent:
        return KeyPressedEvent(value=self._key_generator())
