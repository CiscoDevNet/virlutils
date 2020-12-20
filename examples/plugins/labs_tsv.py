from virl.api import ViewerPlugin


class LabsTSVViewer(ViewerPlugin, viewer="lab"):
    def visualize(self, **kwargs):
        """
        Render the labs list as a tab-delimited set of
        rows.  Replaces the output of `cml ls`.

        The input will be kwargs["labs"] and kwargs["cached_labs"]
        """

        labs = kwargs["labs"]
        if kwargs["cached_labs"]:
            labs += kwargs["cached_labs"]

        print("ID\tTitle\tDescription\tOwner\tStatus\tNodes\tLinks\tInterfaces")
        for lab in labs:
            """
            Each lab is of type virl2_client.models.lab.Lab whereas each cached lab is of
            type virl.api.cml.CachedLab.  The two are similar enough for these properties to
            be common
            """
            print(
                "{id}\t{title}\t{description}\t{owner}\t{status}\t{nodes}\t{links}\t{interfaces}".format(
                    id=lab.id,
                    title=lab.title,
                    description=lab.description,
                    owner=lab.owner,
                    status=lab.state(),
                    nodes=lab.statistics["nodes"],
                    links=lab.statistics["links"],
                    interfaces=lab.statistics["interfaces"],
                )
            )
