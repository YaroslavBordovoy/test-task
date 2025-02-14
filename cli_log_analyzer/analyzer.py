from pathlib import Path
import re
from cli_log_analyzer.dataclass import NginxLog


PATH_TO_LOG_FILE = Path(__file__).parent / "nginx.log"


def extract_data(input_path: Path) -> list[str]:
    with open(input_path, "r") as file:
        data = file.readlines()

        return data


def data_formater(data: list[str]) -> list[NginxLog]:
    # for element in data:
    #     print(element.split())

    element = data[0]
    print(element)

    id_ = re.search(r"\d+.\d+.\d+.\d+", element).group(0)
    timestamp = re.search(r"\d+/\w{3}/\d+:\d+:\d+:\d+ [+-]\d+", element).group(0)
    method = re.search(r'"([A-Z]{3,10}) ', element).group(1)

    print(f"ID - {id_}")
    print(f"Timestamp - {timestamp}")
    print(f"Method - {method}")


def main(input_path: Path) -> None:
    if not input_path:
        raise FileNotFoundError("File path not passed.")

    raw_data = extract_data(input_path)
    processed_data = data_formater(raw_data)


if __name__ == "__main__":
    main(PATH_TO_LOG_FILE)