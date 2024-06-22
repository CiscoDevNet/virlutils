import click

from virl.api.plugin import CommandPlugin


class TestCmdPlugin(CommandPlugin, command="test-cmd"):
    @staticmethod
    @click.command()
    def run():
        print("TEST COMMAND")
