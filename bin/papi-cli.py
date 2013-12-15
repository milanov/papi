"""
PAPI command line interface.
"""

from argparse import ArgumentParser
from papi.project import Papi


def cli():
    """
    Generate api documentation from the command line.

    """

    argparser = ArgumentParser(
        description="PAPI command line interface",
    )

    argparser.set_defaults(
        destination="",
        output_format="html",
        theme="default",
        browser=False,
        format="",
        resources=""
    )

    argparser.add_argument(
        "-d", "--destination", dest="destination",
        help="specify output directory"
    )

    argparser.add_argument(
        "-o", "--output-format", dest="output_format",
        help="Specify output format (html, pdf, ...)"
    )

    argparser.add_argument(
        "-t", "--theme", dest="theme",
        help="Specify a theme"
    )

    argparser.add_argument(
        "-b", "--browser", dest="browser", action="store_true",
        help="Open in browser"
    )

    argparser.add_argument(
        "-f", "--format", dest="format",
        help="Specify docstring parser (restucturedtext, markdown, ...)"
    )

    argparser.add_argument("resources", help="Specify Python resources")

    args = argparser.parse_args()
    args.resources = [m.strip() for m in args.resources.split(",")]

    project = Papi(args)
    project.generate()

    if args.browser:
        project.open_in_browser()

if __name__ == "__main__":
    cli()
