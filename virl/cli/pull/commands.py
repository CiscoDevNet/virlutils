import click
import requests


def do_pull(repo, fname):
    click.secho("Pulling from {}".format(repo))
    url = "https://raw.githubusercontent.com/"
    url = url + "{}/master/{}".format(repo, fname)
    resp = requests.get(url)
    if resp.ok:
        with open(fname, "w") as fh:
            fh.write(resp.text)
        click.secho("Saved topology as {}".format(fname), fg="green")
    else:
        click.secho("Error pulling {} - repo not found".format(repo), fg="red")
        exit(1)


@click.command()
@click.argument("repo")
def pull(repo, **kwargs):
    """
    pull topology.yaml from repo
    """
    do_pull(repo, "topology.yaml")


@click.command()
@click.argument("repo")
def pull1(repo, **kwargs):
    """
    pull topology.virl from repo
    """
    do_pull(repo, "topology.virl")
