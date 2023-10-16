import pytest
from pathlib import Path
from gama_config.gama_gs import read_gs_config, GamaGsConfig, Mode, LogLevel, Network
from gama_config.test.helpers import write_temp_file


def test_read_gs_config_works():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "log_level: info",
            "mode: none",
            "network: shared",
            "prod: false",
            "remote_cmd_override: false",
        ]
    )
    config_file = write_temp_file(config_string)

    config = read_gs_config(config_file)

    assert config == GamaGsConfig(
        ddsrouter_groundstation_ip=None,
        ddsrouter_groundstation_port=None,
        ddsrouter_vessel_ip=None,
        ddsrouter_vessel_port=None,
        log_level=LogLevel.INFO,
        mode=Mode.NONE,
        network=Network.SHARED,
        prod=False,
        remote_cmd_override=False,
    )


def test_throws_if_file_not_found():
    with pytest.raises(FileNotFoundError, match="Could not find config file"):
        read_gs_config(Path("does_not_exist.yaml"))


def test_throws_if_file_cannot_be_parsed():
    config_file = write_temp_file("")

    with pytest.raises(ValueError, match="Could not parse config file"):
        read_gs_config(config_file)


def test_throws_if_mode_does_not_match_enum():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "log_level: info",
            "mode: goblin",
            "network: shared",
            "prod: false",
            "remote_cmd_override: false",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(ValueError, match="'goblin' is not a valid Mode"):
        read_gs_config(config_file)


def test_throws_if_network_does_not_match_enum():
    config_string = "\n".join(
        [
            "ddsrouter_groundstation_ip: null",
            "ddsrouter_groundstation_port: null",
            "ddsrouter_vessel_ip: null",
            "ddsrouter_vessel_port: null",
            "log_level: info",
            "mode: none",
            "network: starlink",
            "prod: false",
            "remote_cmd_override: false",
        ]
    )
    config_file = write_temp_file(config_string)

    with pytest.raises(ValueError, match="'starlink' is not a valid Network"):
        read_gs_config(config_file)
