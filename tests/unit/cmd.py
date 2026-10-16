"""Testa o utilitário de comandos do sistema."""

import sys

from src.service.module import Cmd


def test_run() -> None:
    result = Cmd.run(
        f'{sys.executable} -c "print(\'watchguardian-cmd-run\')"'
    )

    assert result.returncode == 0


def test_detached() -> None:
    process = Cmd.detached(
        f'{sys.executable} -c "import time; time.sleep(0.2)"'
    )

    assert process.pid is not None
    assert process.pid > 0

    process.wait(timeout=5)
    assert process.returncode == 0


if __name__ == "__main__":
    test_run()
    test_detached()
