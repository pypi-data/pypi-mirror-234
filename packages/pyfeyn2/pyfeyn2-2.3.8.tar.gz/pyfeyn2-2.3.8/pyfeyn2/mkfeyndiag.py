# TODO read in FeynMF and produce pdf output allowing to choose renderer
import argparse
import importlib
from pathlib import Path

import cssutils
from feynml.feynml import FeynML
from xsdata.formats.dataclass.parsers import XmlParser

import pyfeyn2.render.all as renderall
from pyfeyn2.render.text.ascii import ASCIIRender
from pyfeyn2.render.text.unicode import UnicodeRender


def main(argv=None):
    # parse command line options with argparse
    parser = argparse.ArgumentParser(
        prog="pyfeyn2.mkfeyndiag",
        description="Draw FeynML diagrams with pyfeyn2.",
    )
    parser.add_argument(
        "input",
        metavar="INPUT",
        type=str,
        help="Input FeynML file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT",
        default="output.pdf",
        type=str,
        help="Output file.",
    )
    parser.add_argument(
        "-r",
        "--renderer",
        metavar="RENDERER",
        default=None,
        type=str,
        help="Renderer to use.",
    )
    parser.add_argument(
        "--style",
        metavar="STYLE",
        default=None,
        type=str,
        help="CSS like Style file to use.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the output file.",
    )
    parser.add_argument(
        "--diagram",
        metavar="DIAGRAM",
        default=None,
        type=str,
        help="Diagram id to render.",
    )

    args = parser.parse_args(argv)

    arenderer = args.renderer
    renderer = None
    renderer = renderall.renderer_from_string(arenderer)

    xml_string = Path(args.input).read_text()
    parser = XmlParser()
    fml = parser.from_string(xml_string, FeynML)

    if renderer is None:
        arenderer = fml.head.get_meta_dict()["renderer"]
        renderer = renderall.renderer_from_string(arenderer)
    if args.style is not None:
        style_string = Path(args.style).read_text()
        for diagram in fml.diagrams:
            diagram.external_sheet = cssutils.parseString(style_string)

    for i, d in enumerate(fml.diagrams):
        if args.diagram is None or args.diagram == d.id:
            renderer(d).render(file=args.output + f"_{i}", show=args.show)
