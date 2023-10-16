import gdsfactory as gf
from pydantic import BaseModel
from gdsfactory.typings import Layer
from functools import partial
from gdsfactory.add_pins import add_pins_inside1nm
from gdsfactory.technology import LayerLevel, LayerStack
from gdsfactory.cross_section import cross_section, Section

class LayerMap(BaseModel):
    SHALLOW_WAVEGUIDES: Layer = (1, 0)
    DEEP_WAVEGUIDES: Layer = (2, 0)
    TRENCH: Layer = (3, 0)
    HEATER: Layer = (4, 0)
    DEEP_WAVEGUIDES_PROTECTION: Layer = (11, 0)
    SHALLOW_WAVEGUIDES_PROTECTION: Layer = (21, 0)
    DICING_LINES: Layer = (100, 0)
    PORT: Layer = (1,10)
    BB_OUTLINE: Layer = (51,0)
    BB_GUIDES: Layer = (52,0)
    BB_PARAMETERS: Layer = (53,0)

    class Config:
        """pydantic config."""
        
        frozen = True
        extra = "forbid"

LAYER = LayerMap()

# Cross sections
deep = gf.partial(
    gf.cross_section.strip,
    width=1.2,
    radius=100,
    layer=LAYER.DEEP_WAVEGUIDES,
    cladding_layers=(LAYER.DEEP_WAVEGUIDES,LAYER.DEEP_WAVEGUIDES_PROTECTION),
    cladding_offsets=(0.1,15,-15,-0.1),
)
shallow = gf.partial(
    gf.cross_section.strip,
    width=1.2,
    radius=150,
    layer=LAYER.SHALLOW_WAVEGUIDES,
    cladding_layers=(LAYER.SHALLOW_WAVEGUIDES,LAYER.SHALLOW_WAVEGUIDES_PROTECTION),
    cladding_offsets=(0.1,15,-15,-0.1),
)
heater = gf.partial(
    cross_section,
    width=10,
    layer=LAYER.HEATER,
    name="heater",
    add_bbox=None,
)
trench = gf.partial(
    cross_section,
    width=10,
    layer=LAYER.TRENCH,
    name="trench",
    add_bbox=None,
)

if __name__ == "__main__":

    # import cnmpdk   #IMPORTANT
    from components import cnmMMI1x2DE_BB
    c = gf.Component("test name")
    mmi1 = c << cnmMMI1x2DE_BB()
    mmi2 = c << cnmMMI1x2DE_BB()
    mmi2.move((100,50))

    route = gf.routing.get_route(input_port=mmi1.ports["out1"], output_port=mmi2.ports["in0"], cross_section="deep")
    c.add(route.references)

    c.show(show_ports=True)