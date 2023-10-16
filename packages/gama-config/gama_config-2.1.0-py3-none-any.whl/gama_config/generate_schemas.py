import os
from pathlib import Path
import json
from dc_schema import get_schema
from gama_config.gama_vessel import GamaVesselConfig
from gama_config.gama_gs import GamaGsConfig


def generate_schemas():
    """Generates the schemas for the config files"""
    SCHEMAS_PATH = Path(os.path.dirname(__file__)) / "schemas"
    with open(SCHEMAS_PATH / "gama_vessel.schema.json", "w") as f:
        json.dump(get_schema(GamaVesselConfig), f, indent=2)
    with open(SCHEMAS_PATH / "gama_gs.schema.json", "w") as f:
        json.dump(get_schema(GamaGsConfig), f, indent=2)


if __name__ == "__main__":
    print("Generating schemas...")
    generate_schemas()
