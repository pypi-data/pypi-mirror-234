import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from fiddler.constants import FileType
from fiddler.core_objects import ModelInfo
from fiddler.exceptions import NotSupported
from fiddler.schema.server_info import Version


def match_semver(version: Optional[Version], match_expr: str) -> bool:
    """
    Match the version with match_expr
    :param version: Server version
    :param match_expr: Version to match with. Read more at VersionInfo.match
    :return: True if server version matches, otherwise False
    """
    if not version:
        return False

    if version.prerelease:
        return Version(version.major, version.minor, version.patch).match(match_expr)

    return version.match(match_expr)


def raise_not_supported(
    compatible_client_version: str, client_version: str, server_version: Version
) -> Any:
    """
    Raise error when client version is not compatible with the server version.
    :param compatible_client_version: Max client version supported for the server
    :param client_version: client version
    :param server_version: server version
    :return: NotSupported error
    """
    raise NotSupported(
        f'Please downgrade your fiddler-client to <= {compatible_client_version}. '
        f"The version you are using ({client_version}) isn't compatible with "
        f'your server ({server_version}).'
    )


def get_model_artifact_info(artifact_dir: Path) -> List[Dict[str, Any]]:
    """
    Get model artifact files details
    :param artifact_dir: Model artifact directory
    :return: List of artifact files details
    """
    info: List[Dict[str, Any]] = []

    for f in os.listdir(artifact_dir):
        file_stats = os.stat(os.path.join(artifact_dir, f))
        info.append(
            {'name': f, 'size': file_stats.st_size, 'modified': file_stats.st_mtime}
        )
    return info


def read_model_yaml(artifact_dir: Path) -> Optional[ModelInfo]:
    """
    Read model info from model.yaml file inside artifact dir
    :param artifact_dir: Model artifact dir
    :return: ModelInfo object if model.yaml file is found, otherwise None
    """
    yaml_file = artifact_dir / 'model.yaml'
    if not yaml_file.is_file():
        return None

    with yaml_file.open() as f:
        return ModelInfo.from_dict(yaml.safe_load(f))


def map_extension_to_file_type(file_path: Path) -> Any:
    file_extension = file_path.suffix
    if file_extension == '.csv':
        return FileType.CSV

    if file_extension == '.parquet':
        return FileType.PARQUET
