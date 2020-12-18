from virl.api.plugin import GeneratorPlugin
import click


class TestGenPlugin(GeneratorPlugin, generator="test-gen"):
    @staticmethod
    @click.command()
    def generate():
        print("TEST GENERATOR")
