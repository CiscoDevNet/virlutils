import click
from virl.helpers import store_sim_info


@click.command()
@click.argument('sim')
def use(sim):
    """
    use virl simulation launched elsewhere
    """
    store_sim_info(sim, env='default')  # 'topology-2lkx2'
    click.secho('Now using VIRL simulation {}'.format(sim))
