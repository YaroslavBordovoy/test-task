import argparse
import re
from pathlib import Path

from cli_log_analyzer.arg_parser import get_args
from cli_log_analyzer.dataclass import NginxLog


def check_file(args: argparse.Namespace) -> Path:
    source_file = Path(args.log_file).resolve()

    if not source_file.is_file():
        raise FileNotFoundError(f"The file {args.log_file} was not found.")

    return source_file


def extract_data(input_path: Path) -> list[str]:
    with open(input_path, "r") as file:
        data = file.readlines()

        return data


def data_formater(data: list[str]) -> list[NginxLog]:
    entity_list = []

    try:
        for element in data:
            entity_list.append(
                NginxLog(
                    ip=re.search(r"\d+.\d+.\d+.\d+", element).group(0),
                    timestamp=re.search(r"\d+/\w{3}/\d+:\d+:\d+:\d+ [+-]\d+", element).group(0),
                    method = re.search(r'"([A-Z]{3,10}) ', element).group(1),
                    path_ = re.search(r"/[\w./?=&-]* ", element).group(0),
                    status = re.search(r'" (\d{3}) ', element).group(1),
                    response_size = re.search(r"\d+$", element).group(0),
                )
            )
    except AttributeError as error:
        raise AttributeError(f"An unexpected error occurred: {error}")

    return entity_list


def main(args: argparse.Namespace) -> None:
    access_file = check_file(args)

    raw_data = extract_data(access_file)
    processed_data = data_formater(raw_data)


if __name__ == "__main__":
    args = get_args()
    main(args)
