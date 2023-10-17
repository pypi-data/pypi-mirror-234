""" mcli util command """
import argparse

from mcli.cli.m_util.util import get_util


def add_util_argparser(subparser: argparse._SubParsersAction,):
    """Adds the util parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """

    util_parser: argparse.ArgumentParser = subparser.add_parser(
        'util',
        aliases=['utilization'],
        help='Get cluster utilization',
    )

    util_parser.add_argument(
        'clusters',
        help='Which cluster would you like to get utilization for?',
        nargs='*',
    )

    util_parser.add_argument(
        '--hide-users',
        action='store_true',
        help='Do not show the by user utilization breakdown',
    )

    training_or_inference = util_parser.add_mutually_exclusive_group()

    training_or_inference.add_argument(
        '-t',
        '--training',
        help='Only view training utilization',
        action='store_true',
    )

    training_or_inference.add_argument(
        '-i',
        '--inference',
        help='Only view inference utilization',
        action='store_true',
    )

    util_parser.set_defaults(func=get_util)
    return util_parser
