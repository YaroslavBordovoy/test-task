import argparse


parser = argparse.ArgumentParser(
    prog="TerminalParser",
    description="Converting xml data to json",
)
parser.add_argument(
    "--input-dir",
    type=str,
    default="file_processing/input_data.xml",
    help="Source directory with xml data",
)
parser.add_argument(
    "--output-dir",
    type=str,
    default="file_processing/output_data.json",
    help="Target directory with json data",
)


def get_args():
    return parser.parse_args()
