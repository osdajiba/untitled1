# settings.py

import json


def build_config(config_file, username, password):
    config = {
        "user_config": {
            "username": username,
            "password": password
        },
    }

    with open(config_file, 'w') as config_file:
        json.dump(config, config_file, indent=4)


def main():
    # Generate the default config file
    config_file = "config.example.json"
    username = "your_username"
    password = "your_password"

    # Build config.example.json
    build_config(config_file, username, password)


if __name__ == "__main__":
    main()
