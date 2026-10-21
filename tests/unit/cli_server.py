"""Tests CLI realtime flags for logs and observability commands."""

import argparse

from WatchGuardian._internal.cli.server import server


def test_realtime_defaults_to_false_and_is_opt_in() -> None:
    parser = argparse.ArgumentParser()
    modules = parser.add_subparsers(dest="module", required=True)
    server(modules)

    for command in ("logs", "obs"):
        normal = parser.parse_args(["server", command])
        realtime = parser.parse_args(["server", command, "--realtime"])

        assert normal.realtime is False
        assert realtime.realtime is True


if __name__ == "__main__":
    test_realtime_defaults_to_false_and_is_opt_in()
    print("Server CLI realtime flag test passed")
