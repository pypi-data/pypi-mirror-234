# -*- coding: utf-8 -*-

from datetime import datetime
from .paths import path_log_txt


class Debugger:
    def __init__(self):
        self.path_log_txt = path_log_txt
        self._enable = False

    def reset(self):
        self.path_log_txt.unlink(missing_ok=True)

    def enable(self):
        self._enable = True

    def disable(self):
        self._enable = False

    def _log(self, text: str):
        with self.path_log_txt.open("a") as f:
            ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            line = f"{ts} {text}\n"
            f.write(line)

    def log(self, text: str):
        if self._enable:
            self._log(text)


debugger = Debugger()
