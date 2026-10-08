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

    # Pega a data atual
    @staticmethod
    def _get_time() -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    # Formata o texto
    @staticmethod
    def _format(text: str, level: str, time: datetime.datetime) -> str:
        return f"{level} | {__name__} | {str(time)} | {text}"

    def success(self, text: str) -> dict | None:

        if self.LEVELS["SUCCESS"] >= self.level_value:

            now = self._get_time()
            new_text = self.green(text=text)

            print(
                self._format(
                    text=new_text,
                    level="SUCCESS",
                    time=now,
                )
            )

            return {
                "level": "SUCCESS",
                "text": text,
                "created_at": now,
            }

        return None

    def info(self, text: str) -> dict | None:

        if self.LEVELS["INFO"] >= self.level_value:

            now = self._get_time()
            new_text = self.cyan(text=text)

            print(
                self._format(
                    text=new_text,
                    level="INFO",
                    time=now,
                )
            )

            return {
                "level": "INFO",
                "text": text,
                "created_at": now,
            }

        return None

    def warning(self, text: str) -> dict | None:

        if self.LEVELS["WARNING"] >= self.level_value:

            now = self._get_time()
            new_text = self.yellow(text=text)

            print(
                self._format(
                    text=new_text,
                    level="WARNING",
                    time=now,
                )
            )

            return {
                "level": "WARNING",
                "text": text,
                "created_at": now,
            }

        return None

    def error(self, text: str) -> dict | None:

        if self.LEVELS["ERROR"] >= self.level_value:

            now = self._get_time()
            new_text = self.red(text=text)

            print(
                self._format(
                    text=new_text,
                    level="ERROR",
                    time=now,
                )
            )

            return {
                "level": "ERROR",
                "text": text,
                "created_at": now,
            }

        return None

    def debug(self, text: str) -> dict | None:

        if self.LEVELS["DEBUG"] >= self.level_value:

            now = self._get_time()
            new_text = self.magenta(text=text)

            print(
                self._format(
                    text=new_text,
                    level="DEBUG",
                    time=now,
                )
            )

            return {
                "level": "DEBUG",
                "text": text,
                "created_at": now,
            }

        return None

    def critical(self, text: str) -> dict | None:

        if self.LEVELS["CRITICAL"] >= self.level_value:

            now = self._get_time()
            new_text = self.bold(
                self.red(text=text)
            )

            print(
                self._format(
                    text=new_text,
                    level="CRITICAL",
                    time=now,
                )
            )

            return {
                "level": "CRITICAL",
                "text": text,
                "created_at": now,
            }

        return None