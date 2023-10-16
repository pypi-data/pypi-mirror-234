r"""This script takes a config of task templates and uploads them to bitfount hub.

The config also contains paths to any custom models and weights that are used in the
task templates. If the models or weights have changed since the last upload, the models
and weights are uploaded to bitfount hub and the task templates are updated to use the
new versions of the models and weights. Finally, there is also the option to archive
task templates that are no longer used.
```

Example dev usage:

```bash
BITFOUNT_ENVIRONMENT=staging python -m dev-scripts.upload_task_templates  \\
task_templates/config.yaml -u <username>
```

Example production usage:

```bash
python -m bitfount.runners.upload_task_templates task_templates/config.yaml -u \\
<username> -p <password> --client_id=<client_id> --client_secret=<client_secret>
```
"""
from datetime import datetime, timedelta, timezone
import logging
import os
from pathlib import Path
import re
from typing import Any, Dict, Literal, Optional, Tuple, Union, cast

from fire import Fire
from pydantic import BaseModel, ValidationError
from requests import HTTPError, post
import yaml

from bitfount import BitfountModelReference, setup_loggers
from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    _get_environment,
)
from bitfount.hub.authentication_flow import _get_auth_environment
from bitfount.hub.helper import _create_bitfounthub
from bitfount.hub.types import _DEV_HUB_URL, _STAGING_HUB_URL, PRODUCTION_HUB_URL
from bitfount.hub.utils import hash_file_contents
from bitfount.runners.config_schemas import JWT, APIKeys
from bitfount.types import BaseDistributedModelProtocol, _StrAnyDict

BF_USER = "bitfount"
setup_loggers([logging.getLogger("bitfount")])


class ModelConfig(BaseModel):
    """Model config model for static and runtime type checking."""

    model_file: str
    private: bool = True
    weights_file: Optional[str] = None


class BasicTaskTemplateConfig(BaseModel):
    """Base task template config model for static and runtime type checking."""

    slug: str


class TaskTemplateConfig(BasicTaskTemplateConfig):
    """Model config model for static and runtime type checking."""

    title: str
    type: Union[
        Literal["image-segmentation"],
        Literal["image-classification"],
        Literal["object-detection"],
        Literal["text-classification"],
        Literal["text-generation"],
        Literal["tabular-classification"],
        Literal["tabular-regression"],
    ]
    description: str
    template: str


