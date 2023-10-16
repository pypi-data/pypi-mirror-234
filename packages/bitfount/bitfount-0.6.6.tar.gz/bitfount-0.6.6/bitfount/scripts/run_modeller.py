#!/usr/bin/env python
"""Script to run a modeller that sends tasks off to Pods."""
import logging
import os
from os import PathLike
from pathlib import Path
from typing import Union

import fire

from bitfount import config
from bitfount.runners.modeller_runner import (
    DEFAULT_MODEL_OUT,
    run_modeller,
    setup_modeller_from_config_file,
)
from bitfount.runners.utils import setup_loggers

log_level = os.getenv("BITFOUNT_LOG_LEVEL", logging.INFO)

loggers = setup_loggers([logging.getLogger("bitfount")], log_level=log_level)

config._BITFOUNT_CLI_MODE = True


def run(
    path_to_config_yaml: Union[str, PathLike],
    require_all_pods: bool = False,
    model_out: Path = DEFAULT_MODEL_OUT,
) -> None:
    """Runs a modeller from a config file."""
    (
        modeller,
        pod_identifiers,
        project_id,
        run_on_new_datapoints,
        batched_execution,
    ) = setup_modeller_from_config_file(path_to_config_yaml)
    run_modeller(
        modeller,
        pod_identifiers,
        require_all_pods,
        model_out,
        project_id,
        run_on_new_datapoints,
        batched_execution,
    )


def main() -> None:
    """Script entry point."""
    fire.Fire(run)


if __name__ == "__main__":
    main()
