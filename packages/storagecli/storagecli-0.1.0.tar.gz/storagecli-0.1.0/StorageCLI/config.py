from platformdirs import user_config_path
from pathlib import Path
import json
import click

APP_NAME = "StorageCLI"
AUTHOR_NAME = "Merklebot"
config_file = Path(f'{user_config_path(APP_NAME, AUTHOR_NAME)}/config.json')


def write_config(organization_name, bucket_token):
    try:
        config_file.parent.mkdir(exist_ok=True, parents=True)
        config_file.write_text(json.dumps({
            "organization_name": organization_name,
            "bucket_token": bucket_token
        }))
    except Exception as e:
        raise click.ClickException(repr(e))


def read_organization_name():
    try:
        config = json.loads(config_file.read_text())
        return config.get("organization_name")
    except Exception as e:
        raise click.ClickException(repr(e))


def read_token():
    try:
        config = json.loads(config_file.read_text())
        return config.get("bucket_token")
    except Exception as e:
        raise click.ClickException(repr(e))


def clear_config():
    try:
        config_file.parent.mkdir(exist_ok=True, parents=True)
        config_file.write_text("{}")
    except Exception as e:
        raise click.ClickException(repr(e))