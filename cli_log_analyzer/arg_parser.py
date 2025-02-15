import argparse


parser = argparse.ArgumentParser(
    prog="NginxParser",
    description="Reads the name of the log file",
)
parser.add_argument(
    "log_file",
    type=str,
    default="cli_log_analyzer/access.log",
    help="Source directory with Nginx data",
)


def get_args():
    return parser.parse_args()
