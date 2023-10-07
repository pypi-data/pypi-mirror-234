# -*- coding: utf-8 -*-

import typing as T


class EndOfInputError(Exception):
    """ """

    def __init__(
        self,
        selection: T.Any,
        *args,
    ):
        super().__init__(*args)
        self.selection = selection


class TerminalTooSmallError(SystemError):
    pass
