"""
API for fetching static instructions how to build configuration.
"""
from typing import Dict
from pathlib import Path
from ..files.json import read_json
from ..types import Setup, ConfigJson


def index(setup: Setup) -> Dict[str, ConfigJson]:
    """
    Collect and return complete static configuration information.
    """

    def ensure_real_ddim_length(items):
        # items is a list of dicts with optional dimension field
        # if the dimension field exists, it must have length of 2
        # if the dimension field does not exist and tyoe is real it must be [1, 1]
        for item in items:
            if "dimension" in item["data"]:
                if len(item["data"]["dimension"]) == 1:
                    item["data"]["dimension"] = [1, item["data"]["dimension"][0]]
                elif len(item["data"]["dimension"]) != 2:
                    raise Exception(
                        f"Dimension must be a list of length 0 or 2, got {item['data']['dimension']}.")
            elif item["data"]["type"] == "real":
                item["data"]["dimension"] = [1, 1]
        return items

    def remove_non_public(json: Path) -> ConfigJson:
        """
        Helper to drop non-public items unless setup says otherwise.
        """
        if setup["non_public"]:
            return json
        items = list(
            filter(lambda x: x["description"]["public"], json["items"]))
        return {
            "datamappings": json["datamappings"],
            "items": ensure_real_ddim_length(items),
            "view": json["view"] if "view" in json else {"groups": []}
        }

    configs = {}
    for path in setup["json_files"]:
        data = remove_non_public(read_json(path))
        configs[path.name] = data
    return configs
