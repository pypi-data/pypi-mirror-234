import argparse
import pathlib
from sys import exit
import takenote.__version__


def init_argparse() -> argparse.ArgumentParser:
    help_text = """Create a notes file for the requested 
        week."""

    parser = argparse.ArgumentParser(usage="%(prog)s [OPTIONS]", description=help_text)
    parser.add_argument(
        "-v", "--version", action="version", version=f"{parser.prog} version {takenote.__version__}"
    )
    parser.add_argument(
        "--notesFolder",
        default=pathlib.Path.home().joinpath("Notes"),
        type=pathlib.Path,
        help="""The root path for the notes folder. 
        If not supplied this defaults to the Notes folder in the users home folder.""",
    )
    parser.add_argument(
        "--editor",
        default="code",
        help="""The editor to open the notes with. 
        If not supplied this defaults 'code' for Visual Studio Code""",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="""The VSCode workspace to open along with the notes. 
        If supplied this overrides the --editor option to 'code' for Visual Studio Code""",
    )
    parser.add_argument(
        "--thisWeek",
        action="store_true",
        default=False,
        help="""Create or open a file dated for Monday of this week.""",
    )
    parser.add_argument(
        "--lastWeek",
        action="store_true",
        default=False,
        help="""Create or open a file dated for Monday of last week.""",
    )
    parser.add_argument(
        "--nextWeek",
        action="store_true",
        default=False,
        help="""Create or open a file dated for Monday of next week.""",
    )
    parser.add_argument(
        "--template",
        default=None,
        help="""The template to use when creating a new file. 
        The file location is relative to the root notes folder.""",
    )

    return parser


def process_args(args):
    parser = init_argparse()
    options = parser.parse_args(args)

    if options.workspace is not None:
        options.editor = "code"

    return options, parser
