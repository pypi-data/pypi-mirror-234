import pytest
from pathlib import Path
from gama_config.gama_vessel import (
    read_vessel_config,
    GamaVesselConfig,
    GamaVesselGreenstream,
    Pipeline,
    GamaVesselConfigExtensions,
    Mode,
    Variant,
    LogLevel,
    Network,
)
from gama_config.test.helpers import write_temp_file


def test_read_vessel_config_works():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "extensions:",
            "  groot: false",
            "  lookout: false",
            "  rviz: false",
            "greenstream:",
            "  pipeline_overrides: null",
            "log_level: info",
            "mode: stubs",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: educat",
        ]
    )
    config_file = write_temp_file(config_string)

    config = read_vessel_config(config_file)

    assert config == GamaVesselConfig(
        ddsrouter_groundstation_ip=None,
        ddsrouter_groundstation_port=None,
        ddsrouter_vessel_ip=None,
        ddsrouter_vessel_port=None,
        extensions=GamaVesselConfigExtensions(
            groot=False,
            lookout=False,
            rviz=False,
        ),
        greenstream=GamaVesselGreenstream(
            pipeline_overrides=None,
        ),
        log_level=LogLevel.INFO,
        mode=Mode.STUBS,
        network=Network.HOST,
        prod=False,
        ubiquity_ip="",
        ubiquity_pass="",
        ubiquity_user="",
        variant=Variant.EDUCAT,
    )


def test_reads_greenstream_pipeline_overrides():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "extensions:",
            "  groot: false",
            "  lookout: false",
            "  rviz: false",
            "greenstream:",
            "  pipeline_overrides:",
            "  - null",
            "  - name: bow",
            "    elements:",
            "    - v4l2src",
            "    - video/x-raw, format=RGB,width=1920,height=1080",
            "log_level: info",
            "mode: stubs",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: educat",
        ]
    )
    config_file = write_temp_file(config_string)

    config = read_vessel_config(config_file)

    assert config == GamaVesselConfig(
        ddsrouter_groundstation_ip=None,
        ddsrouter_groundstation_port=None,
        ddsrouter_vessel_ip=None,
        ddsrouter_vessel_port=None,
        extensions=GamaVesselConfigExtensions(
            groot=False,
            lookout=False,
            rviz=False,
        ),
        greenstream=GamaVesselGreenstream(
            pipeline_overrides=[
                None,
                Pipeline(
                    name="bow",
                    order=None,
                    elements=["v4l2src", "video/x-raw, format=RGB,width=1920,height=1080"],
                ),
            ],
        ),
        log_level=LogLevel.INFO,
        mode=Mode.STUBS,
        network=Network.HOST,
        prod=False,
        ubiquity_ip="",
        ubiquity_pass="",
        ubiquity_user="",
        variant=Variant.EDUCAT,
    )


def test_throws_if_file_not_found():
    with pytest.raises(FileNotFoundError, match="Could not find config file"):
        read_vessel_config(Path("does_not_exist.yaml"))


def test_throws_if_file_cannot_be_parsed():
    config_file = write_temp_file("")

    with pytest.raises(ValueError, match="Could not parse config file"):
        read_vessel_config(config_file)


def test_throws_if_mode_does_not_match_enum():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "extensions:",
            "  groot: false",
            "  lookout: false",
            "  rviz: false",
            "greenstream:",
            "  pipeline_overrides: null",
            "log_level: info",
            "mode: goblin",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: educat",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(ValueError, match="'goblin' is not a valid Mode"):
        read_vessel_config(config_file)


def test_throws_if_variant_does_not_match_enum():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "extensions:",
            "  groot: false",
            "  lookout: false",
            "  rviz: false",
            "greenstream:",
            "  pipeline_overrides: null",
            "log_level: info",
            "mode: stubs",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: killer-robot",
        ]
    )

    config_file = write_temp_file(config_string)

    with pytest.raises(ValueError, match="'killer-robot' is not a valid Variant"):
        read_vessel_config(config_file)


def test_throws_if_greenstream_config_is_bad():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "extensions:",
            "  groot: false",
            "  lookout: false",
            "  rviz: false",
            "greenstream:",
            "  pipeline_overrides:",
            "  - null",
            "  - elements:",  # This is missing a name
            "    - v4l2src",
            "    - video/x-raw, format=RGB,width=1920,height=1080",
            "log_level: info",
            "mode: stubs",
            "network: host",
            "prod: false",
            "ubiquity_ip: ''",
            "ubiquity_pass: ''",
            "ubiquity_user: ''",
            "variant: educat",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(
        ValueError, match='missing value for field "greenstream.pipeline_overrides.name"'
    ):
        read_vessel_config(config_file)
