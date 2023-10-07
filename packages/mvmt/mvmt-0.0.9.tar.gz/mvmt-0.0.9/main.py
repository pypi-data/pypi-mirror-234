import os, sys

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
sys.path.append(os.path.dirname(f"{dname}/src/"))

from src.mvmt import tableau, utils
import argparse
from PrettyPrint import PrettyPrintTree


def main(args):
    H = utils.construct_heyting_algebra(
        file_path=f"{dname}/algebra_specs/{args.algebra}"
    )
    valid, tab = tableau.isValid(args.expression, H)
    print(f"{args.expression} is valid: {valid}")
    if args.print_tableau:
        pt = PrettyPrintTree(
            lambda x: x.children,
            lambda x: str(x.signed_formula),
            lambda x: f"<{x.world}, {x.relation}>",
        )
        pt(tab.root)

    if not valid and args.display_model:
        M = tableau.construct_counter_model(args.expression, H, tab)
        tableau.visualize_model(M)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("expression", default="p")
    parser.add_argument(
        "-a",
        "--algebra",
        help="Name of json file inspecifying the Heyting algebra (default: three_valued.json)",
        default="three_valued.json",
    )
    parser.add_argument(
        "-t",
        "--print_tableau",
        help="Enables printing the tableau",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--display_model",
        help="Enables displaying a counter model (if it exists)",
        action="store_true",
    )
    args = parser.parse_args()
    main(args)
