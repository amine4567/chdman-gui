import json
import os
from pathlib import Path
from typing import Dict


def load_resource(json_relative_path: str) -> Dict:
    this_filepath = Path(os.path.realpath(__file__))
    with open(
        this_filepath.parent / "resources" / (json_relative_path + ".json"), "r"
    ) as fp:
        loaded_data = json.load(fp)

    return loaded_data