def main(
    config_file: os.PathLike,
    username: str = BF_USER,
    password: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> None:
    """Uploads models, weights and task templates to bitfount.

    Iterates over the models in the config file and uploads them to bitfount if
    the code hash or weights are different from the latest version on bitfount.
    Once the models are updated, the task templates are updated to use the latest
    versions of the models and the task templates are themselves uploaded to bitfount.

    Args:
        config_file: The path to the YAML config.
        username: The username for the model owner. Defaults to 'bitfount'.
        password: The password for the model owner if using ExternallyManagedJWTHandler
            for authentication. Defaults to None.
        client_id: The client id for the model owner if using
            ExternallyManagedJWTHandler for authentication. Defaults to None.
        client_secret: The client secret for the model owner if using
            ExternallyManagedJWTHandler for authentication. Defaults to None.
    """
    with open(config_file, "r") as f:
        config_yaml = yaml.safe_load(f)

    model_names_and_versions = {}
    jwt = None
    if password is not None and client_id is not None and client_secret is not None:
        print("Using JWT for authentication")
        access_token, expires_in = _get_user_token(
            username, password, client_id, client_secret
        )
        jwt = JWT(
            jwt=access_token,
            expires=datetime.now(timezone.utc) + timedelta(seconds=expires_in),
            # Refreshing not necessary as this is not a long-running script
            get_token=lambda: None,  # type: ignore[arg-type, return-value]
        )

    if "models" in config_yaml:
        model_names_and_versions = _upload_models(config_yaml, username, jwt=jwt)
    if "task-templates" in config_yaml:
        _update_and_upload_task_templates(
            config_yaml, username, model_names_and_versions, jwt=jwt
        )
    if "deprecated-task-templates" in config_yaml:
        _archive_templates(config_yaml, username, jwt=jwt)


def _archive_templates(
    config_yaml: _StrAnyDict, username: str, jwt: Optional[JWT] = None
) -> None:
    """Archive task templates that are no longer used.

    Args:
        config_yaml: The config yaml.
        username: The username for the model owner.
        jwt: The JWT for the model owner.

    Raises:
        ValueError: If the task template config is invalid.
    """
    hub_url = _get_hub_url()
    task_template_url = f"{hub_url}/api/task-templates/{username}"
    hub = _create_bitfounthub(username=username, url=hub_url, secrets=jwt)
    for template in config_yaml["deprecated-task-templates"]:
        # Validate the task template config. If it is invalid, raise an error
        try:
            validated_template = BasicTaskTemplateConfig(**template)
        except ValidationError as e:
            raise ValueError(f"Invalid task template config: {e}")

        print(f"Archiving task template: {validated_template.slug}")
        archive_template_response = hub.session.patch(
            url=f"{task_template_url}/{validated_template.slug}",
            data={"state": "archived"},
        )

        try:
            archive_template_response.raise_for_status()
        except HTTPError:
            print(vars(archive_template_response))
        else:
            print(f"Task template {validated_template.slug} archived.")


def _upload_models(
    config_yaml: _StrAnyDict, username: str, jwt: Optional[JWT] = None
) -> Dict[str, int]:
    """Uploads the models to bitfount hub if they have been changed.

    Args:
        config_yaml: The config yaml.
        username: The username for the model owner.
        jwt: The JWT for the model owner.

    Returns:
        A dictionary containing the model names and new version numbers.

    Raises:
        ValueError: If the model config is invalid.
    """
    model_names_and_versions: Dict[str, int] = {}

    # Iterate over the models in the config file
    for model_config in config_yaml["models"]:
        # Validate the model config. If it is invalid, raise an error
        try:
            validated_model_config = ModelConfig(**model_config)
        except ValidationError as e:
            raise ValueError(f"Invalid model config: {e}")

        # Check if the model is present on bitfount hub
        model_ref = BitfountModelReference(
            model_ref=Path(validated_model_config.model_file).stem,
            username=username,
            secrets=jwt,
        )
        model_response = model_ref.hub._get_model_response(
            username=username, model_name=cast(str, model_ref.model_ref)
        )

        # If the model is not present on bitfount, upload it
        if model_response is None:
            _upload_model_and_weights(validated_model_config, username, secrets=jwt)
            # TODO: [BIT-3129] ensure that the first version is always 1
            #  (can be 0 at the moment)
            model_names_and_versions[cast(str, model_ref.model_ref)] = 1
        # If the model is present on bitfount, check if the code hash or weights
        # are different from the latest version on bitfount and upload to a new
        # version if they are different
        else:
            model_version = model_response["modelVersion"]
            hub_model_hash = model_response["modelHash"]
            model_hash = hash_file_contents(Path(validated_model_config.model_file))
            hashes_different = hub_model_hash != model_hash
            weights_different = False
            if validated_model_config.weights_file is not None:
                try:
                    hub_model_weights = model_ref.hub.get_weights(
                        username=username,
                        model_name=cast(str, model_ref.model_ref),
                        model_version=model_version,
                    )
                except HTTPError as e:
                    print(
                        f"Could not get weights from S3: {e.strerror}\n"
                        f"Will continue assuming there are no weights defined"
                    )
                    hub_model_weights = None
                model_weights = Path(validated_model_config.weights_file).read_bytes()
                weights_different = hub_model_weights != model_weights
            if hashes_different or weights_different:
                _upload_model_and_weights(validated_model_config, username, secrets=jwt)
                model_names_and_versions[cast(str, model_ref.model_ref)] = (
                    model_version + 1
                )
            else:
                print(
                    f"Model {validated_model_config.model_file} is already up to date."
                )
                model_names_and_versions[cast(str, model_ref.model_ref)] = model_version
    return model_names_and_versions


def _update_and_upload_task_templates(
    config_yaml: _StrAnyDict,
    username: str,
    model_names_and_versions: Dict[str, int],
    jwt: Optional[JWT] = None,
) -> None:
    """Updates the task templates and uploads them to bitfount hub if they have changed.

    Args:
        config_yaml: The config yaml.
        username: The username for the model owner.
        model_names_and_versions: A dictionary containing the model names and new
            version numbers.
        jwt: The JWT for the model owner.

    Raises:
        ValueError: If the task template config is invalid.
    """
    for task_template_config in config_yaml["task-templates"]:
        # Validate the task template config. If it is invalid, raise an error
        try:
            validated_task_template_config = TaskTemplateConfig(**task_template_config)
        except ValidationError as e:
            raise ValueError(f"Invalid task template config: {e}")

        # Update the model version on task templates that reference any models whose
        # version has changed
        with open(validated_task_template_config.template, "r") as f:
            template = yaml.safe_load(f)

        template = _add_username_to_yaml_config(template, username)
        template = _update_yaml_config(template, model_names_and_versions, username)
        slug = _sanitise_task_template_slug(validated_task_template_config.slug)
        task_template = {
            "title": validated_task_template_config.title,
            "slug": validated_task_template_config.slug,
            "type": validated_task_template_config.type,
            "template": template,
            "description": validated_task_template_config.description,
        }
        hub_url = _get_hub_url()
        task_template_url = f"{hub_url}/api/task-templates"

        # Check if a task template already exists for this user & slug.
        hub = _create_bitfounthub(username=username, url=hub_url, secrets=jwt)
        template_exists_response = hub.session.get(
            url=f"{task_template_url}/{username}/{slug}",
        )

        if template_exists_response.status_code == 200:
            task_template_on_hub = template_exists_response.json()
            if (template == task_template_on_hub["template"]) and (
                validated_task_template_config.description
                == task_template_on_hub["description"]
            ):
                # If the task template or the description have not changed
                # then we will skip updating this template
                print(f'Task "{slug}" is unchanged, not updating it.')
                return

            print(f"Updating task template: {slug}")
            # If the template already exists, push a new version to the hub
            task_template_url = f"{task_template_url}/{username}/{slug}"
        else:
            print(f"Creating task template: {slug}")

        # Create a new task template or task template version
        template_upload_response = hub.session.post(
            url=task_template_url,
            json=task_template,
        )

        try:
            template_upload_response.raise_for_status()
        except HTTPError:
            print(vars(template_upload_response))


def _sanitise_task_template_slug(slug: str) -> str:
    """Ensure provided slug is valid and sanitised.

    Args:
        slug: The slug to sanitise.

    Returns:
        The sanitised slug.
    """
    # Slug name sanitisation
    # Needs to be only alphanumeric characters
    alpha_safe_slug = re.sub(r"[^0-9a-z]", "-", slug.strip().lower())
    # No consecutive hyphens
    double_hyphen_safe_slug = re.sub(r"(-)+", "-", alpha_safe_slug)
    # No hyphens at the start or end
    external_hyphen_safe_slug = re.sub(r"^-|-$", "", double_hyphen_safe_slug)
    # Less than 50 characters
    slug = external_hyphen_safe_slug[:50]
    return slug


def _update_yaml_config(
    config_yaml: _StrAnyDict, model_names_and_versions: Dict[str, int], username: str
) -> _StrAnyDict:
    """Update the model version in the yaml config.

    Args:
        config_yaml: The yaml config.
        model_names_and_versions: A dictionary containing the model names and new
            version numbers.

    Returns:
        The updated yaml config.

    Raises:
        ValueError: If the model is not found in the config.
    """
    for index, algo_config in enumerate(config_yaml["task"]["algorithm"]):
        if "model" in algo_config and "bitfount_model" in algo_config["model"]:
            updated_model_version = False
            # If the model is a bitfount model, iterate over new model versions
            # to find a match and update the version number
            for model_slug, model_version in model_names_and_versions.items():
                if algo_config["model"]["bitfount_model"]["model_ref"] == model_slug:
                    config_yaml["task"]["algorithm"][index]["model"]["bitfount_model"][
                        "model_version"
                    ] = model_version
                    config_yaml["task"]["algorithm"][index]["model"]["bitfount_model"][
                        "username"
                    ] = username
                    updated_model_version = True
                    break
            if not updated_model_version:
                raise ValueError(
                    f"Model {algo_config['model']['bitfount_model']['model_ref']} "
                    "was not referenced in the model config."
                )

    return config_yaml


def _get_hub_url() -> str:
    """Retrieve the hub URL appropriate for the current environment."""
    environment = _get_environment()
    if environment == _STAGING_ENVIRONMENT:
        return _STAGING_HUB_URL
    elif environment == _DEVELOPMENT_ENVIRONMENT:
        return _DEV_HUB_URL
    else:
        return PRODUCTION_HUB_URL


def _get_user_token(
    username: str,
    password: str,
    client_id: str,
    client_secret: str,
) -> Tuple[str, int]:
    """Gets a user token from auth0 to use for authentication.

    Args:
        username: The username to authenticate with.
        password: The password to authenticate with.
        client_id: The client id for auth0 tenant.
        client_secret: The client secret for the auth0 tenant.

    Returns:
        A tuple containing the access token and length in seconds until the token
        expires.
    """
    auth_environment = _get_auth_environment()
    realm = (
        "Username-Password-Authentication"
        if auth_environment.name == "development"
        else "bitfount-db"
    )

    token_response = post(
        f"https://{auth_environment.auth_domain}/oauth/token",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": username,
            "password": password,
            "audience": "https://hub.bitfount.com/api",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "profile",
            "realm": realm,
        },
        timeout=10,
    )
    token_response_json = token_response.json()
    return token_response_json["access_token"], token_response_json["expires_in"]


