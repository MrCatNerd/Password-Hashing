import json

from os.path import join as join_path


def load_settings() -> dict:
    data: dict = dict()

    with open(join_path("data", "settings.json"), "r") as f:
        data = json.load(f)

    return data


data: dict = load_settings()

SALT_LEN = data["salt len"]

del data
