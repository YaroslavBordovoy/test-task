import argparse
from pathlib import Path

import pytest
from lxml import etree

from file_processing.converter import check_dirs
from file_processing.converter import extract_data, check_tag


def test_check_dirs_exist(tmp_path: Path):
    args = argparse.Namespace(
        input_dir=str(tmp_path / "input.xml"),
        output_dir=str(tmp_path / "output.json"),
    )

    Path(args.input_dir).touch()

    input_path, output_path = check_dirs(args)

    assert input_path == Path(args.input_dir)
    assert output_path == Path(args.output_dir)
    assert output_path.exists()


@pytest.mark.parametrize(
    "file_content, expected_result",
    [
        (
            "<product><id>1</id><name>Smartphone</name><price>599.99</price><category>Electronics</category></product>",
            {"id": 1, "name": "Smartphone", "price": 599.99, "category": "Electronics"}
        ),
    ]
)
def test_extract_data_valid_data(tmp_path: Path, file_content: str, expected_result: dict):
    xml_file = tmp_path / "test.xml"
    xml_file.write_text(file_content, encoding="utf-8")

    result = extract_data(xml_file)

    assert result == expected_result


@pytest.mark.parametrize(
    "file_content, expected_result",
    [
        (
            "<product><id>1<name>Smartphone</name><price>599.99</price><category>Electronics</category></product>",
            ValueError,
        ),
    ]
)
def test_extract_data_without_id_tag(tmp_path: Path, file_content: str, expected_result: Exception):
    xml_file = tmp_path / "test.xml"
    xml_file.write_text(file_content, encoding="utf-8")

    with pytest.raises(expected_result):
        extract_data(xml_file)


@pytest.mark.parametrize(
    "file_content, expected_result",
    [
        (
            "<product><name>Smartphone</name><price>599.99</price><category>Electronics</category></product>",
            ValueError,
        ),
        (
            "<product><id>2</id><price>599.99</price><category>Electronics</category></product>",
            ValueError,
        ),
        (
            "<product><id>2</id><name>Smartphone</name><price>599.99</price></product>",
            ValueError,
        ),
    ]
)
def test_check_invalid_data(tmp_path: Path, file_content: str, expected_result: Exception):
    xml_file = tmp_path / "test.xml"
    xml_file.write_text(file_content, encoding="utf-8")

    with pytest.raises(expected_result):
        extract_data(xml_file)


@pytest.mark.parametrize(
    "xml_content, tag, expected_result",
    [
        (
            "<product><id>1</id><name>Smartphone</name><price>599.99</price><category>Electronics</category></product>",
            "id",
            "1",
        ),
        (
            "<product><id>1</id><name>Smartphone</name><price>599.99</price><category>Electronics</category></product>",
            "name",
            "Smartphone",
        ),
        (
            "<product><id>1</id><name>Smartphone</name><price>599.99</price><category>Electronics</category></product>",
            "price",
            "599.99",
        ),
    ]
)
def test_check_valid_tag(xml_content: str, tag: str, expected_result: str):
    data = etree.fromstring(xml_content)
    result = check_tag(data, tag)

    assert result == expected_result


@pytest.mark.parametrize(
    "xml_content, tag, expected_result",
    [
        (
            "<product><name>Smartphone</name><price>599.99</price><category>Electronics</category></product>",
            "id",
            ValueError,
        ),
        (
            "<product><id>1</id><price>599.99</price><category>Electronics</category></product>",
            "name",
            ValueError,
        ),
        (
            "<product><id>1</id><name>Smartphone</name><category>Electronics</category></product>",
            "price",
            ValueError,
        ),
    ]
)
def test_check_invalid_tag(xml_content: str, tag: str, expected_result: Exception):
    data = etree.fromstring(xml_content)

    with pytest.raises(expected_result):
        check_tag(data, tag)
