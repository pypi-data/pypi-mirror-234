# Swimlane Core

The swimlane-core is a Python package that provides an easy-to-use interface for users to communicate with Turbine. With this package, users can effortlessly interact with Turbine without dealing with the complexities of handling arguments, inputs, outputs and files.


## Features

* Fetch inputs from the standard input.
* Handle file descriptors and downloads.
* Set outputs and errors in a standardized format.
* Retrieve asset details, command-line arguments, asset schema, action schema, and proxy.

## Usage

### Simple examples

```python
from swimlane_core import (get_action_schema, get_arguments, get_asset,
                           get_asset_schema, get_inputs, get_proxy,
                           process_inputs, process_outputs, set_error,
                           set_output)


args = get_arguments()
inputs = get_inputs()
inputs = process_inputs(inputs)
asset = get_asset()
asset_schema = get_asset_schema()
action_schema = get_action_schema()
http_proxy = get_proxy()
resp = process_outputs(resp)
set_output(resp)
set_error(e)
```

```python
from swimlane_core import process_inputs


raw_inputs = {
    "file": "an id",
    "file_name": "sample.txt"
}

processed_inputs = process_inputs(raw_inputs)
print(processed_inputs)

raw_inputs = {
    "file": "a base64",
    "file_name": "sample.txt"
}

```

```python
from swimlane_core import process_outputs


raw_outputs = {
    "file": b"file content",
    "file_name": "sample.txt"
}

processed_outputs = process_outputs(raw_outputs)
print(processed_outputs)

raw_inputs = {
    "file": "a file id",
    "file_name": "sample.txt"
}

```

### Advanced

The package provides a simple facade, you can access the underling classes for complex workflows or modifying the behavior of the package.


```python
from swimlane_core import FileDescriptor, InputHandler, OutputHandler
```