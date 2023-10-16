from pyfeyn2.auto.bend import auto_bend
from pyfeyn2.auto.label import auto_label
from pyfeyn2.auto.position import feynman_adjust_points
from pyfeyn2.feynmandiagram import FeynmanDiagram


def auto_diagram(fd: FeynmanDiagram, scale=2, size=15):
    """
    Automatically tune a Feynman diagram from a FeynML file.
    """
    d = fd
    SCALE = scale
    d.legs[0].with_xy(-SCALE, SCALE)
    d.legs[1].with_xy(-SCALE, -SCALE)
    d.legs[2].with_xy(SCALE, SCALE)
    d.legs[3].with_xy(SCALE, -SCALE)
    d = feynman_adjust_points(d, size=15, clear_vertices=False)
    auto_bend(d)
    auto_label(d.propagators)
    auto_label(d.legs)
    return d
