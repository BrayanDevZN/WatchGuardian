"Utilitario para executar comandos do sistema."

import os
import shlex
import subprocess


class Cmd:

    @staticmethod
    def run(command: str) -> subprocess.CompletedProcess:
        args = shlex.split(command)

        return subprocess.run(
            args,
            check=False,
        )

    @staticmethod
    def detached(command: str) -> subprocess.Popen:
        args = shlex.split(command)

        if os.name == "nt":
            flags = (
                subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP
            )

            return subprocess.Popen(
                args,
                creationflags=flags,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        return subprocess.Popen(
            args,
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
