from collections import Counter
from pathlib import Path

from cli_log_analyzer.dataclass import NginxLog


def save_result(
        avg_size: float,
        ip_requests: list[tuple],
        client_err: list[tuple],
        server_err: list[tuple],
) -> None:
    target_file = Path("analysis_result.txt")

    with open(target_file, "a", encoding="utf-8") as file:
        file.write(f"Average weight of responses: {avg_size}\n")
        file.write(f"Top 5 IP requests: {ip_requests}\n")
        file.write(f"Top 3 client errors: {client_err}\n")
        file.write(f"Top 3 server errors: {server_err}\n")


def analyze_data(data: list[NginxLog]) -> None:
    total_weight_of_responses = 0
    ip_storage = {}
    client_errors  = {}
    server_errors = {}

    for entity in data:
        total_weight_of_responses += entity.response_size

        ip_storage[entity.ip] = ip_storage.get(entity.ip, 0) + 1

        if 400 <= entity.status < 500:
            client_errors[entity.status] = client_errors.get(entity.status, 0) + 1
        elif 500 <= entity.status < 600:
            server_errors[entity.status] = server_errors.get(entity.status, 0) + 1

    average_weight_of_responses = total_weight_of_responses / len(data) if data else 0
    top_ip_requests = Counter(ip_storage).most_common(5)
    top_client_errors = Counter(client_errors).most_common(3) or "No client errors"
    top_server_errors = Counter(server_errors).most_common(3) or "No server errors"

    save_result(
        avg_size=average_weight_of_responses,
        ip_requests=top_ip_requests,
        client_err=top_client_errors,
        server_err=top_server_errors,
    )

    print(f"Average weight of responses: {average_weight_of_responses}")
    print(f"Top 5 IP requests: {top_ip_requests}")
    print(f"Top 3 client errors: {top_client_errors}")
    print(f"Top 3 server errors: {top_server_errors}")
