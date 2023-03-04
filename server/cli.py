from argparse import ArgumentParser
from configparser import ConfigParser


def parse_arguments():
    parser = ArgumentParser("URL Shortener instance")
    parser.add_argument(
        "--configuration-file",
        type=str,
        default="server/configuration.ini",
        help="Path configuration file"
    )
    return parser.parse_args()


def get_configuration():
    args = parse_arguments()
    ret = ConfigParser()
    ret.read(args.configuration_file)
    return ret
