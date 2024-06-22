import click

from virl.api.plugin import GeneratorPlugin


class TestGenPlugin(GeneratorPlugin, generator="test-gen"):
    @staticmethod
    @click.command()
    def generate():
        print("TEST GENERATOR")
