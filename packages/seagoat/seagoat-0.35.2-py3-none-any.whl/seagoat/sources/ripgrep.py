import re
import subprocess
from pathlib import Path

import orjson

from seagoat.repository import Repository
from seagoat.result import Result
from seagoat.sources.chroma import MAXIMUM_VECTOR_DISTANCE
from seagoat.utils.file_types import is_file_type_supported


def _fetch(query_text: str, path: str, limit: int):
    query_text = re.sub(r"\s+", "|", query_text)
    files = {}

    cmd = [
        "rg",
        "--json",
        "--max-count",
        str(limit),
        "--ignore-case",
        "--max-filesize",
        "200K",
        query_text,
        path,
    ]

    try:
        rg_output = subprocess.check_output(cmd, encoding="utf-8")
    except subprocess.CalledProcessError as exception:
        rg_output = exception.output

    for line in rg_output.splitlines():
        result = orjson.loads(line)

        if result.get("type") == "match":
            result_data = result["data"]
            absolute_path = result_data["path"]["text"]
            relative_path = Path(absolute_path).relative_to(path)
            line_number = int(result_data["line_number"])

            if not is_file_type_supported(relative_path):
                continue

            if relative_path not in files:
                files[relative_path] = Result(str(relative_path), absolute_path)

            # This is so that ripgrep results are on comparable levels with chroma results
            files[relative_path].add_line(line_number, MAXIMUM_VECTOR_DISTANCE * 0.8)

    return files.values()


def initialize(repository: Repository):
    path = repository.path

    def fetch(query_text: str, limit: int):
        return _fetch(query_text, str(path), limit)

    def cache_chunk(_):
        # Ripgrep does not need a cache for chunks
        pass

    return {
        "fetch": fetch,
        "cache_chunk": cache_chunk,
    }
