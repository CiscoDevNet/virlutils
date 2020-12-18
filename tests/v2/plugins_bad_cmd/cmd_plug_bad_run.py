from virl.api.plugin import CommandPlugin


class TestBadCmdPlugin(CommandPlugin, command="test-bad-cmd"):
    def run():
        print("TEST COMMAND")
