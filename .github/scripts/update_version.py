#!/usr/bin/env python
"""
Script to update the version in pyproject.toml from a given version tag.
This should be replaced by some sort of cli tool
"""

import sys

import toml


def update_version(version):
    """Update version in pyproject.toml file."""
    # Read the current pyproject.toml
    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)

    print(f"Updating version to {version}")

    # Update the version in the pyproject.toml
    pyproject["project"]["version"] = version

    # Write the updated pyproject.toml
    with open("pyproject.toml", "w") as f:
        toml.dump(pyproject, f)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/update_version.py VERSION")
        sys.exit(1)

    update_version(sys.argv[1])
