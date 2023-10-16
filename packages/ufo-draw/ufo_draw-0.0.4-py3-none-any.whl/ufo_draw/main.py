import argparse

import feynml
from feynmodel.interface.qgraf import feynmodel_to_qgraf, qgraf_to_feynmodel
from feynmodel.interface.ufo import load_ufo_model
from pyfeyn2.auto.diagram import auto_diagram
from pyfeyn2.render.latex.tikzfeynman import TikzFeynmanRender
from pyqgraf import qgraf

from ufo_draw.ufo_diagrams import generate_diagrams


def main():
    # parse command line options with argparse
    parser = argparse.ArgumentParser(
        prog="ufo-draw.ufo_draw",
        description="Draw FeynML diagrams from ufo models with pyfeyn2.",
    )
    parser.add_argument(
        "-p",
        "-m",
        "--path",
        "--model",
        type=str,
        default="ufo_sm",
        help="Path to UFO model directory.",
    )
    parser.add_argument(
        "-l",
        "--loops",
        type=int,
        default=0,
        help="Number of loops to draw.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="diagram",
        help="Output file name without suffix.",
    )
    # argument list of incoming particles
    parser.add_argument(
        "-i",
        "--initial",
        type=str,
        default="e- e+",
        help="Incoming particles.",
    )
    # argument list of outgoing particles
    parser.add_argument(
        "-f",
        "--final",
        type=str,
        default="e- e+",
        help="Outgoing particles.",
    )
    parser.add_argument(
        "--fml",
        action="store_true",
        help="Output FeynML.",
        default=False,
    )
    # TODO convert general particle input to less general particle input
    # TODO filter orders
    # TODO filter propagators

    # TODO show option?

    args = parser.parse_args()

    fml = generate_diagrams(
        args.path, args.initial.split(" "), args.final.split(" "), args.loops
    )

    # Render diagrams
    for i, d in enumerate(fml.diagrams):
        auto_diagram(d)
        t = TikzFeynmanRender(d)
        t.render(show=True, file=args.output + f"_{i}")
    # Write FML
    if args.fml:
        s = fml.to_xml()
        # print s to args.output + ".fml"
        with open(args.output + ".fml", "w") as f:
            f.write(s)
