"""
Main command-line interface
"""
import sys

from imxdparser import ChildParser, MainParser

from . import clone, validate


def _parser_error(parser, argv, *_args):
    """
    Reparse with an additional parameter to force an error
    """
    argv += [""]
    parser.parse_args(argv)


def _options(argv=None):
    """
    Prepare an intermixed argparser. Command line argument positions
    is a bit more flexible.
    """
    if argv is None:
        argv = sys.argv[1:]

    def error(*_args):
        _parser_error(parser, argv)

    parser = MainParser(description="Lorem ipsum sit dolor amet")
    parser.add_argument("--version", action="version", version="1.1.0")
    parser.attach()
    parser.set_defaults(func=error)

    subparser = ChildParser(parser, "version")
    subparser.attach()
    subparser.set_defaults(func=lambda *_: print("1.1.0"))

    subparser = ChildParser(parser, "validate")
    # fmt: off
    subparser.add_argument("template", metavar="TEMPLATE", help="Path of a 'scaffold.yml' template file")
    # fmt: on
    subparser.attach()
    subparser.set_defaults(func=validate.validate)

    subparser = ChildParser(parser, "clone")
    # fmt: off
    subparser.add_argument("-i", "--input-file", metavar="FILE", help="Location of a yaml input file with answers to the questions")
    subparser.add_argument("-o", "--output-dir", default=".", metavar="PATH", help="Where to output the generated files")
    subparser.add_argument("template", metavar="TEMPLATE", help="Path of a 'scaffold.yml' template file")
    # fmt: on
    subparser.attach()
    subparser.set_defaults(func=clone.clone)

    return vars(parser.parse_args(argv))


def main():
    args = _options()
    if args.get("func"):
        func = args.pop("func")
        func(args)
