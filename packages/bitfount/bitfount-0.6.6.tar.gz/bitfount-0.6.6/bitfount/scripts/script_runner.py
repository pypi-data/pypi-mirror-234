"""Main script to run others as subcommands."""
import fire

from bitfount.scripts.generate_schema import gen_schema
from bitfount.scripts.generate_yaml_specs import generate_yaml_specs
from bitfount.scripts.run_modeller import run as modeller_run
from bitfount.scripts.run_pod import run as pod_run
from bitfount.scripts.run_testing import evaluate_model


def main() -> None:
    """Main script entry point."""
    fire.Fire(
        {
            "generate_schema": gen_schema,
            "run_modeller": modeller_run,
            "run_pod": pod_run,
            "run_testing": evaluate_model,
            "generate_yaml_specs": generate_yaml_specs,
        }
    )


if __name__ == "__main__":
    main()
