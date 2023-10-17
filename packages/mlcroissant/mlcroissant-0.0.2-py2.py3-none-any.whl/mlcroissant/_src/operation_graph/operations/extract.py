"""Extract operation module."""

import dataclasses
import logging
import os
import tarfile
import zipfile

from etils import epath
import pandas as pd

from mlcroissant._src.core.constants import EXTRACT_PATH
from mlcroissant._src.core.path import get_fullpath
from mlcroissant._src.core.path import Path
from mlcroissant._src.operation_graph.base_operation import Operation
from mlcroissant._src.operation_graph.operations.download import get_hash
from mlcroissant._src.structure_graph.nodes.file_object import FileObject
from mlcroissant._src.structure_graph.nodes.file_set import FileSet


def should_extract(encoding_format: str) -> bool:
    """Whether the encoding format should be extracted (zip or tar)."""
    return (
        encoding_format == "application/x-tar" or encoding_format == "application/zip"
    )


def _extract_file(source: epath.Path, target: epath.Path) -> None:
    """Extracts the `source` file to `target`."""
    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as zip:
            zip.extractall(target)
    elif tarfile.is_tarfile(source):
        with tarfile.open(source) as tar:
            tar.extractall(target)
    else:
        raise ValueError(f"Unsupported compression method for file: {source}")


@dataclasses.dataclass(frozen=True, repr=False)
class Extract(Operation):
    """Extracts tar/zip and yields filtered pd.DataFrame."""

    node: FileObject
    target_node: FileSet

    def __call__(self, archive_file: Path) -> pd.DataFrame:
        """See class' docstring."""
        url = self.node.content_url
        hashed_url = get_hash(url)
        extract_dir = EXTRACT_PATH / hashed_url
        if not extract_dir.exists():
            _extract_file(archive_file.filepath, extract_dir)
        logging.info(
            "Found directory where data is extracted: %s", os.fspath(extract_dir)
        )
        return Path(
            filepath=extract_dir,
            fullpath=get_fullpath(extract_dir, EXTRACT_PATH),
        )
