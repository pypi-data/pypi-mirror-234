import importlib.metadata
from pathlib import Path

import toml


def to_version(version: str, pyproject_path: str) -> None:
    """
    Defines the version of the project in the pyproject.toml file.

    Args:
        version (str): The new version string to update.
        pyproject_path (str): The path to the pyproject.toml file.

    Returns:
        None
    """
    pyproject_toml_path = Path(pyproject_path)
    pyproject_toml = toml.load(pyproject_toml_path)
    pyproject_toml["tool"]["poetry"]["version"] = version

    with open(pyproject_toml_path, "w") as f:
        toml.dump(pyproject_toml, f)


def summary(package_name):
    """
    Finds the summary for a package.
    """
    package = importlib.metadata.metadata(package_name)
    description = package["Summary"]
    return description
