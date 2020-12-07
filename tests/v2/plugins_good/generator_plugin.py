from virl.api.plugin import GeneratorPlugin
import click

generator = "test-gen"


class TestGenPlugin(GeneratorPlugin, generator=generator):
    @staticmethod
    @click.command()
    def generate():
        print("TEST GENERATOR")
