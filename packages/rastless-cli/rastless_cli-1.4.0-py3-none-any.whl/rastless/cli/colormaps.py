import click
import simplejson

from rastless.commands import colormaps
from rastless.config import Cfg


@click.command()
@click.pass_obj
@click.argument('sld_file', type=click.Path(exists=True))
@click.option("-n", "--name", help="Name of the colormap, otherwise take the filename")
@click.option("-d", "--description", help="Add description")
@click.option("-l", "--legend-image", help="Filepath to png legend image")
def add_colormap(cfg: Cfg, sld_file, name, description, legend_image):
    """Add a SLD file"""
    try:
        colormaps.add_colormap(cfg, sld_file, name, description, legend_image)
    except Exception as e:
        click.echo(f"SLD File could not be converted. Reason: {e}")


@click.command()
@click.option("-n", "--name", help="Name of the colormap", required=True)
@click.pass_obj
def delete_colormap(cfg: Cfg, name):
    """Remove a SLD file"""
    colormaps.delete_colormap(cfg, name)


@click.command()
@click.pass_obj
def list_colormaps(cfg: Cfg):
    """List all colormaps"""
    cms = colormaps.list_colormaps(cfg)
    click.echo(simplejson.dumps(cms, indent=4, sort_keys=True))
    return cms
