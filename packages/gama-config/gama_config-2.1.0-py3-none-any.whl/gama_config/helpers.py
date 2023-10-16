from dataclasses import asdict
from enum import Enum
import yaml
import os
from typing import Any, Callable
from pathlib import Path

type_parse = Callable[[Any], Any]


def join_lines(*lines: str) -> str:
    return "\n".join(lines)


def find_gama_config() -> Path:
    """Returns the path to the .gama directory"""
    return Path.home().joinpath(".config/greenroom")


def dacite_to_dict(obj: Any):
    def dict_factory(data: Any):
        def convert_value(obj: Any):
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return {k: convert_value(v) for k, v in data}

    return asdict(obj, dict_factory=dict_factory)


def write_config(path: Path, config: Any, schema_url: str):
    # Make the parent dir if it doesn't exist
    os.makedirs(path.parent, exist_ok=True)
    with open(path, "w") as stream:
        print(f"Writing: {path}")
        headers = f"# yaml-language-server: $schema={schema_url}"
        data = "\n".join([headers, yaml.dump(dacite_to_dict(config))])
        stream.write(data)


def read_config(path: Path, parse: type_parse):
    try:
        with open(path) as stream:
            return parse(yaml.safe_load(stream))
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find config file: {path}")
    except Exception as e:
        raise ValueError(f"Could not parse config file {path} - {e}")
