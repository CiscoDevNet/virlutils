from virl.api.plugin import CommandPlugin
import click

command = "test-cmd"


class TestCmdPlugin(CommandPlugin, command=command):
    @staticmethod
    @click.command()
    def run():
        print("TEST COMMAND")
