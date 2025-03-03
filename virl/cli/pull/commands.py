import click
import requests


def do_pull(repo, fname, branch="master", recurse=False):
    click.secho("Pulling {} from {} on branch {}".format(fname, repo, branch))
    url = "https://raw.githubusercontent.com/"
    url = url + "{}/{}/{}".format(repo, branch, fname)
    resp = requests.get(url)
    if resp.ok:
        with open(fname, "w") as fh:
            fh.write(resp.text)
        click.secho("Saved topology as {}".format(fname), fg="green")
        return True
    else:
        click.secho("Error pulling {} from {} on branch {} - repo, file, or branch not found".format(fname, repo, branch), fg="red")
        return False


@click.command()
@click.argument("repo")
@click.option("--file", default="topology.yaml", required=False, help="Filename to pull (default: topology.yaml)")
@click.option("--branch", default="main", required=False, help="Branch name from which to pull (default: main)")
def pull(repo, file, branch):
    """
    pull CML lab YAML file from repo
    """
    ret = do_pull(repo, fname=file, branch=branch)
    if not ret:
        exit(1)
