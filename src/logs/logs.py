"""
Serve pra salvar os logs
"""

import datetime
from typing import Literal

from src.logs.colors import Colors


class Logs(Colors):

    LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "SUCCESS": 25,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }

    def __init__(
        self,
        loglevel: Literal[
            "SUCCESS",
            "INFO",
            "WARNING",
            "ERROR",
            "DEBUG",
            "CRITICAL",
        ],
    ) -> None:

        self.level = loglevel
        self.level_value = self.LEVELS[loglevel]

    @staticmethod
    def _get_time() -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    
    def _format(self,text: str, level: str, time: datetime.datetime) -> str:
        return f"[{self.gray(level)}] => {self.brown(__name__)} | {self.gold(str(time))} | {text}"

    def _can_log(self, level: str) -> bool:

        if self.level == "SUCCESS":
            return True

        return self.LEVELS[level] >= self.level_value

    def success(self, text: str) -> dict | None:

        if not self._can_log("SUCCESS"):
            return None

        now = self._get_time()
        new_text = self.green(text=text)

        print(
            self._format(
                text=new_text,
                level=self.green("SUCCESS"),
                time=now,
            )
        )

        return {
            "level": "SUCCESS",
            "text": text,
            "created_at": now,
        }

    def info(self, text: str) -> dict | None:

        if not self._can_log("INFO"):
            return None

        now = self._get_time()
        new_text = self.cyan(text=text)

        print(
            self._format(
                text=new_text,
                level=self.cyan("INFO"),
                time=now,
            )
        )

        return {
            "level": "INFO",
            "text": text,
            "created_at": now,
        }

    def warning(self, text: str) -> dict | None:

        if not self._can_log("WARNING"):
            return None

        now = self._get_time()
        new_text = self.yellow(text=text)

        print(
            self._format(
                text=new_text,
                level=self.yellow("WARNING"),
                time=now,
            )
        )

        return {
            "level": "WARNING",
            "text": text,
            "created_at": now,
        }

    def error(self, text: str) -> dict | None:

        if not self._can_log("ERROR"):
            return None

        now = self._get_time()
        new_text = self.red(text=text)

        print(
            self._format(
                text=new_text,
                level=self.red("ERROR"),
                time=now,
            )
        )

        return {
            "level": "ERROR",
            "text": text,
            "created_at": now,
        }

    def debug(self, text: str) -> dict | None:

        if not self._can_log("DEBUG"):
            return None

        now = self._get_time()
        new_text = self.magenta(text=text)

        print(
            self._format(
                text=new_text,
                level=self.magenta("DEBUG"),
                time=now,
            )
        )

        return {
            "level": "DEBUG",
            "text": text,
            "created_at": now,
        }

    def critical(self, text: str) -> dict | None:

        if not self._can_log("CRITICAL"):
            return None

        now = self._get_time()
        new_text = self.bold(
            self.red(text=text)
        )

        print(
            self._format(
                text=new_text,
                level=self.red("CRITICAL"),
                time=now,
            )
        )

        return {
            "level": "CRITICAL",
            "text": text,
            "created_at": now,
        }