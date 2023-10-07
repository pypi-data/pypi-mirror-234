from .file_handler import *
from .io_handler import *

_input_handler_instance = None


def _get_input_handler_instance():
    global _input_handler_instance
    if _input_handler_instance is None:
        _input_handler_instance = InputHandler()
    return _input_handler_instance


def get_inputs() -> dict:
    """
    Retrieve inputs from the standard input.
    """
    handler = _get_input_handler_instance()
    return handler.inputs


def get_asset() -> dict:
    """
    Retrieve the asset details from the standard input.
    """
    handler = _get_input_handler_instance()
    return handler.asset


def get_arguments() -> dict:
    """
    Retrieve the command-line arguments.
    """
    handler = _get_input_handler_instance()
    return handler.args


def get_asset_schema() -> dict:
    """
    Retrieve the asset schema
    """
    handler = _get_input_handler_instance()
    return handler.asset_schema


def get_action_schema() -> dict:
    """
    Retrieve the action schema
    """
    handler = _get_input_handler_instance()
    return handler.action_schema


def get_proxy() -> str:
    """
    Retrieve the proxy
    """
    handler = _get_input_handler_instance()
    return handler.http_proxy


def process_inputs(raw_inputs: dict) -> dict:
    """
    Process raw inputs to handle any file descriptors and downloads.
    """
    return FileDescriptor.process_input_files(raw_inputs)


def process_outputs(raw_outputs: dict) -> dict:
    """
    Process raw outputs to handle any file descriptors and uploads.
    """
    return FileDescriptor.process_output_files(raw_outputs)


def set_output(data: dict):
    """
    Set the given data as the output.
    """
    OutputHandler.set_output(data)


def set_error(error_data: dict):
    """
    Set the given error data as the error output.
    """
    OutputHandler.set_error(error_data)
