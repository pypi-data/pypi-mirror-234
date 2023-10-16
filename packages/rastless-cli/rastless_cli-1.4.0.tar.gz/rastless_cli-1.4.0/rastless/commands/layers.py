from typing import Set

from rastless.config import Cfg
from rastless.core.cog import append_to_timestep, create_new_timestep
from rastless.core.s3 import delete_layer_step_files
from rastless.core.validate import validate_filenames_exists, validate_input_with_append, validate_layer_step_override
from rastless.db.models import LayerModel, PermissionModel


def create_layer(cfg: Cfg, permissions, **kwargs):
    layer = LayerModel.model_validate(kwargs)
    cfg.db.add_layer(layer)

    permission_models = [PermissionModel(permission=permission, layer_id=layer.layer_id) for permission in permissions]
    cfg.db.add_permissions(permission_models)

    return layer.layer_id


def create_timestep(cfg: 'Cfg', filenames: Set[str], append: bool, datetime: str, sensor: str, layer_id: str,
                    temporal_resolution: str, profile: str, override: bool):
    validate_filenames_exists(set(filenames))
    validate_input_with_append(sensor, append)

    layer_step = cfg.db.get_layer_step(datetime, layer_id)
    override = validate_layer_step_override(layer_step, append, override)

    if layer_step and override:
        delete_layer_step_files(layer_step, cfg)
        create_new_timestep(cfg, filenames, layer_id, datetime, profile, temporal_resolution, sensor)
    elif layer_step and append:
        append_to_timestep(cfg, layer_step, filenames, profile)
    else:
        create_new_timestep(cfg, filenames, layer_id, datetime, profile, temporal_resolution, sensor)


def list_layers(cfg: Cfg, client):
    """List all layers"""
    layers = cfg.db.list_layers()
    if client:
        return [x for x in layers if x["client"] == client]
    else:
        return layers
