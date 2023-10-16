from __future__ import annotations

import argparse
from typing import Sequence

import texcliques.constants as C
from texcliques.commands.extract_references import extract_refs


def get_args() -> argparse.Namespace:
    """Parse the command line arguments."""

    parser = argparse.ArgumentParser(
        description=C.DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter
    )

    # https://stackoverflow.com/a/8521644/812183
    parser.add_argument(
        '-V', '--version', action='version',
        version=f"{C.COLORS['subtle']}%(prog)s {C.VERSION}{C.COLORS['normal']}",
    )

    def add_cmd(name: str, *, help: str) -> argparse.ArgumentParser:
        parser = subparsers.add_parser(name, help=help)
        return parser

    subparsers = parser.add_subparsers(dest='command')

    # 'extract-refs' command
    extract_refs_parser = add_cmd(
        'extract-refs',
        help="Extract the references from a LaTeX file and save them in various"
        " formats. You can specify: "
        " - a --section to extract the references from"
        " - the --fields that you want to extrct from the references."
        " - the output --formats."
    )
    extract_refs_parser.add_argument(
        'file',
        metavar='FILE',
        help='The LaTeX file to extract references from.'
    )
    extract_refs_parser.add_argument(
        'bib',
        metavar='BIB',
        help='The BibTeX file to extract references from.'
    )
    extract_refs_parser.add_argument(
        '-s', '--section',
        metavar='SECTION',
        help='The section to extract references from.'
    )
    extract_refs_parser.add_argument(
        '-p', '--pattern',
        metavar='PATTERN',
        default=r'\\cite[tp]?{([^}]+)}',
        help='The pattern to use for identifying references in the LaTeX file. '
        'The pattern must contain a single capturing group that matches the '
        'reference ID. Defaults to: `%(default)s`.'
    )
    extract_refs_parser.add_argument(
        '--sort',
        action='store_true',
        help='Sort the references in natural order based on their key.'
    )
    extract_refs_parser.add_argument(
        '-o', '--output',
        metavar='OUTPUT',
        default='references',
        help='The base name of the output files.'
    )
    extract_refs_parser.add_argument(
        '--fields',
        metavar='FIELDS',
        nargs='+',
        default=['id', 'title', 'author'],
        help='The fields to extract from the BibTeX file.'
    )
    extract_refs_parser.add_argument(
        '--formats',
        metavar='FORMATS',
        nargs='+',
        default=['toml', 'yaml', 'json'],
        help='The output formats to save the references into. '
        'Supported formats: `toml`, `yaml`, `json`.'
    )

    return parser.parse_args()


def main(argv: Sequence[str] | None = None) -> int:
    args = get_args()

    if args.command == 'extract-refs':
        return extract_refs(args)
    else:
        raise NotImplementedError(f"Command '{args.command}' not implemented.")


if __name__ == '__main__':
    raise SystemExit(main())
