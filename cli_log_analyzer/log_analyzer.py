import argparse
import re
from pathlib import Path

from cli_log_analyzer.arg_parser import get_args
from cli_log_analyzer.dataclass import NginxLog
from cli_log_analyzer.utilities import analyze_data


def check_file(args: argparse.Namespace) -> Path:
    """
    Verifies the existence of the log file and returns its absolute path.

    Args:
        args (argparse.Namespace):
            Parsed command-line arguments containing the log file path.

    Returns:
        Path: Resolved absolute path to the log file.

    Raises:
        FileNotFoundError: If the specified log file does not exist.
    """
    source_file = Path(args.log_file).resolve()

    if not source_file.is_file():
        raise FileNotFoundError(f"The file {args.log_file} was not found.")

    return source_file


def extract_data(input_path: Path) -> list[str]:
    """
    Reads log file content and returns a list of log entries.

    Args:
        input_path (Path): Path to the log file.

    Returns:
        list[str]:
            A list of log entries, each representing a single line from the log file.
    """
    with open(input_path, "r") as file:
        data = file.readlines()

        return data


def data_formater(data: list[str]) -> list[NginxLog]:
    """
    Parses raw log data and converts it into structured NginxLog instances.

    Args:
        data (list[str]): A list of log entries.

    Returns:
        list[NginxLog]: A list of NginxLog objects, each containing structured log data.

    Raises:
        AttributeError: If a log entry does not match the expected format.
    """
    entity_list = []

    try:
        for element in data:
            entity_list.append(
                NginxLog(
                    ip=re.search(r"\d+.\d+.\d+.\d+", element).group(0),
                    timestamp=re.search(r"\d+/\w{3}/\d+:\d+:\d+:\d+ [+-]\d+", element).group(0),
                    method = re.search(r'"([A-Z]{3,10}) ', element).group(1),
                    path_ = re.search(r"/[\w./?=&-]* ", element).group(0),
                    status = int(re.search(r'" (\d{3}) ', element).group(1)),
                    response_size = int(re.search(r"\d+$", element).group(0)),
                )
            )
    except AttributeError as error:
        raise AttributeError(f"An unexpected error occurred: {error}")

    return entity_list


def main(args: argparse.Namespace) -> None:
    """
    Main function that orchestrates log file processing and analysis.

    Args:
        args (argparse.Namespace):
            Parsed command-line arguments containing the log file path.

    Returns:
        None
    """
    access_file = check_file(args)

    raw_data = extract_data(access_file)
    processed_data = data_formater(raw_data)
    analyze_data(processed_data)


if __name__ == "__main__":
    args = get_args()
    main(args)
