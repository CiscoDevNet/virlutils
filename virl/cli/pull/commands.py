import click
import requests


def do_pull(repo, fname, branch="master", recurse=False):
    click.secho("Pulling from {} on branch {}".format(repo, branch))
    url = "https://raw.githubusercontent.com/"
    url = url + "{}/{}/{}".format(repo, branch, fname)
    resp = requests.get(url)
    if resp.ok:
        with open(fname, "w") as fh:
            fh.write(resp.text)
        click.secho("Saved topology as {}".format(fname), fg="green")
        return True
    elif resp.status_code == 404 and not recurse:
        return do_pull(repo, fname, "main", True)
    else:
        click.secho("Error pulling {} - repo or file not found".format(repo), fg="red")
        return False


@click.command()
@click.argument("repo")
def pull(repo, **kwargs):
    """
    pull topology.yaml from repo
    """
    ret = do_pull(repo, "topology.yaml")
    if not ret:
        ret = do_pull(repo, "topology.virl")
        if not ret:
            exit(1)


@click.command()
@click.argument("repo")
def pull1(repo, **kwargs):
    """
    pull topology.virl from repo
    """
    ret = do_pull(repo, "topology.virl")
    if not ret:
        exit(1)
