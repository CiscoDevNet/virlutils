from virl.api import ViewerPlugin

viewer = "lab"


class LabViewer(ViewerPlugin, viewer=viewer):
    def visualize(self, **kwargs):
        print("TEST VIEWER")
