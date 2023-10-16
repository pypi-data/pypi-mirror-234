from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from rastless.db.base import DynamoBaseModel, camel_case, str_uuid


class LayerModel(DynamoBaseModel):
    layer_id: str = Field(default_factory=str_uuid)
    client: str
    product: str
    title: str
    region_id: int = 1
    unit: Optional[str] = None
    background_id: Optional[str] = None
    colormap: Optional[str] = None
    description: Optional[str] = None

    _pk_tag = "layer"
    _sk_tag = "layer"
    _sk_value = "layer_id"


class PermissionModel(DynamoBaseModel):
    permission: str
    layer_id: str

    _pk_tag = "permission"
    _pk_value = "permission"
    _sk_tag = "layer"
    _sk_value = "layer_id"


class CogFile(BaseModel):
    s3_filepath: str
    bbox: tuple[Decimal, Decimal, Decimal, Decimal]

    @classmethod
    @field_validator('bbox', mode="before")
    def to_decimal(cls, value):
        return [Decimal(str(item)) if not isinstance(item, Decimal) else item for item in value]

    class Config:
        populate_by_name = True
        alias_generator = camel_case


class LayerStepModel(DynamoBaseModel):
    layer_id: str
    cog_filepath: Optional[str] = None
    cog_layers: Optional[dict[str, CogFile]] = None
    datetime: str
    sensor: str
    resolution: Decimal
    temporal_resolution: str
    maxzoom: int
    minzoom: int
    bbox: tuple[Decimal, Decimal, Decimal, Decimal]

    _pk_tag = "step"
    _pk_value = "datetime"
    _sk_tag = "layer"
    _sk_value = "layer_id"

    @classmethod
    @field_validator('bbox', mode="before")
    def to_decimal(cls, value):
        return [Decimal(str(item)) if not isinstance(item, Decimal) else item for item in value]


class ColorMap(DynamoBaseModel):
    name: str
    description: Optional[str] = None
    values: List[Decimal]
    colors: List[List[Decimal]]
    nodata: List[Decimal]
    legend_image: Optional[str] = None

    _pk_tag = "cm"
    _sk_tag = "cm"
    _sk_value = "name"
