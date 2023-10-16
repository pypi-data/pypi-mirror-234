import gdsfactory as gf
from gdsfactory.read import import_gds
from cnmpdk.config import PATH
from functools import partial

library_version = "6.1.1"
library_path = "CNM_library_v"+library_version+"_BB_MPW_06_07-07-2022_CNMPDK.gds"

gdsdir = PATH.gds
import_gds = partial(gf.import_gds, gdsdir=gdsdir)

@gf.cell
def cnmD2SBB_1to1() -> gf.Component:
    """Return cnmD2SBB_1to1 fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmD2SBB_1to1")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[53,0],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmD2SBB_1to2() -> gf.Component:
    """Return cnmD2SBB_1to2 fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmD2SBB_1to2")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[73,0],width=2.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmD2SBB_1to3() -> gf.Component:
    """Return cnmD2SBB_1to3 fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmD2SBB_1to3")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[83,0],width=3.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmINVTAP_10_0() -> gf.Component:
    """Return cnmINVTAP_10 fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmINVTAP_10.0")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[425.12500,0],width=0.95,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI1585_BB() -> gf.Component:
    """Return cnmMMI1585_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI1585_BB")
    c.add_port(name="in0",center=[0,-3.85],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,3.85],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[253.37000,-3.85],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[253.37000,3.85],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI1x2DE_BB() -> gf.Component:
    """Return cnmMMI1x2DE_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI1x2DE_BB")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[66.08700,-3.85],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[66.08700,3.85],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI1x2SH_BB() -> gf.Component:
    """Return cnmMMI1x2SH_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI1x2SH_BB")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[91.48900,-4.65],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[91.48900,4.65],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI2x2DE_BB() -> gf.Component:
    """Return cnmMMI2x2DE_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI2x2DE_BB")
    c.add_port(name="in0",center=[0,-4.5],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,4.5],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[205.42000,-4.5],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[205.42000,4.5],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI2x2SH_BB() -> gf.Component:
    """Return cnmMMI2x2SH_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI2x2SH_BB")
    c.add_port(name="in0",center=[0,-4.6],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,4.6],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[214.50600,-4.6],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[214.50600,4.6],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI3x3DE_BB() -> gf.Component:
    """Return cnmMMI3x3DE_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI3x3DE_BB")
    c.add_port(name="in0",center=[0,-5.65],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="in2",center=[0,5.65],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[210.47700,-5.65],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[210.47700,0],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[210.47700,5.65],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI3x3SH_BB() -> gf.Component:
    """Return cnmMMI3x3SH_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI3x3SH_BB")
    c.add_port(name="in0",center=[0,-6.65],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="in2",center=[0,6.65],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[315.26100,-6.65],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[315.26100,0],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[315.26100,6.65],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmMMI8515_BB() -> gf.Component:
    """Return cnmMMI8515_BB fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmMMI8515_BB")
    c.add_port(name="in0",center=[0,-3.9],width=1.2,orientation=180,layer=1)
    c.add_port(name="in1",center=[0,3.9],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[119.67400,-3.9],width=1.2,orientation=0,layer=1)
    c.add_port(name="out1",center=[119.67400,3.9],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmS2DBB_1to1() -> gf.Component:
    """Return cnmS2DBB_1to1 fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmS2DBB_1to1")
    c.add_port(name="in0",center=[0,0],width=1.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[53,0],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmS2DBB_2to1() -> gf.Component:
    """Return cnmS2DBB_2to1 fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmS2DBB_2to1")
    c.add_port(name="in0",center=[0,0],width=2.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[73,0],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnmS2DBB_3to1() -> gf.Component:
    """Return cnmS2DBB_3to1 fixed cell."""
    c = gf.Component()
    c = import_gds(library_path, "cnmS2DBB_3to1")
    c.add_port(name="in0",center=[0,0],width=3.2,orientation=180,layer=1)
    c.add_port(name="out0",center=[83,0],width=1.2,orientation=0,layer=1)
    return c

@gf.cell
def cnm_5x5_die() -> gf.Component:
    """Return cnm_5x5_die fixed cell."""
    return import_gds("CNM_5x5_Die.gds")

@gf.cell
def cnm_10x5_die() -> gf.Component:
    """Return cnm_10x5_die fixed cell."""
    return import_gds("CNM_10x5_Die.gds")

if __name__ == "__main__":
    # import cnmpdk
    # c = cnmD2SBB_1to1()
    # c = cnm_5x5_die()
    # c = cnm_10x5_die()

    c = gf.Component("test name")

    mmi1 = c << cnmMMI1x2DE_BB()
    mmi2 = c << cnmMMI1x2DE_BB()
    mmi2.move((200,50))

    # route = gf.routing.get_route(input_port=mmi1.ports["out1"], output_port=mmi2.ports["in0"], cross_section="strip")
    route = gf.routing.get_route_sbend(mmi1.ports["out1"], mmi2.ports["in0"], cross_section="deep")

    # mmi1 = c << gf.components.mmi1x2()
    # mmi2 = c << gf.components.mmi1x2()
    # mmi2.movex(50)
    # mmi2.movey(5)
    # route = gf.routing.get_route_sbend(mmi1.ports['o2'], mmi2.ports['o1'])

    c.add(route.references)

    c.show(show_ports=True)
    # c.plot()

    # c = gf.Component("demo_route_sbend")
    # mmi1 = c << gf.components.mmi1x2()
    # mmi2 = c << gf.components.mmi1x2()
    # mmi2.movex(50)
    # mmi2.movey(5)
    # route = gf.routing.get_route_sbend(mmi1.ports['o2'], mmi2.ports['o1'])
    # c.add(route.references)
    # # c.plot()
    # c.show(show_ports=True)