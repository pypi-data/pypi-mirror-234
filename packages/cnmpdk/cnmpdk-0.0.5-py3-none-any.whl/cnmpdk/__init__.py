"""cnm_gf - pdk for cnm silicon nitride"""
__version__ = '0.0.1'
__author__ = 'Mario Mejias <mario.mejias@vlcphotonics.com>'

import sys
import gdsfactory as gf
from cnmpdk.tech import LAYER
from cnmpdk import tech
from gdsfactory.pdk import Pdk
from gdsfactory.cross_section import get_cross_section_factories
from gdsfactory.get_factories import get_cells

cross_sections = get_cross_section_factories(tech)
cells = get_cells(sys.modules[__name__])

PDK = Pdk(
    name="cnmpdk",
    cells=cells,
    cross_sections=cross_sections,
    layers=LAYER.dict(),
    # layer_stack=LAYER_STACK,
    # layer_views=LAYER_VIEWS,
    # sparameters_path=PATH.sparameters_path,
)
PDK.activate()

__all__ = [
    "LAYER",
    "deep",
]