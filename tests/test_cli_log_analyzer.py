import argparse
from pathlib import Path
import pytest

from cli_log_analyzer.dataclass import NginxLog
from cli_log_analyzer.log_analyzer import check_file, extract_data, data_formater
from cli_log_analyzer.utilities import analyze_data


def test_check_dirs_exist(tmp_path: Path):
    log_file = tmp_path / "test.log"
    log_file.touch()

    args = argparse.Namespace(log_file=str(log_file))

    result = check_file(args)

    assert result == log_file
    assert result.exists()


@pytest.mark.parametrize(
    "file_content, expected_result",
    [
        (
            '192.168.1.1 - - [10/Jan/2024:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1024',
            ["192.168.1.1 - - [10/Jan/2024:13:55:36 +0000] \"GET /index.html HTTP/1.1\" 200 1024"]
        ),
    ]
)
def test_check_extract_data(tmp_path: Path, file_content, expected_result: list[str]):
    log_file = tmp_path / "test.log"
    log_file.write_text(file_content, encoding="utf-8")

    result = extract_data(log_file)

    assert result == expected_result


@pytest.mark.parametrize(
    "file_content, expected_result",
    [
        (
            [
                "10.10.10.10 - - [10/Feb/2024:17:40:30 +0000] \"POST /api/register HTTP/1.1\" 201 1024",
                "192.168.1.1 - - [10/Jan/2024:13:55:36 +0000] \"GET /index.html HTTP/1.1\" 200 1024",
            ],
            [
                NginxLog(
                    ip="10.10.10.10",
                    timestamp="10/Feb/2024:17:40:30 +0000",
                    method="POST",
                    path_="/api/register ",
                    status=201,
                    response_size=1024,
                ),
                NginxLog(
                    ip="192.168.1.1",
                    timestamp="10/Jan/2024:13:55:36 +0000",
                    method="GET",
                    path_="/index.html ",
                    status=200,
                    response_size=1024,
                ),
            ],
        ),
    ]
)
def test_data_formater(file_content: list[str], expected_result: list[NginxLog]):
    result = data_formater(file_content)

    assert result == expected_result


@pytest.mark.parametrize(
    "file_content, expected_result",
    [
        (
            [
                " - - \"POST /api/register HTTP/1.1\" 201 1024",
            ],
            AttributeError,
        ),
        (
            [
                "192.168.1.1 - - [10/Jan/2024:13:55:36 +0000] \" HTTP/1.1\" 200",
            ],
            AttributeError,
        ),
    ]
)
def test_invalid_data_formater(file_content: list[str], expected_result: Exception):
    with pytest.raises(expected_result):
        data_formater(file_content)


@pytest.mark.parametrize(
    "test_data, expected_avg_size, expected_top_ips, expected_client_errors, expected_server_errors",
    [
        (
            [
                NginxLog(
                    ip="192.168.1.1",
                    timestamp="10/Feb/2024:13:55:36 +0000",
                    method="GET",
                    path_="/index.html ",
                    status=200,
                    response_size=1024,
                ),
                NginxLog(
                    ip="203.0.113.45",
                    timestamp="10/Feb/2024:14:02:15 +0000",
                    method="POST",
                    path_="/api/login ",
                    status=401,
                    response_size=512,
                ),
                NginxLog(
                    ip="172.16.0.23",
                    timestamp="10/Feb/2024:14:30:10 +0000",
                    method="GET",
                    path_="/dashboard ",
                    status=500,
                    response_size=2048,
                ),
            ],
            1194.67,
            [("192.168.1.1", 1), ("203.0.113.45", 1), ("172.16.0.23", 1)],
            [(401, 1)],
            [(500, 1)],
        ),
    ]
)
def test_analyze_data_logging(
        mocker,
        test_data: list[NginxLog],
        expected_avg_size: float,
        expected_top_ips: list[tuple],
        expected_client_errors: list[tuple],
        expected_server_errors: list[tuple],
):
    mock_logger = mocker.patch("cli_log_analyzer.utilities.logging")

    analyze_data(test_data)

    mock_logger.info.assert_any_call(f"Average weight of responses: {expected_avg_size}")
    mock_logger.info.assert_any_call(f"Top 5 IP requests: {expected_top_ips}")
    mock_logger.info.assert_any_call(f"Top 3 client errors: {expected_client_errors}")
    mock_logger.info.assert_any_call(f"Top 3 server errors: {expected_server_errors}")
