import click
from virl.cli.definitions.images.iimport.image_file.commands import image_file
from virl.cli.definitions.images.iimport.definition.commands import definition


@click.group()
def iimport():
    """
    import images and image definitions
    """
    pass


iimport.add_command(image_file)
iimport.add_command(definition)
