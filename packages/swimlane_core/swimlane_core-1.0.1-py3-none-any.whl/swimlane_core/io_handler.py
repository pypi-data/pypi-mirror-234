import argparse
import glob
import json
import os
import sys

import yaml


class IOHandlerError(Exception):
    """Base exception class for the IOHandler module."""


class InputHandler:
    def __init__(self):
        try:
            self.args = self._parse_cli_args()
            self.raw_inputs = self._load_raw_inputs()
            self.asset, self.inputs = self._load_asset_and_inputs()
            self.asset_schema, self.action_schema = self._load_schemas(
                self.asset, self.args.action
            )
            self.http_proxy = os.getenv("http_proxy") or self.asset.get(
                "http_proxy", None
            )

        except Exception as e:
            raise IOHandlerError(f"Error initializing InputHandler: {str(e)}")

    @staticmethod
    def _parse_cli_args():
        parser = argparse.ArgumentParser(
            description="Parse command-line arguments for IOHandler."
        )
        parser.add_argument("action", help="The connector action to run", default={})
        return parser.parse_args()

    @staticmethod
    def _load_raw_inputs():
        raw_inputs = sys.stdin.read() or "{}"
        try:
            return json.loads(raw_inputs)
        except json.JSONDecodeError:
            raise IOHandlerError("Invalid JSON input format received.")

    def _load_asset_and_inputs(self):
        asset_keys = os.getenv("ASSET_KEYS")
        if asset_keys is None:
            raise IOHandlerError("ASSET_KEYS environment variable not set.")
        asset = {
            k: self.raw_inputs[k] for k in asset_keys.split(",") if k in self.raw_inputs
        }
        inputs = {k: self.raw_inputs[k] for k in self.raw_inputs if k not in asset}
        return asset, inputs

    @staticmethod
    def get_asset_name(asset):
        asset_type_mappings = [
            ({"username", "password"}, "http_basic"),
            ({"token"}, "http_bearer"),
            ({"oauth2_username", "oauth2_password"}, "oauth2_password"),
            ({"client_secret", "client_id"}, "oauth2_client_credentials"),
        ]
        for keys, name in asset_type_mappings:
            if keys <= set(asset):
                return name
        return "apikey"  # Default to apikey

    def _load_schemas(self, asset, action_name):
        asset_name = self.get_asset_name(asset)
        manifests = glob.glob("./**/*.yaml", recursive=True)
        asset_manifest, action_manifest = {}, {}

        for manifest in manifests:
            with open(manifest, "r") as file:
                try:
                    schema = yaml.safe_load(file)
                    if schema["schema"] == "asset/1" and schema["name"] == asset_name:
                        asset_manifest = schema
                    elif (
                        schema["schema"] == "action/1" and schema["name"] == action_name
                    ):
                        action_manifest = schema
                except Exception:
                    pass
        return asset_manifest, action_manifest


class OutputHandler:
    @staticmethod
    def set_output(data):
        try:
            print("::set-output", json.dumps(data, indent=None), "", sep="")
        except Exception as e:
            raise IOHandlerError(f"Error setting output: {str(e)}")

    @staticmethod
    def set_error(error_data):
        error_json_string = json.dumps(error_data, indent=None)
        print(f"::set-error {error_json_string}", file=sys.stderr)
