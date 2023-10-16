import base64
from typing import List
from xml.dom import minidom

import numpy as np

from rastless.db.models import ColorMap


class Sld:
    def __init__(self, filename):
        self.xml_doc = minidom.parse(filename)
        self.items = self.xml_doc.getElementsByTagName('sld:ColorMapEntry')

    @staticmethod
    def _hex_to_rgb(hex_color) -> tuple:
        hex_value = hex_color.lstrip('#')
        return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))

    @property
    def hex_colors(self) -> np.array:
        return np.array([entry.attributes["color"].value for entry in self.items if
                         float(entry.attributes["opacity"].value) > 0])

    @property
    def rgb_colors(self) -> np.array:
        return np.array([self._hex_to_rgb(hex_color) for hex_color in self.hex_colors])

    @property
    def values(self) -> np.array:
        return np.array([float(entry.attributes["quantity"].value) for entry in self.items if
                         float(entry.attributes["opacity"].value) > 0])

    @property
    def no_data(self) -> List:
        return [float(entry.attributes["quantity"].value) for entry in self.items if
                float(entry.attributes["opacity"].value) == 0]


def legend_png_to_base64(legend_filepath: str) -> bytes:
    with open(legend_filepath, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
    return encoded_image


def create_colormap(name: str, sld_filepath: str, description: str = None, legend_filepath: str = None) -> ColorMap:
    legend_base64 = None
    if legend_filepath:
        legend_base64 = legend_png_to_base64(legend_filepath)

    sld = Sld(sld_filepath)
    return ColorMap(name=name, values=sld.values.tolist(), colors=sld.rgb_colors.tolist(),
                    nodata=sld.no_data, description=description, legend_image=legend_base64)
