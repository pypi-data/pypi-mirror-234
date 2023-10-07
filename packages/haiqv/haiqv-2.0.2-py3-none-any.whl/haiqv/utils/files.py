import os
import pathlib
import posixpath

from mimetypes import guess_type
from urllib.parse import unquote
from urllib.request import pathname2url


def relative_path_to_artifact_path(path):
    if os.path == posixpath:
        return path
    if os.path.abspath(path) == path:
        raise Exception("This method only works with relative paths.")
    return unquote(pathname2url(path))


def path_not_unique(name):
    norm = posixpath.normpath(name)
    return norm != name or norm == "." or norm.startswith("..") or norm.startswith("/")


def get_text_extensions():
    return [
        "txt",
        "log",
        "err",
        "cfg",
        "conf",
        "cnf",
        "cf",
        "ini",
        "properties",
        "prop",
        "hocon",
        "toml",
        "yaml",
        "yml",
        "xml",
        "json",
        "js",
        "py",
        "py3",
        "csv",
        "tsv",
        "md",
        "rst",
        "MLmodel",
        "mlproject",
    ]


def guess_mime_type(file_path):
    filename = pathlib.Path(file_path).name
    extension = os.path.splitext(filename)[-1].replace(".", "")
    # for MLmodel/mlproject with no extensions
    if extension == "":
        extension = filename
    if extension in get_text_extensions():
        return "text/plain"
    mime_type, _ = guess_type(filename)
    if not mime_type:
        # As a fallback, if mime type is not detected, treat it as a binary file
        return "application/octet-stream"
    return mime_type
