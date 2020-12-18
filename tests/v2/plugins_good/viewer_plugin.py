from virl.api import ViewerPlugin


class LabViewer(ViewerPlugin, viewer="lab"):
    def visualize(self, **kwargs):
        print("TEST VIEWER")
