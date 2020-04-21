import click
import requests

@click.command()
@click.argument('repo')
def pull(repo, **kwargs):
    """
    pull topology.yaml from repo
    """
    click.secho("Pulling from {}".format(repo))
    url = "https://raw.githubusercontent.com/"
    url = url + "{}/master/topology.yaml".format(repo)
    resp = requests.get(url)
    if resp.ok:
        with open('topology.yaml', 'w') as fh:
            fh.write(resp.text)
        click.secho("Saved topology as topology.yaml", fg="green")
    else:
        click.secho("Error pulling {} - repo not found".format(repo),
                    fg="red")

@click.command()
@click.argument('repo')
def pull1(repo, **kwargs):
    """
    pull topology.virl from repo
    """
    click.secho("Pulling from {}".format(repo))
    url = "https://raw.githubusercontent.com/"
    url = url + "{}/master/topology.virl".format(repo)
    resp = requests.get(url)
    if resp.ok:
        with open('topology.virl', 'w') as fh:
            fh.write(resp.text)
        click.secho("Saved topology as topology.virl", fg="green")
    else:
        click.secho("Error pulling {} - repo not found".format(repo),
                    fg="red")
