from datetime import timedelta
import io
import json
import os
import sys
import time
from urllib.parse import urlencode
import warnings

import jwt
import requests

from craft_ai_sdk.constants import DEPLOYMENT_EXECUTION_RULES

from .io import (
    INPUT_OUTPUT_TYPES,
    Input,
    Output,
    InputSource,
    OutputDestination,
    _format_execution_output,
    _format_execution_input,
)
from craft_ai_sdk.exceptions import SdkException

from .utils import (
    STEP_PARAMETER,
    _datetime_to_timestamp_in_ms,
    chunk_buffer,
    handle_data_store_response,
    handle_http_request,
    handle_http_response,
    log_action,
    log_func_result,
    map_container_config_step_parameter,
    move_branch_outside_of_container_config,
    remove_none_values,
    use_authentication,
)

from .experimental_warnings import (
    UPDATE_STEP_WARNING_MESSAGE,
    experimental,
)

warnings.simplefilter("always", DeprecationWarning)


class CraftAiSdk:
    """Main class to instantiate

    Attributes:
        base_environment_url (:obj:`str`): Base URL to CraftAI Environment.
        base_environment_api_url (:obj:`str`): Base URL to CraftAI Environment API.
        base_control_url (:obj:`str`): Base URL to CraftAI authorization server.
        base_control_api_url (:obj:`str`): Base URL to CraftAI authorization server API.
        verbose_log (bool): If True, information during method execution will be
            printed.
        warn_on_metric_outside_of_step (bool): If True, a warning will be printed when
            a metric is added outside of a step.
    """

    # Size (in bytes) from which datastore upload will switch to multipart
    # Minimum part size is 5MiB
    # (https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html)
    # 100MiB is the recommended size to switch to multipart
    # (https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
    _MULTIPART_THRESHOLD = int(
        os.environ.get("CRAFT_AI__MULTIPART_THRESHOLD__B", "100_000_000")
    )
    _MULTIPART_PART_SIZE = int(
        os.environ.get("CRAFT_AI__MULTIPART_PART_SIZE__B", "10_000_000")
    )
    _access_token_margin = timedelta(seconds=30)
    _version = "0.27.1"  # Would be better to share it somewhere
    _get_time = time.time  # For tests fake timing

    def __init__(
        self,
        sdk_token=None,
        environment_url=None,
        control_url=None,
        verbose_log=None,
        warn_on_metric_outside_of_step=True,
    ):
        """Inits CraftAiSdk.

        Args:
            sdk_token (:obj:`str`, optional): SDK token. You can retrieve it
                from the website.
                Defaults to ``CRAFT_AI_SDK_TOKEN`` environment variable.
            environment_url (:obj:`str`, optional): URL to CraftAI environment.
                Defaults to ``CRAFT_AI_ENVIRONMENT_URL`` environment variable.
            control_url (:obj:`str`, optional): URL to CraftAI authorization server.
                You probably don't need to set it.
                Defaults to ``CRAFT_AI_CONTROL_URL`` environment variable, or
                https://mlops-platform.craft.ai.
            verbose_log (:obj:`bool`, optional): If ``True``, information during method
                execution will be printed.
                Defaults to ``True`` if the environment variable ``SDK_VERBOSE_LOG`` is
                set to ``true``; ``False`` if it is set to ``false``; else, defaults to
                ``True`` in interactive mode; ``False`` otherwise.
            warn_on_metric_outside_of_step (:obj:`bool`, optional): If ``True``, a
                warning will be raised when a metric is added outside of a step.
                Defaults to ``True``.

        Raises:
            ValueError: if the ``sdk_token`` or ``environment_url`` is not defined and
            the corresponding environment variable is not set.
        """
        self._session = requests.Session()
        self._session.headers["craft-ai-client"] = f"craft-ai-sdk@{self._version}"

        # Set authorization token
        if sdk_token is None:
            sdk_token = os.environ.get("CRAFT_AI_SDK_TOKEN")
        if not sdk_token:
            raise ValueError(
                'Parameter "sdk_token" should be set, since '
                '"CRAFT_AI_SDK_TOKEN" environment variable is not defined.'
            )
        self._refresh_token = sdk_token
        self._access_token = None
        self._access_token_data = None

        # Set base environment url
        if environment_url is None:
            environment_url = os.environ.get("CRAFT_AI_ENVIRONMENT_URL")
        if not environment_url:
            raise ValueError(
                'Parameter "environment_url" should be set, since '
                '"CRAFT_AI_ENVIRONMENT_URL" environment variable is not defined.'
            )
        environment_url = environment_url.rstrip("/")
        self.base_environment_url = environment_url
        self.base_environment_api_url = f"{environment_url}/api/v1"

        # Set base control url
        if control_url is None:
            control_url = os.environ.get("CRAFT_AI_CONTROL_URL")
        if not control_url:
            control_url = "https://mlops-platform.craft.ai"
        control_url = control_url.rstrip("/")
        self.base_control_url = control_url
        self.base_control_api_url = f"{control_url}/api/v1"

        if verbose_log is None:
            env_verbose_log = os.environ.get("SDK_VERBOSE_LOG", "").lower()
            # Detect interactive mode: https://stackoverflow.com/a/64523765
            verbose_log = (
                True
                if env_verbose_log == "true"
                else False
                if env_verbose_log == "false"
                else hasattr(sys, "ps1")
            )
        self.verbose_log = verbose_log

        # Set warn_on_metric_outside_of_step
        self.warn_on_metric_outside_of_step = warn_on_metric_outside_of_step

    # _____ REQUESTS METHODS _____

    @handle_http_request
    @use_authentication
    def _get(self, url, params=None, **kwargs):
        return self._session.get(
            url,
            params=params,
            **kwargs,
        )

    @handle_http_request
    @use_authentication
    def _post(self, url, data=None, params=None, files=None, **kwargs):
        return self._session.post(
            url,
            data=data,
            params=params,
            files=files,
            **kwargs,
        )

    @handle_http_request
    @use_authentication
    def _put(self, url, data=None, params=None, files=None, **kwargs):
        return self._session.put(
            url,
            data=data,
            params=params,
            files=files,
            **kwargs,
        )

    @handle_http_request
    @use_authentication
    def _delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    # _____ AUTHENTICATION & PROFILE _____

    @handle_http_request
    def _query_refresh_access_token(self):
        url = f"{self.base_control_api_url}/auth/refresh"
        data = {"refresh_token": self._refresh_token}
        return self._session.post(url, json=data)

    def _refresh_access_token(self):
        response = self._query_refresh_access_token()
        self._access_token = response["access_token"]
        self._access_token_data = jwt.decode(
            self._access_token, options={"verify_signature": False}
        )

    def _clear_access_token(self):
        self._access_token = None
        self._access_token_data = None

    def who_am_i(self):
        """Get the information of the current user

        Returns:
            :obj:`dict` containing user infos"""
        url = f"{self.base_control_api_url}/users/me"
        return self._get(url)

    @property
    def warn_on_metric_outside_of_step(self):
        """Whether a warning should be raised when a metric is added outside of a
        step."""
        return self._warn_on_metric_outside_of_step

    @warn_on_metric_outside_of_step.setter
    def warn_on_metric_outside_of_step(self, value):
        if not isinstance(value, bool):
            raise TypeError("warn_on_metric_outside_of_step must be a boolean")
        self._warn_on_metric_outside_of_step = value

    # _____ STEPS _____

    def _log_step_with_io(self, step):
        parameters = step.get("parameters", {})
        if not {"step_name", "inputs", "outputs"} <= parameters.keys():
            return

        inputs, outputs = parameters["inputs"], parameters["outputs"]
        msg = f'Step "{parameters["step_name"]}" created'
        if inputs:
            msg += "\n  Inputs: "
            for inp in inputs:
                required_str = ", required" if inp.get("is_required", False) else ""
                msg += f'\n    - {inp["name"]} ({inp["data_type"]}{required_str})'

        if outputs:
            msg += "\n  Outputs: "
            for output in outputs:
                msg += f'\n    - {output["name"]} ({output["data_type"]})'

        log_action(self, msg)

    @log_func_result("Steps creation")
    def create_step(
        self,
        step_name,
        function_path=None,
        function_name=None,
        repository_branch=STEP_PARAMETER.FALLBACK_PROJECT,
        description=None,
        container_config=None,
        inputs=None,
        outputs=None,
        timeout_s=3 * 60,
    ):
        """Create pipeline step from a function located on a remote repository.

        Use :obj:`STEP_PARAMETER` to explicitly set a value to null or fall back on
        project information.

        Args:
            step_name (:obj:`str`): Step name.
            function_path (:obj:`str`, optional): Path to the file that contains the
                function. This parameter is required if parameter "dockerfile_path"
                is not specified.
            function_name (:obj:`str`, optional): Name of the function in that file.
                This parameter is required if parameter "dockerfile_path" is not
                specified.
            repository_branch (:obj:`str`, optional): Branch name. Defaults to falling
                back on project information.
            description (:obj:`str`, optional): Description. Defaults to None.
            container_config (:obj:`dict[str, str]`, optional): Some step configuration,
                with the following optional keys:

                * ``"language"`` (:obj:`str`): Language and version used for the step.
                  Defaults to falling back on project information.
                * ``"repository_url"`` (:obj:`str`): Remote repository url.
                  Defaults to falling back on project information.
                * ``"repository_deploy_key"`` (:obj:`str`): Private SSH key of the
                  repository.
                  Defaults to falling back on project information, can be set to null.
                * ``"requirements_path"`` (:obj:`str`): Path to the requirements.txt
                  file. Environment variables created through
                  :func:`create_or_update_environment_variable` can be used
                  in requirements.txt, as in ``"${ENV_VAR}"``.
                  Defaults to falling back on project information, can be set to null.
                * ``"included_folders"`` (:obj:`list[str]`): List of folders and files
                  in the repository required for the step execution.
                  Defaults to falling back on project information, can be set to null.
                * ``"system_dependencies"`` (:obj:`list[str]`): List of system
                  dependencies.
                  Defaults to falling back on project information, can be set to null.
                * ``"dockerfile_path"`` (:obj:`str`): Path to the Dockerfile. This
                  parameter should only be used as a last resort and for advanced use.
                  When specified, the following parameters should be set to null:
                  ``"function_path"``, ``"function_name"``, ``"language"``,
                  ``"requirements_path"`` and ``"system_dependencies"``.

            inputs(`list` of instances of :class:`Input`): List of inputs. Each
                parameter of the step function should be specified as an instance of
                :class:`Input` via this parameter `inputs`.
                During the execution of the step, the value of the inputs would be
                passed as function arguments.
            outputs(`list` of instances of :class:`Output`): List of the step
                outputs. For the step to have outputs, the function should return a
                :obj:`dict` with the name of the output as keys and the value of the
                output as values. Each output should be specified as an instance
                of :class:`Output` via this parameter `outputs`.
            timeout_s (:obj:`int`): Maximum time to wait for the step to be created.
                3min by default, and at least 2min.

        Returns:
            :obj:`dict`: Created step represented as a :obj:`dict` with the following
            keys:

            * ``"parameters"`` (:obj:`dict`): Information used to create the step with
              the following keys:

              * ``"step_name"`` (:obj:`str`): Name of the step.
              * ``"function_path"`` (:obj:`str`): Path to the file that contains the
                function.
              * ``"function_name"`` (:obj:`str`): Name of the function in that file.
              * ``"repository_branch"`` (:obj:`str`): Branch name.
              * ``"description"`` (:obj:`str`): Description.
              * ``"inputs"`` (:obj:`list` of :obj:`dict`): List of inputs represented
                as a :obj:`dict` with the following keys:

                * ``"name"`` (:obj:`str`): Input name.
                * ``"data_type"`` (:obj:`str`): Input data type.
                * ``"is_required"`` (:obj:`bool`): Whether the input is required.
                * ``"default_value"`` (:obj:`str`): Input default value.

              * ``"outputs"`` (:obj:`list` of :obj:`dict`): List of outputs
                represented as a :obj:`dict` with the following keys:

                * ``"name"`` (:obj:`str`): Output name.
                * ``"data_type"`` (:obj:`str`): Output data type.
                * ``"description"`` (:obj:`str`): Output description.

              * ``"container_config"`` (:obj:`dict[str, str]`): Some step
                configuration, with the following optional keys:

                * ``"language"`` (:obj:`str`): Language and version used for the
                  step.
                * ``"repository_url"`` (:obj:`str`): Remote repository url.
                * ``"included_folders"`` (:obj:`list[str]`): List of folders and
                  files in the repository required for the step execution.
                * ``"system_dependencies"`` (:obj:`list[str]`): List of system
                  dependencies.
                * ``"dockerfile_path"`` (:obj:`str`): Path to the Dockerfile.
                * ``"requirements_path"`` (:obj:`str`): Path to the requirements.txt
                  file.

            * ``"creation_info"`` (:obj:`dict`): Information about the step creation:

              * ``"created_at"`` (:obj:`str`): The creation date in ISO format.
              * ``"updated_at"`` (:obj:`str`): The last update date in ISO format.
              * ``"commit_id"`` (:obj:`str`): The commit id on which the step was
                built.
              * ``"status"`` (:obj:`str`): The step status, always ``"Ready"`` when
                this function returns.
        """

        container_config = {} if container_config is None else container_config.copy()
        if repository_branch is not None:
            container_config.update({"repository_branch": repository_branch})

        data = remove_none_values(
            {
                "step_name": step_name,
                "function_path": function_path,
                "function_name": function_name,
                "description": description,
                "container_config": map_container_config_step_parameter(
                    container_config
                ),
            }
        )

        if inputs is not None:
            if any([not isinstance(input_, Input) for input_ in inputs]):
                raise ValueError("'inputs' must be a list of instances of Input.")
            data["inputs"] = [inp.to_dict() for inp in inputs]

        if outputs is not None:
            if any([not isinstance(output_, Output) for output_ in outputs]):
                raise ValueError("'outputs' must be a list of instances of Output.")
            data["outputs"] = [output.to_dict() for output in outputs]

        url = f"{self.base_environment_api_url}/steps"

        log_action(
            self,
            "Please wait while step is being created. This may take a while...",
        )

        start_time = self._get_time()
        created_step, response = self._post(url, json=data, get_response=True)

        if response.status_code != 206:  # Step is still building
            returned_step = move_branch_outside_of_container_config(created_step)
            self._log_step_with_io(returned_step)
            return returned_step

        _RETRY_INTERVAL = 10  # seconds
        elapsed_time = self._get_time() - start_time
        step_status = "Pending"
        while step_status != "Ready" and elapsed_time < timeout_s:
            time.sleep(_RETRY_INTERVAL)
            created_step = self.get_step(step_name)
            step_status = created_step.get("creation_info", {}).get("status", None)
            elapsed_time = self._get_time() - start_time
        if step_status != "Ready":
            raise SdkException(
                'The step was not ready in time. It is still being created but \
this function stopped trying. Please check its status with "get_step".',
                name="TimeoutException",
            )
        return created_step

    def get_step(self, step_name):
        """Get a single step if it exists.

        Args:
            step_name (:obj:`str`): The name of the step to get.

        Returns:
            :obj:`dict`: ``None`` if the step does not exist; otherwise
            the step information, with the following keys:

            * ``"parameters"`` (:obj:`dict`): Information used to create the step with
              the following keys:

              * ``"step_name"`` (:obj:`str`): Name of the step.
              * ``"function_path"`` (:obj:`str`): Path to the file that contains the
                function.
              * ``"function_name"`` (:obj:`str`): Name of the function in that file.
              * ``"repository_branch"`` (:obj:`str`): Branch name.
              * ``"description"`` (:obj:`str`): Description.
              * ``"inputs"`` (:obj:`list` of :obj:`dict`): List of inputs represented
                as a :obj:`dict` with the following keys:

                * ``"name"`` (:obj:`str`): Input name.
                * ``"data_type"`` (:obj:`str`): Input data type.
                * ``"is_required"`` (:obj:`bool`): Whether the input is required.
                * ``"default_value"`` (:obj:`str`): Input default value.

              * ``"outputs"`` (:obj:`list` of :obj:`dict`): List of outputs
                represented as a :obj:`dict` with the following keys:

                * ``"name"`` (:obj:`str`): Output name.
                * ``"data_type"`` (:obj:`str`): Output data type.
                * ``"description"`` (:obj:`str`): Output description.

              * ``"container_config"`` (:obj:`dict[str, str]`): Some step
                configuration, with the following optional keys:

                * ``"language"`` (:obj:`str`): Language and version used for the
                  step.
                * ``"repository_url"`` (:obj:`str`): Remote repository url.
                * ``"included_folders"`` (:obj:`list[str]`): List of folders and
                  files in the repository required for the step execution.
                * ``"system_dependencies"`` (:obj:`list[str]`): List of system
                  dependencies.
                * ``"dockerfile_path"`` (:obj:`str`): Path to the Dockerfile.
                * ``"requirements_path"`` (:obj:`str`): Path to the requirements.txt
                  file.

            * ``"creation_info"`` (:obj:`dict`): Information about the step creation:

              * ``"created_at"`` (:obj:`str`): The creation date in ISO format.
              * ``"updated_at"`` (:obj:`str`): The last update date in ISO format.
              * ``"commit_id"`` (:obj:`str`): The commit id on which the step was
                built.
              * ``"status"`` (:obj:`str`): either ``"Pending"`` or ``"Ready"``.
        """
        url = f"{self.base_environment_api_url}/steps/{step_name}"
        try:
            step = self._get(
                url,
            )
        except SdkException as error:
            if error.status_code == 404:
                return None
            raise error
        return move_branch_outside_of_container_config(step)

    def list_steps(self):
        """Get the list of all steps.

        Returns:
            :obj:`list` of :obj:`dict`: List of steps represented as :obj:`dict` with
            the following keys:

            * ``"step_name"`` (:obj:`str`): Name of the step.
            * ``"status"`` (:obj:`str`): either ``"Pending"`` or ``"Ready"``.
            * ``"created_at"`` (:obj:`str`): The creation date in ISO format.
            * ``"updated_at"`` (:obj:`str`): The last update date in ISO format.
            * ``"repository_branch"`` (:obj:`str`): The branch of the
              repository where the step was built.
            * ``"repository_url"`` (:obj:`str`): The url of the repository
              where the step was built.
            * ``"commit_id"`` (:obj:`str`): The commit id on which the step was
              built.
        """
        url = f"{self.base_environment_api_url}/steps"

        return self._get(url)

    @experimental(UPDATE_STEP_WARNING_MESSAGE)
    @log_func_result("Step update")
    def update_step(
        self,
        step_name,
        function_path=None,
        function_name=None,
        repository_branch=STEP_PARAMETER.FALLBACK_PROJECT,
        description=None,
        container_config=None,
    ):
        """Update a pipeline step from a source code located on a remote repository.

        The current step configuration will be **replaced** by the provided options.
        Use :obj:`STEP_PARAMETER` to explicitly set a value to null or fall back on
        project information.

        Args:
            step_name (:obj:`str`): Name of the step to update.
            function_path (:obj:`str`, optional): Path to the file that contains the
                function. This parameter is required if parameter "dockerfile_path"
                is not specified.
            function_name (:obj:`str`, optional): Name of the function in that file.
                This parameter is required if parameter "dockerfile_path" is not
                specified.
            repository_branch (:obj:`str`, optional): Branch name. Defaults to falling
                back on project information.
            description (:obj:`str`, optional): Description. Defaults to None.
            container_config (:obj:`dict[str, str]`, optional): Some step configuration,
                with the following optional keys:

                * ``"language"`` (:obj:`str`): Language and version used for the step.
                  Defaults to falling back on project information.
                * ``"repository_url"`` (:obj:`str`): Remote repository url.
                  Defaults to falling back on project information.
                * ``"repository_deploy_key"`` (:obj:`str`): Private SSH key of the
                  repository.
                  Defaults to falling back on project information, can be set to null.
                * ``"requirements_path"`` (:obj:`str`): Path to the requirements.txt
                  file. Environment variables created through
                  :func:`create_or_update_environment_variable` can be used
                  in requirements.txt, as in ``"${ENV_VAR}"``.
                  Defaults to falling back on project information, can be set to null.
                * ``"included_folders"`` (:obj:`list[str]`): List of folders and files
                  in the repository required for the step execution.
                  Defaults to falling back on project information, can be set to null.
                * ``"system_dependencies"`` (:obj:`list[str]`): List of system
                  dependencies.
                  Defaults to falling back on project information, can be set to null.
                * ``"dockerfile_path"`` (:obj:`str`): Path to the Dockerfile. This
                  parameter should only be used as a last resort and for advanced use.
                  When specified, the following parameters should be set to null:
                  ``"function_path"``, ``"function_name"``, ``"language"``,
                  ``"requirements_path"`` and ``"system_dependencies"``.

        Returns:
            :obj:`dict`: The updated step represented as a :obj:`dict` with
            the following keys:

            * ``"parameters"`` (:obj:`dict`): Information used to create the step with
              the following keys:

              * ``"step_name"`` (:obj:`str`): Name of the step.
              * ``"function_path"`` (:obj:`str`): Path to the file that contains the
                function.
              * ``"function_name"`` (:obj:`str`): Name of the function in that file.
              * ``"repository_branch"`` (:obj:`str`): Branch name.
              * ``"description"`` (:obj:`str`): Description.
              * ``"inputs"`` (:obj:`list` of :obj:`dict`): List of inputs represented
                as a :obj:`dict` with the following keys:

                * ``"name"`` (:obj:`str`): Input name.
                * ``"data_type"`` (:obj:`str`): Input data type.
                * ``"is_required"`` (:obj:`bool`): Whether the input is required.
                * ``"default_value"`` (:obj:`str`): Input default value.

              * ``"outputs"`` (:obj:`list` of :obj:`dict`): List of outputs
                represented as a :obj:`dict` with the following keys:

                * ``"name"`` (:obj:`str`): Output name.
                * ``"data_type"`` (:obj:`str`): Output data type.
                * ``"description"`` (:obj:`str`): Output description.

              * ``"container_config"`` (:obj:`dict[str, str]`): Some step
                configuration, with the following optional keys:

                * ``"language"`` (:obj:`str`): Language and version used for the
                  step.
                * ``"repository_url"`` (:obj:`str`): Remote repository url.
                * ``"included_folders"`` (:obj:`list[str]`): List of folders and
                  files in the repository required for the step execution.
                * ``"system_dependencies"`` (:obj:`list[str]`): List of system
                  dependencies.
                * ``"dockerfile_path"`` (:obj:`str`): Path to the Dockerfile.
                * ``"requirements_path"`` (:obj:`str`): Path to the requirements.txt
                  file.

            * ``"creation_info"`` (:obj:`dict`): Information about the step creation:

              * ``"created_at"`` (:obj:`str`): The creation date in ISO format.
              * ``"updated_at"`` (:obj:`str`): The last update date in ISO format.
              * ``"commit_id"`` (:obj:`str`): The commit id on which the step was
                built.
              * ``"status"`` (:obj:`str`): either ``"Pending"`` or ``"Ready"``.

        """

        url = f"{self.base_environment_api_url}/steps/{step_name}"

        container_config = {} if container_config is None else container_config.copy()
        if repository_branch is not None:
            container_config.update({"repository_branch": repository_branch})
        data = remove_none_values(
            {
                "function_path": function_path,
                "function_name": function_name,
                "description": description,
                "container_config": map_container_config_step_parameter(
                    container_config
                ),
            }
        )

        log_action(
            self,
            "Please wait while step is being updated. This may take a while...",
        )
        return move_branch_outside_of_container_config(self._put(url, json=data))

    @log_func_result("Step deletion")
    def delete_step(self, step_name, force_dependents_deletion=False):
        """Delete one step.

        Args:
            step_name (:obj:`str`): Name of the step to delete
                as defined in the ``config.yaml`` configuration file.
            force_dependents_deletion (:obj:`bool`, optional): if True the associated
                step's dependencies will be deleted too (pipeline, pipeline executions,
                deployments). Defaults to False.

        Returns:
            :obj:`dict[str, str]`: The deleted step represented as a :obj:`dict` with
            the following keys:

            * ``"step_name"`` (:obj:`str`): Name of the step.
        """
        url = f"{self.base_environment_api_url}/steps/{step_name}"
        params = {
            "force_dependents_deletion": force_dependents_deletion,
        }
        return self._delete(url, params=params)

    # _____ PIPELINES _____

    @log_func_result("Pipeline creation")
    def create_pipeline(self, pipeline_name, step_name):
        """Create a pipeline containing a single step.

        Args:
            pipeline_name (:obj:`str`): Name of the pipeline to be created.
            step_name (:obj:`str`): Name of the step to be included in the pipeline.
                Note that the step should have the status ``"Ready"`` to create the
                pipeline.

        Returns:
            :obj:`dict`: Created pipeline represented as :obj:`dict` with the following
            keys:

            * ``"pipeline_name"`` (:obj:`str`): Name of the pipeline.
            * ``"created_at"`` (:obj:`str`): Pipeline date of creation.
            * ``"steps"`` (:obj:`list[str]`): List of step names included in the
              pipeline.
            * ``"open_inputs"`` (:obj:`list` of :obj:`dict`): List of open inputs
              of the pipeline. Each open input is represented as a :obj:`dict` with the
              following keys:

              * ``"input_name"`` (:obj:`str`): Name of the open input.
              * ``"step_name"`` (:obj:`str`): Name of the step that provides the open
                input.
              * ``"data_type"`` (:obj:`str`): Data type of the open input.
              * ``"description"`` (:obj:`str`): Description of the open input.
              * ``"default_value"`` (:obj:`str`): Default value of the open input.
              * ``"is_required"`` (:obj:`bool`): Whether the open input is required or
                not.

            * ``"open_outputs"`` (:obj:`list` of :obj:`dict`): List of open outputs
              of the pipeline. Each open output is represented as a :obj:`dict` with the
              following keys:

              * ``"output_name"`` (:obj:`str`): Name of the open output.
              * ``"step_name"`` (:obj:`str`): Name of the step that provides the open
                output.
              * ``"data_type"`` (:obj:`str`): Data type of the open output.
              * ``"description"`` (:obj:`str`): Description of the open output.
        """
        url = f"{self.base_environment_api_url}/pipelines"
        body = {
            "pipeline_name": pipeline_name,
            "step_names": [step_name],
        }

        resp = self._post(url, json=body)
        return resp

    def _get_pipeline(self, pipeline_name):
        url = f"{self.base_environment_api_url}/pipelines/{pipeline_name}"
        return self._get(url)

    def get_pipeline(self, pipeline_name):
        """Get a single pipeline if it exists.

        Args:
            pipeline_name (:obj:`str`): Name of the pipeline to get.

        Returns:
            None if the pipeline does not exist, otherwise pipeline information, with
            the following keys:

            * ``"pipeline_name"`` (:obj:`str`): Name of the pipeline.
            * ``"created_at"`` (:obj:`str`): Pipeline date of creation.
            * ``"steps"`` (:obj:`list[str]`): List of step names included in the
              pipeline.
            * ``"open_inputs"`` (:obj:`list` of :obj:`dict`): List of open inputs
              of the pipeline. Each open input is represented as a :obj:`dict` with the
              following keys:

              * ``"input_name"`` (:obj:`str`): Name of the open input.
              * ``"step_name"`` (:obj:`str`): Name of the step that provides the open
                input.
              * ``"data_type"`` (:obj:`str`): Data type of the open input.
              * ``"description"`` (:obj:`str`): Description of the open input.
              * ``"default_value"`` (:obj:`str`): Default value of the open input.
              * ``"is_required"`` (:obj:`bool`): Whether the open input is required or
                not.

            * ``"open_outputs"`` (:obj:`list` of :obj:`dict`): List of open outputs
              of the pipeline. Each open output is represented as a :obj:`dict` with the
              following keys:

              * ``"output_name"`` (:obj:`str`): Name of the open output.
              * ``"step_name"`` (:obj:`str`): Name of the step that provides the open
                output.
              * ``"data_type"`` (:obj:`str`): Data type of the open output.
              * ``"description"`` (:obj:`str`): Description of the open output.
        """
        try:
            return self._get_pipeline(pipeline_name)
        except SdkException as error:
            if error.status_code == 404:
                return None
            raise error

    def list_pipelines(self):
        """Get the list of all pipelines.

        Returns:
            :obj:`list` of :obj:`dict`: List of pipelines represented as :obj:`dict`
            with the following keys:

            * ``"pipeline_name"`` (:obj:`str`): Name of the pipeline.
            * ``"created_at"`` (:obj:`str`): Pipeline date of creation.
        """
        url = f"{self.base_environment_api_url}/pipelines"

        return self._get(url)

    @log_func_result("Pipeline deletion")
    def delete_pipeline(self, pipeline_name, force_deployments_deletion=False):
        """Delete a pipeline identified by its name.

        Args:
            pipeline_name (:obj:`str`): Name of the pipeline.
            force_deployments_deletion (:obj:`bool`, optional): if True the associated
                endpoints will be deleted too. Defaults to False.

        Returns:
            :obj:`dict`: The deleted pipeline and its associated deleted deployments
            represented as a :obj:`dict` with the following keys:

                * ``"pipeline"`` (:obj:`dict`): Deleted pipeline represented as
                  :obj:`dict` with the following keys:

                  * ``"name"`` (:obj:`str`): Name of the deleted pipeline.

                * ``"deployments"`` (:obj:`list`): List of deleted deployments
                  represented as :obj:`dict` with the following keys:

                  * ``"name"`` (:obj:`str`): Name of the deleted deployments.
                  * ``"type"`` (:obj:`str`): Type of the deleted deployments.
        """
        url = f"{self.base_environment_api_url}/pipelines/{pipeline_name}"
        params = {
            "force_deployments_deletion": force_deployments_deletion,
        }
        return self._delete(url, params=params)

    # _____ PIPELINE EXECUTIONS _____

    @log_func_result("Pipeline execution startup")
    def run_pipeline(
        self, pipeline_name, inputs=None, inputs_mapping=None, outputs_mapping=None
    ):
        """Run a pipeline.

        Args:
            pipeline_name (:obj:`str`): Name of an existing pipeline.
            inputs (:obj:`dict`, optional): Dictionary of inputs to pass to the pipeline
                with input names as keys and corresponding values as values.
                For files, the value should be the path to the file or a file content
                in an instance of io.IOBase.
                Defaults to None.
            inputs_mapping(:obj:`list` of instances of :class:`InputSource`):
                List of input mappings, to map pipeline inputs to different
                sources (constant_value, environment_variable_name, datastore_path or
                is_null). See :class:`InputSource` for more details.
            outputs_mapping(:obj:`list` of instances of :class:`OutputDestination`):
                List of output mappings, to map pipeline outputs to different
                destinations (is_null or datastore_path). See
                :class:`OutputDestination` for more details.

        Returns:
            :obj:`dict`: Created pipeline execution represented as :obj:`dict` with
            output_names as keys and corresponding values as values.
        """
        if inputs is None:
            inputs = {}
        # Retrieve pipeline input types
        pipeline = self._get_pipeline(pipeline_name)
        pipeline_inputs = pipeline["open_inputs"]
        input_types = {
            input["input_name"]: input["data_type"] for input in pipeline_inputs
        }

        # Get files to upload and data to send
        files = {}
        data = {"json_inputs": {}, "inputs_mapping": []}
        for input_name, input_value in inputs.items():
            if input_types.get(input_name) == INPUT_OUTPUT_TYPES.FILE:
                if isinstance(input_value, str):
                    files[input_name] = open(input_value, "rb")
                elif isinstance(input_value, io.IOBase) and input_value.readable():
                    files[input_name] = input_value
                else:
                    raise SdkException(
                        f"Input {input_name} is a file but \
value is not a string or bytes"
                    )
            elif input_types.get(input_name) != INPUT_OUTPUT_TYPES.FILE:
                data["json_inputs"][input_name] = input_value
        data["json_inputs"] = json.dumps(data["json_inputs"])
        if inputs_mapping is not None:
            if any(
                [
                    not isinstance(input_mapping_, InputSource)
                    for input_mapping_ in inputs_mapping
                ]
            ):
                raise ValueError(
                    "'inputs_mapping' must be a list of instances of InputSource."
                )
            data["inputs_mapping"] = json.dumps(
                [input_mapping_.to_dict() for input_mapping_ in inputs_mapping]
            )
        if outputs_mapping is not None:
            if any(
                [
                    not isinstance(output_mapping_, OutputDestination)
                    for output_mapping_ in outputs_mapping
                ]
            ):
                raise ValueError(
                    "'outputs_mapping' must be a list of instances of \
OutputDestination."
                )
            data["outputs_mapping"] = json.dumps(
                [output_mapping_.to_dict() for output_mapping_ in outputs_mapping]
            )
        # Execute pipeline
        url = f"{self.base_environment_api_url}/pipelines/{pipeline_name}/run"
        post_result = self._post(url, data=data, files=files, allow_redirects=False)
        for file in files.values():
            file.close()
        log_action(
            self,
            f"The pipeline execution may take a while, \
you can check its status and get information on the Executions page of the front-end.\n\
Its execution ID is \"{post_result['execution_id']}\".",
        )
        # Wait for pipeline execution to finish
        execution_id = post_result["execution_id"]
        return self._retrieve_pipeline_execution_outputs(execution_id)

    @log_func_result("Pipeline execution results retrieval")
    def _retrieve_pipeline_execution_outputs(self, execution_id):
        url = (
            f"{self.base_environment_api_url}"
            f"/executions/{execution_id}/outputs?wait_for_results=true"
        )

        do_get = use_authentication(
            lambda sdk, *args, **kwargs: self._session.get(*args, **kwargs)
        )
        response = do_get(self, url, allow_redirects=False)
        while response is None or response.status_code == 307:
            response = do_get(self, url, allow_redirects=False)
        response = handle_http_response(response)

        parsed_response = {}

        for output_item in response["outputs"]:
            value = output_item.get("value", None)
            output_name = output_item["step_output_name"]

            if (
                output_item["data_type"] == INPUT_OUTPUT_TYPES.FILE
                and output_item["mapping_type"] != "is_null"
                and output_item["mapping_type"] != "datastore"
            ):
                value = self._retrieve_pipeline_execution_output_value(
                    execution_id,
                    output_name,
                )

            parsed_response[output_name] = value

        return parsed_response

    def _retrieve_pipeline_execution_output_value(self, execution_id, output_name):
        url = (
            f"{self.base_environment_api_url}"
            f"/executions/{execution_id}/outputs/{output_name}"
        )
        response = self._get(url)
        return response

    def _retrieve_pipeline_execution_input_value(self, execution_id, input_name):
        url = (
            f"{self.base_environment_api_url}"
            f"/executions/{execution_id}/inputs/{input_name}"
        )
        response = self._get(url)
        return response

    def list_pipeline_executions(self, pipeline_name):
        """Get a list of executions for the given pipeline

        Args:
            pipeline_name (:obj:`str`): Name of an existing pipeline.

        Returns:
            :obj:`list`: A list of information on the pipeline execution
            represented as dict with the following keys:

            * ``"execution_id"`` (:obj:`str`): Name of the pipeline execution.
            * ``"status"`` (:obj:`str`): Status of the pipeline execution.
            * ``"created_at"`` (:obj:`str`): Date of creation of the pipeline
              execution.
            * ``"created_by"`` (:obj:`str`): ID of the user who created the pipeline
              execution. In the case of a pipeline run, this is the user who triggered
              the run. In the case of an execution via a deployment, this is the user
              who created the deployment.
            * ``"end_date"`` (:obj:`str`): Date of completion of the pipeline
              execution.
            * ``"pipeline_name"`` (:obj:`str`): Name of the pipeline used for the
              execution.
            * ``"deployment_name"`` (:obj:`str`): Name of the deployment used for the
              execution.
            * ``"steps"`` (:obj:`list` of `obj`): List of the step executions
              represented as :obj:`dict` with the following keys:

              * ``"name"`` (:obj:`str`): Name of the step.
              * ``"status"`` (:obj:`str`): Status of the step.
              * ``"start_date"`` (:obj:`str`): Date of start of the step execution.
              * ``"end_date"`` (:obj:`str`): Date of completion of the step execution.
              * ``"commit_id"`` (:obj:`str`): Id of the commit used to build the
                step.
              * ``"repository_url"`` (:obj:`str`): Url of the repository used to
                build the step.
              * ``"repository_branch"`` (:obj:`str`): Branch of the repository used
                to build the step.
        """
        url = f"{self.base_environment_api_url}/pipelines/{pipeline_name}/executions"

        return self._get(url)

    def get_pipeline_execution(self, execution_id):
        """Get the status of one pipeline execution identified by its execution_id.

        Args:
            execution_id (:obj:`str`): Name of the pipeline execution.

        Returns:
            :obj:`dict`: Information on the pipeline execution represented as dict
            with the following keys:

            * ``"execution_id"`` (:obj:`str`): Name of the pipeline execution.
            * ``"status"`` (:obj:`str`): Status of the pipeline execution.
            * ``"created_at"`` (:obj:`str`): Date of creation of the pipeline
            * ``"created_by"`` (:obj:`str`): ID of the user who created the pipeline
              execution. In the case of a pipeline run, this is the user who triggered
              the run. In the case of an execution via a deployment, this is the user
              who created the deployment.
            * ``"end_date"`` (:obj:`str`): Date of completion of the pipeline
              execution.
            * ``"pipeline_name"`` (:obj:`str`): Name of the pipeline used for the
              execution.
            * ``"deployment_name"`` (:obj:`str`): Name of the deployment used for the
              execution.
            * ``"steps"`` (:obj:`list` of `obj`): List of the step executions
              represented as :obj:`dict` with the following keys:

              * ``"name"`` (:obj:`str`): Name of the step.
              * ``"status"`` (:obj:`str`): Status of the step.
              * ``"start_date"`` (:obj:`str`): Date of start of the step execution.
              * ``"end_date"`` (:obj:`str`): Date of completion of the step execution.
              * ``"commit_id"`` (:obj:`str`): Id of the commit used to build the
                step.
              * ``"repository_url"`` (:obj:`str`): Url of the repository used to
                build the step.
              * ``"repository_branch"`` (:obj:`str`): Branch of the repository used
                to build the step.
            * ``"inputs"`` (:obj:`list` of :obj:`dict`): List of inputs represented
              as a dict with the following keys:

              * ``"step_input_name"`` (:obj:`str`): Name of the input.
              * ``"data_type`` (:obj:`str`): Data type of the input.
              * ``"source`` (:obj:`str`): Source of type of the input. Can be
                "environment_variable", "datastore", "constant", "is_null" "endpoint"
                or "run".
              * ``"endpoint_input_name"`` (:obj:`str`): Name of the input in the
                endpoint execution if source is "endpoint".
              * ``"constant_value"`` (:obj:`str`): Value of the constant if source is
                "constant".
              * ``"environment_variable_name"`` (:obj:`str`): Name of the environment
                variable if source is "environment_variable".
              * ``"is_null"`` (:obj:`bool`): True if source is "is_null".
              * ``"value"``: Value of the input.

            * ``"outputs"`` (:obj:`list` of :obj:`dict`): List of outputs represented
              as a dict with the following keys:

              * ``"step_output_name"`` (:obj:`str`): Name of the output.
              * ``"data_type`` (:obj:`str`): Data type of the output.
              * ``"destination`` (:obj:`str`): Destination of type of the output. Can be
                "datastore", "is_null" "endpoint" or "run".
              * ``"endpoint_output_name"`` (:obj:`str`): Name of the output in the
                endpoint execution if destination is "endpoint".
              * ``"is_null"`` (:obj:`bool`): True if destination is "is_null".
              * ``"value"``: Value of the output.
        """

        url = f"{self.base_environment_api_url}/executions/{execution_id}"

        execution = self._get(url)
        inputs_list = []
        for input_item in execution["inputs"]:
            value = input_item.get("value", None)
            if (
                input_item["data_type"] == INPUT_OUTPUT_TYPES.FILE
                and input_item["mapping_type"] != "is_null"
                and input_item["mapping_type"] != "datastore"
            ):
                value = self._retrieve_pipeline_execution_input_value(
                    execution_id,
                    input_item["step_input_name"],
                )

            inputs_list.append(
                _format_execution_input(
                    input_item["step_input_name"], {**input_item, "value": value}
                )
            )

        outputs_list = []
        for output_item in execution["outputs"]:
            value = output_item.get("value", None)
            if (
                output_item["data_type"] == INPUT_OUTPUT_TYPES.FILE
                and output_item["mapping_type"] != "is_null"
            ):
                value = self._retrieve_pipeline_execution_output_value(
                    execution_id,
                    output_item["step_output_name"],
                )

            outputs_list.append(
                _format_execution_output(
                    output_item["step_output_name"], {**output_item, "value": value}
                )
            )
        execution["inputs"] = inputs_list
        execution["outputs"] = outputs_list
        return execution

    def get_pipeline_execution_output(self, execution_id, output_name):
        """Get the output value of an executed pipeline identified by its execution_id.

        Args:
            execution_id (:obj:`str`): ID of the pipeline execution.
            output_name (:obj:`str`): Name of the output.

        Returns:
            :obj:`dict`: Information on the output represented as a dict with the
            following keys :

            * ``"step_output_name"`` (:obj:`str`): Name of the output.
            * ``"data_type`` (:obj:`str`): Data type of the output.
            * ``"destination`` (:obj:`str`): Destination of type of the output. Can be
              "datastore", "is_null" "endpoint" or "run".
            * ``"endpoint_output_name"`` (:obj:`str`): Name of the output in the
              endpoint execution if destination is "endpoint".
            * ``"is_null"`` (:obj:`bool`): True if destination is "is_null".
            * ``"value"``: Value of the output.
        """
        exec_url = f"{self.base_environment_api_url}/executions/{execution_id}\
?include_io_values=false"
        execution_information = self._get(exec_url)

        output = [
            output_item
            for output_item in execution_information["outputs"]
            if output_item["step_output_name"] == output_name
        ]

        if len(output) == 0:
            raise SdkException(
                f"Cannot find output {output_name} for execution {execution_id}"
            )

        output_value = self._retrieve_pipeline_execution_output_value(
            execution_id,
            output_name,
        )

        return _format_execution_output(
            output_name, {**output[0], "value": output_value}
        )

    def get_pipeline_execution_input(self, execution_id, input_name):
        """Get the input value of an executed pipeline identified by its execution_id.

        Args:
            execution_id (:obj:`str`): ID of the pipeline execution.
            input_name (:obj:`str`): Name of the input.

        Returns:
            :obj:`dict`: Information on the input represented as a dict with the
            following keys :
            * ``"step_input_name"`` (:obj:`str`): Name of the input.
            * ``"data_type`` (:obj:`str`): Data type of the input.
            * ``"source`` (:obj:`str`): Source of type of the input. Can be
            "environment_variable", "datastore", "constant", "is_null" "endpoint"
            or "run".
            * ``"endpoint_input_name"`` (:obj:`str`): Name of the input in the
            endpoint execution if source is "endpoint".
            * ``"constant_value"`` (:obj:`str`): Value of the constant if source is
            "constant".
            * ``"environment_variable_name"`` (:obj:`str`): Name of the environment
            variable if source is "environment_variable".
            * ``"is_null"`` (:obj:`bool`): True if source is "is_null".
            * ``"value"``: Value of the input.
        """

        exec_url = f"{self.base_environment_api_url}/executions/{execution_id}\
?include_io_values=false"
        execution_information = self._get(exec_url)

        input = [
            input_item
            for input_item in execution_information["inputs"]
            if input_item["step_input_name"] == input_name
        ]

        if len(input) == 0:
            raise SdkException(
                f"Cannot find input {input_name} for execution {execution_id}"
            )

        input_value = self._retrieve_pipeline_execution_input_value(
            execution_id,
            input_name,
        )

        return _format_execution_input(input_name, {**input[0], "value": input_value})

    def get_pipeline_execution_logs(
        self,
        pipeline_name,
        execution_id,
        from_datetime=None,
        to_datetime=None,
        limit=None,
    ):
        """Get the logs of an executed pipeline identified by its name.

        Args:
            pipeline_name (:obj:`str`): Name of an existing pipeline.
            execution_id (:obj:`str`): ID of the pipeline execution.
            from_datetime (:obj:`datetime.time`, optional): Datetime from which the logs
                are collected.
            to_datetime (:obj:`datetime.time`, optional): Datetime until which the logs
                are collected.
            limit (:obj:`int`, optional): Maximum number of logs that are collected.

        Returns:
            :obj:`list` of :obj:`dict`: List of collected logs represented as dict with
            the following keys:

            * ``"timestamp"`` (:obj:`str`): Timestamp of the log.
            * ``"message"`` (:obj:`str`): Log message.
        """
        pipeline_url = f"{self.base_environment_api_url}/pipelines/{pipeline_name}"
        url = f"{pipeline_url}/executions/{execution_id}/logs"

        data = {}
        if from_datetime is not None:
            data["from"] = _datetime_to_timestamp_in_ms(from_datetime)
        if to_datetime is not None:
            data["to"] = _datetime_to_timestamp_in_ms(to_datetime)
        if limit is not None:
            data["limit"] = limit

        log_action(
            self,
            "Please wait while logs are being downloaded. This may take a while...",
        )
        logs_by_steps = self._post(url, json=data)

        if len(logs_by_steps) == 0:
            return []

        return logs_by_steps[0]

    def delete_pipeline_execution(self, execution_id):
        """Delete one pipeline execution identified by its execution_id.

        Args:
            execution_id (:obj:`str`): Name of the pipeline execution.

        Returns:
            :obj:`dict`: Deleted pipeline execution represented as dict with
            the following keys:

            * ``"execution_id"`` (:obj:`str`): Name of the pipeline execution.
        """
        url = f"{self.base_environment_api_url}/executions/{execution_id}"
        return self._delete(url)

    # _____ DEPLOYMENTS _____

    @log_func_result("Deployment creation")
    def create_deployment(
        self,
        pipeline_name,
        deployment_name,
        execution_rule,
        schedule=None,
        inputs_mapping=None,
        outputs_mapping=None,
    ):
        """Create a custom deployment associated to a given pipeline.

        Args:
            pipeline_name (:obj:`str`): Name of the pipeline.
            deployment_name (:obj:`str`): Name of the deployment.
            execution_rule(:obj:`str`): Execution rule of the deployment. Must
                be "endpoint" or "periodic". For convenience, members of the enumeration
                :class:`DEPLOYMENT_EXECUTION_RULES` could be used too.
            schedule (:obj:`str`, optional): Schedule of the deployment. Only
                required if ``execution_rule`` is "periodic". Must be a valid
                `cron expression <https://www.npmjs.com/package/croner>`.
                The deployment will be executed periodically according to this schedule.
                The schedule must follow this format:
                ``<minute> <hour> <day of month> <month> <day of week>``.
                Note that the schedule is in UTC time zone.
                '*' means all possible values.
                Here are some examples:

                    * ``"0 0 * * *"`` will execute the deployment every day at
                      midnight.
                    * ``"0 0 5 * *"`` will execute the deployment every 5th day of
                      the month at midnight.

            inputs_mapping(:obj:`list` of instances of :class:`InputSource`):
                List of input mappings, to map pipeline inputs to different
                sources (such as constant values, endpoint inputs, or environment
                variables). See :class:`InputSource` for more details.
                For endpoint rules, if an input of the step in the pipeline is not
                explicitly mapped, it will be automatically mapped to an endpoint
                input with the same name.
                For periodic rules, all inputs of the step in the pipeline must be
                explicitly mapped.
            outputs_mapping(:obj:`list` of instances of :class:`OutputDestination`):
                List of output mappings, to map pipeline outputs to different
                destinations. See :class:`OutputDestination` for more details.
                For endpoint rules, if an output of the step in the pipeline is not
                explicitly mapped, it will be automatically mapped to an endpoint
                output with the same name.
                For periodic rules, all outputs of the step in the pipeline must be
                explicitly mapped.

        Returns:
            :obj:`dict[str, str]`: Created deployment represented as a dict with the
            following keys:

            * ``"name"`` (:obj:`str`): Name of the deployment.
            * ``"endpoint_token"`` (:obj:`str`): Token of the endpoint used to
              trigger the deployment. Note that this token is only returned if
              ``execution_rule`` is "endpoint".
            * ``"schedule"`` (:obj:`str`): Schedule of the deployment. Note that
              this schedule is only returned if ``execution_rule`` is "periodic".
            * ``"human_readable_schedule"`` (:obj:`str`): Human readable schedule
              of the deployment. Note that this schedule is only returned if
              ``execution_rule`` is "periodic".
        """

        if execution_rule not in set(DEPLOYMENT_EXECUTION_RULES):
            raise ValueError(
                "Invalid 'execution_rule', must be in ['endpoint', 'periodic']."
            )

        url = (
            f"{self.base_environment_api_url}/endpoints"
            if execution_rule == "endpoint"
            else f"{self.base_environment_api_url}/periodic-deployment"
        )

        data = {
            "pipeline_name": pipeline_name,
            "name": deployment_name,
        }

        if schedule is not None:
            if execution_rule != "periodic":
                raise ValueError(
                    "'schedule' can only be specified if 'execution_rule' is \
'periodic'."
                )
            else:
                data["schedule"] = schedule

        if inputs_mapping is not None:
            if any(
                [
                    not isinstance(input_mapping_, InputSource)
                    for input_mapping_ in inputs_mapping
                ]
            ):
                raise ValueError("'inputs' must be a list of instances of InputSource.")
            data["inputs"] = [
                input_mapping_.to_dict() for input_mapping_ in inputs_mapping
            ]

        if outputs_mapping is not None:
            if any(
                [
                    not isinstance(output_mapping_, OutputDestination)
                    for output_mapping_ in outputs_mapping
                ]
            ):
                raise ValueError(
                    "'outputs' must be a list of instances of OutputDestination."
                )
            data["outputs"] = [
                output_mapping_.to_dict() for output_mapping_ in outputs_mapping
            ]

        # filter optional parameters
        data = {k: v for k, v in data.items() if v is not None}

        return self._post(url, json=data)

    @log_func_result("Deployment deletion")
    def delete_deployment(self, deployment_name):
        """Delete a deployment identified by its name.

        Args:
            deployment_name (:obj:`str`): Name of the deployment.

        Returns:
            :obj:`dict`: Deleted deployment represented as dict with the following
            keys:

            * ``"name"`` (:obj:`str`): Name of the deployment.
            * ``"type"`` (:obj:`str`): Type of the deployment. Can be "endpoint" or
              "periodic".
        """
        url = f"{self.base_environment_api_url}/deployments/{deployment_name}"
        return self._delete(url)

    def list_deployments(self):
        """Get the list of all deployments.

        Returns:
            :obj:`list` of :obj:`dict`: List of deployments represented as :obj:`dict`
            with the following keys:

            * ``"name"`` (:obj:`str`): Name of the deployment.
            * ``"pipeline_name"`` (:obj:`str`): Name of the pipeline associated to
              the deployment.
            * ``"version"`` (:obj:`str`): Version of the pipeline associated to the
              deployment.
            * ``"execution_count"`` (:obj:`int`): Number of times the deployment has
              been executed.
            * ``"type"`` (:obj:`str`): Type of the deployment. Can be "endpoint", "run"
              or "periodic".
        """
        url = f"{self.base_environment_api_url}/deployments"
        return self._get(url)

    def get_deployment(self, deployment_name):
        """Get information of a deployment.

        Args:
            deployment_name (:obj:`str`): Name of the deployment.

        Returns:
            :obj:`dict`: Deployment information represented as :obj:`dict` with the
            following keys:

            * ``"name"`` (:obj:`str`): Name of the deployment.
            * ``"pipeline"`` (:obj:`dict`): Pipeline associated to the deployment
              represented as :obj:`dict` with the following keys:

              * ``"name"`` (:obj:`str`): Name of the pipeline.

            * ``"inputs_mapping"`` (:obj:`list` of :obj:`dict`): List of inputs
              mapping represented as :obj:`dict` with the following keys:

              * ``"step_input_name"`` (:obj:`str`): Name of the step input.
              * ``"data_type"`` (:obj:`str`): Data type of the step input.
              * ``"description"`` (:obj:`str`): Description of the step input.
              * ``"constant_value"`` (:obj:`str`): Constant value of the step input.
                Note that this key is only returned if the step input is mapped to a
                constant value.
              * ``"environment_variable_name"`` (:obj:`str`): Name of the environment
                variable. Note that this key is only returned if the step input is
                mapped to an environment variable.
              * ``"endpoint_input_name"`` (:obj:`str`): Name of the endpoint input.
                Note that this key is only returned if the step input is mapped to an
                endpoint input.
              * ``"is_null"`` (:obj:`bool`): Whether the step input is mapped to null.
                Note that this key is only returned if the step input is mapped to
                null.
              * ``"datastore_path"`` (:obj:`str`): Datastore path of the step input.
                Note that this key is only returned if the step input is mapped to the
                datastore.
              * ``"is_required"`` (:obj:`bool`): Whether the step input is required.
                Note that this key is only returned if the step input is required.
              * ``"default_value"`` (:obj:`str`): Default value of the step input.
                Note that this key is only returned if the step input has a default
                value.

            * ``"outputs_mapping"`` (:obj:`list` of :obj:`dict`): List of outputs
              mapping represented as :obj:`dict` with the following keys:

              * ``"step_output_name"`` (:obj:`str`): Name of the step output.
              * ``"data_type"`` (:obj:`str`): Data type of the step output.
              * ``"description"`` (:obj:`str`): Description of the step output.
              * ``"endpoint_output_name"`` (:obj:`str`): Name of the endpoint output.
                Note that this key is only returned if the step output is mapped to an
                endpoint output.
              * ``"is_null"`` (:obj:`bool`): Whether the step output is mapped to null.
                Note that this key is only returned if the step output is mapped to
                null.
              * ``"datastore_path"`` (:obj:`str`): Datastore path of the step output.
                Note that this key is only returned if the step output is mapped to
                the datastore.

            * ``"endpoint_token"`` (:obj:`str`): Token of the endpoint. Note that this
              key is only returned if the deployment is an endpoint.
            * ``"schedule"`` (:obj:`str`): Schedule of the deployment. Note that this
              key is only returned if the deployment is a periodic deployment.
            * ``"human_readable_schedule"`` (:obj:`str`): Human readable schedule of
              the deployment. Note that this key is only returned if the deployment is
              a periodic deployment.
        """
        url = f"{self.base_environment_api_url}/deployments/{deployment_name}"
        return self._get(url)

    # _____ ENDPOINTS _____

    @log_func_result("Endpoint trigger")
    def trigger_endpoint(
        self, endpoint_name, endpoint_token, inputs={}, wait_for_results=True
    ):
        """Trigger an endpoint.

        Args:
            endpoint_name (:obj:`str`): Name of the endpoint.
            endpoint_token (:obj:`str`): Token to access endpoint.
            inputs (:obj:`dict`, optional): Dictionary of inputs to pass to the endpoint
                with input names as keys and corresponding values as values.
                For files, the value should be an instance of io.IOBase.
                Defaults to {}.
            wait_for_results (:obj:`bool`, optional): Automatically call
                `retrieve_endpoint_results` and returns the execution result.
                Defaults to `True`.

        Returns:
            :obj:`dict`: Created pipeline execution represented as :obj:`dict` with the
            following keys:

            * ``"execution_id"`` (:obj:`str`): ID of the execution. Note that this key
              is only returned if ``wait_for_results`` is `False`.
            * ``"outputs"`` (:obj:`dict`): Dictionary of outputs of the pipeline with
              output names as keys and corresponding values as values. Note that this
              key is only returned if ``wait_for_results`` is `True`.
        """

        body = {}
        files = {}
        for input_name, input_value in inputs.items():
            if isinstance(input_value, io.IOBase) and input_value.readable():
                files[input_name] = input_value
            else:
                body[input_name] = input_value

        url = f"{self.base_environment_url}/endpoints/{endpoint_name}"
        post_result = requests.post(
            url,
            headers={
                "Authorization": f"EndpointToken {endpoint_token}",
                "craft-ai-client": f"craft-ai-sdk@{self._version}",
            },
            allow_redirects=False,
            json=body,
            files=files,
        )
        parsed_response = handle_http_response(post_result)
        if wait_for_results and 200 <= post_result.status_code < 400:
            return self.retrieve_endpoint_results(
                endpoint_name, parsed_response["execution_id"], endpoint_token
            )
        return parsed_response

    @log_func_result("Endpoint result retrieval")
    def retrieve_endpoint_results(self, endpoint_name, execution_id, endpoint_token):
        """Get the results of an endpoint execution.

        Args:
            endpoint_name (:obj:`str`): Name of the endpoint.
            execution_id (:obj:`str`): ID of the execution returned by
                `trigger_endpoint`.
            endpoint_token (:obj:`str`): Token to access endpoint.

        Returns:
            :obj:`dict`: Created pipeline execution represented as :obj:`dict` with the
            following keys:

            * ``"outputs"`` (:obj:`dict`): Dictionary of outputs of the pipeline with
              output names as keys and corresponding values as values.
        """

        url = (
            f"{self.base_environment_url}"
            f"/endpoints/{endpoint_name}/executions/{execution_id}"
        )
        query = urlencode({"token": endpoint_token})
        response = requests.get(f"{url}?{query}")

        # 500 is returned if the pipeline failed too. In that case, it is not a
        # standard API error
        if response.status_code == 500:
            try:
                return handle_http_response(response)
            except KeyError:
                return response.json()

        if "application/octet-stream" in response.headers.get("Content-Type", ""):
            execution_id = response.headers.get("Execution-Id", "")
            content_disposition = response.headers.get("Content-Disposition", "")
            output_name = content_disposition.split(f"_{execution_id}_")[1]
            return {"outputs": {output_name: handle_http_response(response)}}
        else:
            return handle_http_response(response)

    def generate_new_endpoint_token(self, endpoint_name):
        """Generate a new endpoint token for an endpoint.

        Args:
            endpoint_name (:obj:`str`): Name of the endpoint.

        Returns:
            :obj:`dict[str, str]`: New endpoint token represented as :obj:`dict` with
            the following keys:

            * ``"endpoint_token"`` (:obj:`str`): New endpoint token.
        """
        url = (
            f"{self.base_environment_api_url}"
            f"/endpoints/{endpoint_name}/generate-new-token"
        )
        return self._post(url)

    # _____ DATA STORE _____

    def get_data_store_object_information(self, object_path_in_datastore):
        """Get information about a single object in the data store.

        Args:
            object_path_in_datastore (:obj:`str`): Location of the object in the data
                store.

        Returns:
            :obj:`dict`: Object information, with the following keys:

                * ``"path"`` (:obj:`str`): Location of the object in the data store.
                * ``"last_modified"`` (:obj:`str`): The creation date or last
                  modification date in ISO format.
                * ``"size"`` (:obj:`int`): The size of the object in bytes.
        """
        url = f"{self.base_environment_api_url}/data-store/information"
        data = {
            "path_to_object": object_path_in_datastore,
        }
        return self._post(url, json=data)

    def list_data_store_objects(self):
        """Get the list of the objects stored in the data store.

        Returns:
            :obj:`list` of :obj:`dict`: List of objects in the data store represented
            as :obj:`dict` with the following keys:

                * ``"path"`` (:obj:`str`): Location of the object in the data store.
                * ``"last_modified"`` (:obj:`str`): The creation date or last
                  modification date in ISO format.
                * ``"size"`` (:obj:`int`): The size of the object in bytes.
        """
        url = f"{self.base_environment_api_url}/data-store/list"
        return self._get(url)

    def _get_upload_presigned_url(self, object_path_in_datastore):
        url = f"{self.base_environment_api_url}/data-store/upload"
        params = {"path_to_object": object_path_in_datastore}
        resp = self._get(url, params=params)
        presigned_url, data = resp["signed_url"], resp["fields"]

        return presigned_url, data

    @log_func_result("Object upload")
    def upload_data_store_object(self, filepath_or_buffer, object_path_in_datastore):
        """Upload a file as an object into the data store.

        Args:
            filepath_or_buffer (:obj:`str`, or file-like object): String, path to the
                file to be uploaded ;
                or file-like object implementing a ``read()`` method (e.g. via builtin
                ``open`` function). The file object must be opened in binary mode,
                not text mode.
            object_path_in_datastore (:obj:`str`): Destination of the uploaded file.
        """
        if isinstance(filepath_or_buffer, str):
            # this is a filepath: call the method again with a buffer
            with open(filepath_or_buffer, "rb") as file_buffer:
                return self.upload_data_store_object(
                    file_buffer, object_path_in_datastore
                )

        if not hasattr(filepath_or_buffer, "read"):  # not a readable buffer
            raise ValueError(
                "'filepath_or_buffer' must be either a string (filepath) or an object "
                "with a read() method (file-like object)."
            )
        if isinstance(filepath_or_buffer, io.IOBase) and filepath_or_buffer.tell() > 0:
            filepath_or_buffer.seek(0)

        first_read_size = len(filepath_or_buffer.read(self._MULTIPART_THRESHOLD))
        filepath_or_buffer.seek(0)
        if first_read_size < self._MULTIPART_THRESHOLD:
            return self._upload_singlepart_data_store_object(
                filepath_or_buffer, object_path_in_datastore
            )
        log_action(
            self,
            "Uploading object with multipart (chunk size {:f}MB)".format(
                self._MULTIPART_PART_SIZE / 2**20
            ),
        )
        return self._upload_multipart_data_store_object(
            filepath_or_buffer, object_path_in_datastore
        )

    def _upload_singlepart_data_store_object(self, buffer, object_path_in_datastore):
        files = {"file": buffer}

        presigned_url, data = self._get_upload_presigned_url(object_path_in_datastore)

        resp = requests.post(url=presigned_url, data=data, files=files)
        handle_data_store_response(resp)

    def _upload_multipart_data_store_object(self, buffer, object_path_in_datastore):
        multipart_base_url = (
            f"{self.base_environment_api_url}/data-store/upload/multipart"
        )
        multipart_start_result = self._post(
            url=f"{multipart_base_url}",
            data={"path_to_object": object_path_in_datastore},
        )
        upload_id = multipart_start_result["multipart_upload_id"]

        parts = []
        part_idx = 0
        for chunk in chunk_buffer(buffer, self._MULTIPART_PART_SIZE):
            part_idx += 1
            multipart_part_result = self._get(
                url=f"{multipart_base_url}/{upload_id}",
                params={
                    "path_to_object": object_path_in_datastore,
                    "part_number": part_idx,
                },
            )
            presigned_url = multipart_part_result["signed_url"]

            resp = requests.put(url=presigned_url, data=chunk)
            parts.append(
                {"number": part_idx, "metadata": json.loads(resp.headers["ETag"])}
            )

        self._post(
            url=f"{multipart_base_url}/{upload_id}",
            json={"path_to_object": object_path_in_datastore, "parts": parts},
        )

    def _get_download_presigned_url(self, object_path_in_datastore):
        url = f"{self.base_environment_api_url}/data-store/download"
        data = {
            "path_to_object": object_path_in_datastore,
        }
        presigned_url = self._post(url, data=data)["signed_url"]
        return presigned_url

    @log_func_result("Object download")
    def download_data_store_object(self, object_path_in_datastore, filepath_or_buffer):
        """Download an object in the data store and save it into a file.

        Args:
            object_path_in_datastore (:obj:`str`): Location of the object to download
                from the data store.
            filepath_or_buffer (:obj:`str` or file-like object):
                String, filepath to save the file to ; or a file-like object
                implementing a ``write()`` method, (e.g. via builtin ``open`` function).
                The file object must be opened in binary mode, not text mode.

        Returns:
            None
        """
        presigned_url = self._get_download_presigned_url(object_path_in_datastore)
        resp = requests.get(presigned_url)
        object_content = handle_data_store_response(resp)

        if isinstance(filepath_or_buffer, str):  # filepath
            with open(filepath_or_buffer, "wb") as f:
                f.write(object_content)
        elif hasattr(filepath_or_buffer, "write"):  # writable buffer
            filepath_or_buffer.write(object_content)
            if (
                isinstance(filepath_or_buffer, io.IOBase)
                and filepath_or_buffer.tell() > 0
            ):
                filepath_or_buffer.seek(0)
        else:
            raise ValueError(
                "'filepath_or_buffer' must be either a string (filepath) or an object "
                "with a write() method (file-like object)."
            )

    @log_func_result("Object deletion")
    def delete_data_store_object(self, object_path_in_datastore):
        """Delete an object on the datastore.

        Args:
            object_path_in_datastore (:obj:`str`): Location of the object to be deleted
                in the data store.

        Returns:
            :obj:`dict`: Deleted object represented as dict with the following keys:

              * ``path`` (:obj:`str`): Path of the deleted object.
        """
        url = f"{self.base_environment_api_url}/data-store/delete"
        data = {
            "path_to_object": object_path_in_datastore,
        }
        return self._delete(url, data=data)

    # _____ ENVIRONMENT_VARIABLE _____

    @log_func_result("Environment variable definition")
    def create_or_update_environment_variable(
        self, environment_variable_name, environment_variable_value
    ):
        """Create or update an environment variable available for
        all pipelines executions.

        Args:
            environment_variable_name (:obj:`str`):
               Name of the environment variable to create.
            environment_variable_value (:obj:`str`):
               Value of the environment variable to create.

        Returns:
            None
        """
        url = (
            f"{self.base_environment_api_url}"
            f"/environment-variables/{environment_variable_name}"
        )
        data = {
            "value": environment_variable_value,
        }
        self._put(url, data)
        return None

    def list_environment_variables(self):
        """Get a list of all environments variables.

        Returns:
            :obj:`list` of :obj:`dict`: List of environment variable represented as
            :obj:`dict` with the following keys:

              * ``name`` (:obj:`str`): Name of the environment variable.
              * ``value`` (:obj:`str`): Value of the environment variable.
        """
        url = f"{self.base_environment_api_url}/environment-variables"
        return self._get(url)

    @log_func_result("Environment variable deletion")
    def delete_environment_variable(self, environment_variable_name):
        """Delete the specified environment variable

        Args:
            environment_variable_name (:obj:`str`): Name of the environment variable to
                delete.

        Returns:
            :obj:`dict`: Deleted environment variable represented as :obj:`dict` with
            the following keys:

              * ``name`` (:obj:`str`): Name of the environment variable.
              * ``value`` (:obj:`str`): Value of the environment variable.
        """
        url = (
            f"{self.base_environment_api_url}"
            f"/environment-variables/{environment_variable_name}"
        )
        return self._delete(url)

    # _____ PIPELINE_METRICS _____

    @log_func_result(
        "Pipeline metrics definition", os.environ.get("CRAFT_AI_EXECUTION_ID")
    )
    def record_metric_value(self, name, value):
        """Create or update a pipeline metric. Note that this function can only be used
        inside a step code.

        Args:
            name (:obj:`str`): Name of the metric to store.
            value (:obj:`float`): Value of the metric to store.

        Returns:
            None
        """

        if not os.environ.get("CRAFT_AI_EXECUTION_ID"):
            if self.warn_on_metric_outside_of_step:
                warnings.warn(
                    "You cannot send a metric outside a step code, the metric has not \
been sent"
                )
            return
        url = f"{self.base_environment_api_url}" f"/metrics/single-value/{name}"
        data = {"value": value, "execution_id": os.environ.get("CRAFT_AI_EXECUTION_ID")}
        self._put(url, json=data)
        return None

    @log_func_result(
        "Pipeline list metric definition", os.environ.get("CRAFT_AI_EXECUTION_ID")
    )
    def record_list_metric_values(self, name, values):
        """Add values to a pipeline metric list. Note that this function can only be
        used inside a step code.

        Args:
            name (:obj:`str`):
               Name of the metric list to add values.
            values (:obj:`list` of :obj:`float` or :obj:`float`):
               Values of the metric list to add.

        Returns:
            None
        """

        if not os.environ.get("CRAFT_AI_EXECUTION_ID"):
            if self.warn_on_metric_outside_of_step:
                warnings.warn(
                    "You cannot send a metric outside a step code, the metric has not \
been sent"
                )
            return

        if not isinstance(values, list):
            values = [values]

        BATCH_SIZE = 10000
        for i in range(0, len(values), BATCH_SIZE):
            url = f"{self.base_environment_api_url}" f"/metrics/list-values/{name}"
            data = {
                "values": values[i : i + BATCH_SIZE],
                "execution_id": os.environ.get("CRAFT_AI_EXECUTION_ID"),
            }
            self._post(url, json=data)
        return None

    @log_func_result("Pipeline metrics listing")
    def get_metrics(
        self, name=None, pipeline_name=None, deployment_name=None, execution_id=None
    ):
        """Get a list of pipeline metrics. Note that only one of the
        parameters (pipeline_name, deployment_name, execution_id) can be set.

        Args:
            name (:obj:`str`, optional): Name of the metric to retrieve.
            pipeline_name (:obj:`str`, optional):
                Filter metrics by pipeline, defaults to all the pipelines.
            deployment_name (:obj:`str`, optional):
                Filter metrics by deployment, defaults to all the deployments.
            execution_id (:obj:`str`, optional):
                Filter metrics by execution, defaults to all the executions.

        Returns:
            :obj:`list` of :obj:`dict`: List of execution metrics as :obj:`dict`
            with the following keys:

              * ``name`` (:obj:`str`): Name of the metric.
              * ``value`` (:obj:`float`): Value of the metric.
              * ``created_at`` (:obj:`str`): Date of the metric creation.
              * ``execution_id`` (:obj:`str`): Name of the execution the metric
                belongs to.
              * ``deployment_name`` (:obj:`str`): Name of the deployment the execution
                belongs to.
              * ``pipeline_name`` (:obj:`str`): Name of the pipeline the execution
                belongs to.
        """

        ITEMS_PER_PAGE = 5000

        data = {
            "filters[name]": name,
            "filters[pipeline_name]": pipeline_name,
            "filters[deployment_name]": deployment_name,
            "filters[execution_id]": execution_id,
            "items_per_page": ITEMS_PER_PAGE,
            "page": 1,
        }
        data = remove_none_values(data)

        url = f"{self.base_environment_api_url}/metrics/single-value"

        metrics = []

        result = self._get(url, params=data)
        metrics.extend(result.get("metrics", []))
        total_count = result["total_count"]
        data["page"] += 1

        while len(metrics) < total_count:
            result = self._get(url, params=data)
            metrics.extend(result.get("metrics", []))
            data["page"] += 1
            if metrics == []:
                break

        return metrics

    @log_func_result("Pipeline list metrics listing")
    def get_list_metrics(
        self, name=None, pipeline_name=None, deployment_name=None, execution_id=None
    ):
        """Get a list of pipeline metric lists. Note that only one of the
        parameters (pipeline_name, deployment_name, execution_id) can be set.

        Args:
            name (:obj:`str`, optional): Name of the metric list to retrieve.
            pipeline_name (:obj:`str`, optional):
                Filter metric lists by pipeline, defaults to all the pipelines.
            deployment_name (:obj:`str`, optional):
                Filter metric lists by deployment, defaults to all the deployments.
            execution_id (:obj:`str`, optional):
                Filter metric lists by execution, defaults to all the executions.

        Returns:
            :obj:`list` of :obj:`dict`: List of execution metric lists as :obj:`dict`
            with the following keys:

              * ``name`` (:obj:`str`): Name of the metric.
              * ``value`` (:obj:`float`): Value of the metric.
              * ``created_at`` (:obj:`str`): Date of the metric creation.
              * ``execution_id`` (:obj:`str`): Name of the execution the metric
                belongs to.
              * ``deployment_name`` (:obj:`str`): Name of the deployment the execution
                belongs to.
              * ``pipeline_name`` (:obj:`str`): Name of the pipeline the execution
                belongs to.
        """

        ITEMS_PER_PAGE = 5000

        data = {
            "filters[name]": name,
            "filters[pipeline_name]": pipeline_name,
            "filters[deployment_name]": deployment_name,
            "filters[execution_id]": execution_id,
            "items_per_page": ITEMS_PER_PAGE,
            "page": 1,
        }
        data = remove_none_values(data)

        url = f"{self.base_environment_api_url}/metrics/list-values"

        metrics = []

        result = self._get(url, params=data)
        metrics.extend(result.get("metrics", []))
        total_count = result["total_count"]
        data["page"] += 1

        while len(metrics) < total_count:
            result = self._get(url, params=data)
            metrics.extend(result.get("metrics", []))
            data["page"] += 1
            if metrics == []:
                break

        return metrics
