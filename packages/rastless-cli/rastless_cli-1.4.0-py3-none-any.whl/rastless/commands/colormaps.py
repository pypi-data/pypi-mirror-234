import os

from rastless.config import Cfg
from rastless.core.colormap import create_colormap


def add_colormap(cfg, sld_file, name, description, legend_image):
    """Add a SLD file"""

    if not name:
        name = os.path.basename(sld_file.split(".")[0])
    color_map = create_colormap(name, sld_file, description, legend_image)
    cfg.db.add_color_map(color_map)


def delete_colormap(cfg: Cfg, name):
    """Remove a SLD file"""
    cfg.db.delete_color_map(name)


def list_colormaps(cfg: Cfg):
    """List all colormaps"""
    return cfg.db.get_color_maps()
