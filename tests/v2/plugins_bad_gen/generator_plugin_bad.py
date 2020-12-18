from virl.api.plugin import GeneratorPlugin


class TestBadGenPlugin(GeneratorPlugin, generator="test-bad-gen"):
    def generate():
        print("TEST GENERATOR")
