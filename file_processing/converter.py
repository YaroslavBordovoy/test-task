import argparse
from pathlib import Path

from lxml import etree

from file_processing.arg_parser import get_args
from file_processing.json_saver import save_to_json
from file_processing.validators import (
    id_validator,
    price_validator,
    string_validator,
)


def check_dirs(args: argparse.Namespace) -> tuple[Path, Path]:
    """
    Validates and prepares input and output paths for processing.

    Args:
        args (argparse.Namespace):
            Parsed command-line arguments containing input and output file paths.

    Returns:
        tuple[Path, Path]:
            A tuple containing the validated source file path and target file path.

    Raises:
        FileNotFoundError:
            If the specified input file does not exist.
        FileExistsError:
            If the specified output path is a directory instead of a file.
    """
    source_file = Path(args.input_dir)

    if not source_file.is_file():
        raise FileNotFoundError("The file was not found in this directory.")

    target_file = Path(args.output_dir)

    if target_file.exists() and target_file.is_dir():
        raise FileExistsError("The path points to a directory, not a file.")

    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.touch(exist_ok=True)

    return source_file, target_file


def check_tag(data: etree._Element, tag: str) -> str:
    """
    Extracts and validates the text content of a specified XML tag.

    Args:
        data (etree._Element): The parsed XML data structure.
        tag (str): The name of the XML tag to extract.

    Returns:
        str: The text content of the tag if present and non-empty.

    Raises:
        ValueError:
            If the specified tag is missing or contains empty content.
    """
    tag_element = data.find(tag)

    if tag_element is None or not tag_element.text.strip():
        raise ValueError(f"Missing or empty <{tag}> tag.")

    return tag_element.text.strip()


def extract_data(path: Path) -> dict:
    """
    Extracts and validates structured data from an XML file.

    Args:
        path (Path): The file path to the XML file containing the data.

    Returns:
        dict: A dictionary containing validated fields: 'id', 'name', 'price', 'category'.

    Raises:
        ValueError: If any required XML tag is missing or empty.
        etree.XMLSyntaxError: If the XML file has syntax errors or is malformed.
    """
    with open(path, "r") as file:
        raw_data = file.read()

        try:
            processed_data = etree.fromstring(raw_data)
        except etree.XMLSyntaxError:
            raise ValueError("Invalid XML structure.")

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


def main(args: argparse.Namespace) -> None:
    """
    Main function to process XML data and save it as JSON.

    Args:
        args (argparse.Namespace):
            Parsed command-line arguments containing input and output file paths.

    Returns:
        None
    """
    source_file, target_file = check_dirs(args)
    extracted_data = extract_data(source_file)
    save_to_json(data=extracted_data, output_path=target_file)


if __name__ == "__main__":
    args = get_args()
    main(args)
