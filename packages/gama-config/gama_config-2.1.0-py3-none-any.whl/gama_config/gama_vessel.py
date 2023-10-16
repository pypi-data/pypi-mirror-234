# IMPORTANT
# After changing this file, run `python3 -m gama_config.generate_schemas`
# To re-generate the json schemas

from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from dacite import from_dict, Config
from typing import Optional, Any, List, Annotated
from gama_config import LogLevel
from gama_config.helpers import write_config, read_config, find_gama_config, join_lines
from dc_schema import SchemaAnnotation


GAMA_VESSEL_FILE_NAME = "gama_vessel.yml"
GAMA_VESSEL_SCHEMA_URL = (
    "https://greenroom-robotics.github.io/gama/schemas/gama_vessel.schema.json"
)


class Mode(str, Enum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"
    STUBS = "stubs"


class Network(str, Enum):
    SHARED = "shared"
    VPN = "vpn"
    HOST = "host"


class Variant(str, Enum):
    WHISKEY_BRAVO = "whiskey_bravo"
    EDUCAT = "educat"
    ORACLE_2_2 = "oracle_2_2"
    ORACLE_22 = "oracle_22"


@dataclass
class GamaVesselConfigExtensions:
    lookout: bool = False
    rviz: bool = False
    groot: bool = False


@dataclass
class Pipeline:
    # This will become the name of frame-id, ros topic and webrtc steam
    name: str
    # Used to order the stream in the UI
    order: Optional[int]
    # An array of gstream source / transform elements
    # eg)
    # ["v4l2src", "video/x-raw, format=RGB,width=1920,height=1080"]
    elements: List[str]


@dataclass
class GamaVesselGreenstream:
    pipeline_overrides: Annotated[
        Optional[List[Optional[Pipeline]]],
        SchemaAnnotation(
            description=join_lines(
                "A list of greenstream pipelines.",
                "These will only take affect if the the mode is 'hardware'",
                "",
                "Set these to 'null' to ignore the override.",
            ),
            examples=[
                join_lines(
                    "- null",
                    "- name: bow",
                    "  elements:",
                    "  - v4l2src",
                    "  - video/x-raw, format=RGB,width=1920,height=1080",
                )
            ],
        ),
    ] = None


@dataclass
class GamaVesselConfig:
    ros_domain_id: int = 0
    namespace_vessel: str = "vessel"
    namespace_groundstation: str = "groundstation"
    variant: Variant = Variant.WHISKEY_BRAVO
    mode: Mode = Mode.SIMULATOR
    extensions: GamaVesselConfigExtensions = field(default_factory=GamaVesselConfigExtensions)
    network: Network = Network.SHARED
    prod: bool = False
    log_level: LogLevel = LogLevel.INFO
    ubiquity_user: Optional[str] = None
    ubiquity_pass: Optional[str] = None
    ubiquity_ip: Optional[str] = None
    ddsrouter_groundstation_ip: Optional[str] = None
    ddsrouter_groundstation_port: Optional[str] = None
    ddsrouter_vessel_ip: Optional[str] = None
    ddsrouter_vessel_port: Optional[str] = None
    greenstream: GamaVesselGreenstream = field(default_factory=GamaVesselGreenstream)


def parse_vessel_config(config: dict[str, Any]) -> GamaVesselConfig:
    return from_dict(
        GamaVesselConfig,
        config,
        config=Config(cast=[Mode, Network, Variant, LogLevel]),
    )


def get_vessel_config_path():
    return find_gama_config() / GAMA_VESSEL_FILE_NAME


def read_vessel_config(path: Optional[Path] = None) -> GamaVesselConfig:
    return read_config(path or get_vessel_config_path(), parse_vessel_config)


def write_vessel_config(config: GamaVesselConfig):
    return write_config(get_vessel_config_path(), config, GAMA_VESSEL_SCHEMA_URL)
