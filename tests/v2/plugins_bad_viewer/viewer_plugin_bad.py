from virl.api.plugin import ViewerPlugin


class BadLabViewer(ViewerPlugin):
    def visualize(self, **kwargs):
        print("VIEWER PLUGIN")
