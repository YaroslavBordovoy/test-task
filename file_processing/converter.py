import argparse
from pathlib import Path

from lxml import etree

from file_processing.arg_parser import get_args
from file_processing.validators import (
    id_validator,
    price_validator,
    string_validator,
)


def check_dirs(args: argparse.Namespace) -> tuple[Path, Path]:
    source_file = Path(args.input_dir)

    if not source_file.is_file():
        raise FileNotFoundError("The file was not found in this directory.")

    target_file = Path(args.output_dir)

    if target_file.exists() and target_file.is_dir():
        raise FileExistsError("The path points to a directory, not a file.")

    target_file.touch(exist_ok=True)

    return source_file, target_file


def check_tag(data: etree._Element, tag: str) -> str:
    tag_element = data.find(tag)

    if not tag_element or not tag_element.text.strip():
        raise ValueError(f"Missing or empty <{tag}> tag.")

    return tag_element.text.strip()


def extract_data(path: Path) -> dict:
    with open(path, "r") as file:
        raw_data = file.read()

        processed_data = etree.fromstring(raw_data)

        id_ = int(check_tag(processed_data, "id"))
        name = check_tag(processed_data, "name")
        price = float(check_tag(processed_data, "price"))
        category = check_tag(processed_data, "category")

        id_validator(id_)
        price_validator(price)
        string_validator(name)
        string_validator(category)

        return {
            "id": id_,
            "name": name,
            "price": price,
            "category": category,
        }


def main(args: argparse.Namespace):
    source_file, target_file = check_dirs(args)
    extracted_data = extract_data(source_file)


if __name__ == "__main__":
    args = get_args()
    main(args)