def _add_username_to_yaml_config(
    config_yaml: _StrAnyDict, username: str
) -> Dict[str, Any]:
    """Adds the username to the config.

    If the username is not present in the custom model config, the specified username
    is added to the config instead.

    Args:
        config_yaml: The yaml config.
        username: The username for the model owner.

    Returns:
        The updated yaml config.
    """
    if not isinstance(config_yaml["task"]["algorithm"], list):
        config_yaml["task"]["algorithm"] = [config_yaml["task"]["algorithm"]]
    for algo in config_yaml["task"]["algorithm"]:
        if (
            "model" in algo
            and "bitfount_model" in algo["model"]
            and "username" not in algo["model"]["bitfount_model"]
        ):
            algo["model"]["bitfount_model"]["username"] = username
    return config_yaml


def _upload_model_and_weights(
    model_config: ModelConfig,
    username: str,
    secrets: Optional[Union[APIKeys, JWT]] = None,
) -> None:
    """Uploads the model and weights to bitfount hub.

    Before uploading the model, it is checked that the model implements
    BaseDistributedModelProtocol.

    Args:
        model_config: The model config to upload.
        username: The username for the model owner.
        secrets: The secrets for the model owner.

    Raises:
        TypeError: If the model does not implement BaseDistributedModelProtocol.
        ValueError: If model upload fails.
    """
    model_ref = BitfountModelReference(
        model_ref=Path(model_config.model_file),
        private=model_config.private,
        username=username,
        secrets=secrets,
    )
    model_cls = model_ref._get_model_from_path()
    try:
        assert issubclass(model_cls, BaseDistributedModelProtocol)  # nosec[assert_used]
    except AssertionError:
        raise TypeError(
            f"Model {model_config.model_file} must implement "
            "BaseDistributedModelProtocol."
        )
    upload_response = model_ref._upload_model_to_hub()  # uploads the model
    if upload_response is None:
        raise ValueError("Model upload failed.")
    model_version = upload_response["version"]
    model_ref.model_version = model_version
    if model_config.weights_file is not None:
        model_ref.send_weights(Path(model_config.weights_file))  # uploads the weights


if __name__ == "__main__":
    Fire(main)
