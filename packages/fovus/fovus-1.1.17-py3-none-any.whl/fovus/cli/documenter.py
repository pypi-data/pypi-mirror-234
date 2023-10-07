from fovus.cli.fovus_cli_argument_parser import FovusCliArgumentParser


def get_fovus_parser():
    parser = FovusCliArgumentParser()

    return parser.parser
