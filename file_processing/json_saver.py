import json
from pathlib import Path


def save_to_json(data: dict, output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
