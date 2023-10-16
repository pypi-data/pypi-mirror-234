"""Useful objects/functions for the hub.

This is primarily intended for use by modules outside the `hub` package.
It cannot be imported by most modules in the `hub` package because it would
introduce circular imports.
"""
import hashlib
from pathlib import Path


def hash_file_contents(file_path: Path) -> str:
    """Hash file contents using sha256."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            # This is necessary to ensure cross-platform compatibility between windows
            # and unix platforms which use "\r\n" and "\n" for line endings
            # respectively.
            byte_block = byte_block.replace(b"\r", b"")
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()
