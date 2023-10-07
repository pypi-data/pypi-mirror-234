import base64
import io
import os
from typing import Dict, List, Union

import requests

IPC_API_URI = os.getenv("IPC_API_URI", "")
IPC_API_TOKEN = os.getenv("IPC_API_TOKEN", "")


class InvalidFileDescriptorError(Exception):
    """Raised when the file descriptor structure is invalid."""


class FileDescriptor:
    def __init__(self, file: Union[str, bytes], file_name: str):
        """
        Initialize a FileDescriptor.

        :param file: File content or file ID.
        :param file_name: Name of the file.
        """
        self.file = file
        self.file_name = file_name

    def download(self):
        """Download a file given its ID."""
        self.file = self._download_file(self.file).read()

    def upload(self):
        """Upload file content and update file ID."""
        self.file = self._upload_file_content(self.file, self.file_name)["id"]

    @staticmethod
    def _download_file(file_id: str) -> io.BytesIO:
        """Download a file from IPC API given a file ID."""
        try:
            get_url = f"{IPC_API_URI}/files/{file_id}"
            params = {"token": IPC_API_TOKEN}
            res = requests.get(get_url, params=params)
            res.raise_for_status()
            return io.BytesIO(res.content)
        except requests.RequestException as e:
            raise Exception(f"Error downloading file: {e}")

    @staticmethod
    def _upload_file_content(file_data: Union[str, bytes], file_name: str) -> Dict:
        """Upload file content to IPC API."""
        try:
            post_url = f"{IPC_API_URI}/files"
            params = {"token": IPC_API_TOKEN}
            upload = [("files", (file_name, file_data, "multipart/form-data"))]
            res = requests.post(post_url, files=upload, params=params)
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            raise Exception(f"Error uploading file: {e}")

    @staticmethod
    def process_input_files(data: Union[List[Dict], Dict]) -> Union[List[Dict], Dict]:
        """Recursively process input data containing file descriptors,
        downloading necessary files."""

        if isinstance(data, list):
            return [FileDescriptor.process_input_files(item) for item in data]

        elif isinstance(data, dict):
            if "file" in data and "file_name" in data:
                descriptor = FileDescriptor(
                    data.get("file", ""), data.get("file_name", "")
                )
                descriptor.download()
                return descriptor.to_dict()
            return {
                key: FileDescriptor.process_input_files(value)
                for key, value in data.items()
            }

        else:
            return data

    @staticmethod
    def process_output_files(data: Union[List[Dict], Dict]) -> Union[List[Dict], Dict]:
        """Recursively process output data containing file contents, uploading necessary files."""

        if isinstance(data, list):
            return [FileDescriptor.process_output_files(item) for item in data]

        if isinstance(data, dict):
            if "file" in data and "file_name" in data:
                descriptor = FileDescriptor(
                    data.get("file", b""), data.get("file_name", "")
                )
                descriptor.upload()
                return descriptor.to_dict()
            return {
                key: FileDescriptor.process_output_files(value)
                for key, value in data.items()
            }

        else:
            return data

    def to_dict(self):
        """Convert the file descriptor into a dictionary."""
        return {"file": self.file, "file_name": self.file_name}
