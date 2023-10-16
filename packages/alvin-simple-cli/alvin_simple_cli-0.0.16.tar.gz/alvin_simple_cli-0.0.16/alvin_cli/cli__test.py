# ruff: noqa: PLR6301
import unittest

from alvin_cli.cli import setup


class TestCLI(unittest.TestCase):

    def test_dummy(self) -> None:
        setup()
