# start.py

import json
from core.core import auto_trade


def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def main():
    # Load default config
    config = load_config('../conf/config.json')
    default = config['user_config']

    # More code...
    AT = auto_trade()
    pass


if __name__ == "__main__":
    main()
