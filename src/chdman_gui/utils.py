import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List

from chdman_gui.consts import CHDMAN_BIN_PATH


def load_resource(json_relative_path: str) -> Dict:
    this_filepath = Path(os.path.realpath(__file__))
    with open(
        this_filepath.parent / "resources" / (json_relative_path + ".json"), "r"
    ) as fp:
        loaded_data = json.load(fp)

    return loaded_data


def get_hd_templates() -> List[Dict]:
    output = (
        subprocess.check_output([CHDMAN_BIN_PATH, "listtemplates"]).decode().strip()
    )
    lines = output.split("\n")
    header = re.split(r"\s{2,}", lines[2].strip())
    data = [dict(zip(header, re.split(r"\s{2,}", line.strip()))) for line in lines[4:]]
    return data
