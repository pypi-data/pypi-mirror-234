"""Library defining the interface to the generative firewall."""
import atexit
from pathlib import Path
from typing import List, Optional, Union

from urllib3.util import Retry

from rime_sdk.client import RETRY_HTTP_STATUS
from rime_sdk.internal.file_upload import GenerativeFirewallFileUploader
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.swagger.swagger_client import (
    ApiClient,
    Configuration,
    FirewallApi,
    FirewallConfigurationApi,
    GenerativefirewallFirewallRuleConfig,
    GenerativefirewallValidateRequest,
    ValidateRequestInput,
    ValidateRequestOutput,
)
from rime_sdk.swagger.swagger_client.models.rime_language import RimeLanguage

_DEFAULT_CHANNEL_TIMEOUT = 60.0


VALID_LANGUAGES = [
    RimeLanguage.EN,
    RimeLanguage.JA,
]


class GenerativeFirewall:
    """An interface to a Generative Firewall object.

    To initialize the GenerativeFirewall, provide the address of your RIME instance.

    Args:
        domain: str
            The base domain/address of the RIME service.
        api_key: str
            The API key used to authenticate to RIME services.
        channel_timeout: float
            The amount of time in seconds to wait for responses from the cluster.

    Example:
        .. code-block:: python

            firewall = GenerativeFirewall("my_vpc.rime.com", "api-key")
    """

    def __init__(
        self,
        domain: str,
        api_key: str = "",
        channel_timeout: float = _DEFAULT_CHANNEL_TIMEOUT,
    ):
        """Create a new Client connected to the services available at `domain`."""
        configuration = Configuration()
        configuration.api_key["X-Firewall-Api-Key"] = api_key
        if domain.endswith("/"):
            domain = domain[:-1]
        if not domain.startswith("https://") and not domain.startswith("http://"):
            domain = "https://" + domain
        configuration.host = domain
        self._api_client = ApiClient(configuration)
        # Prevent race condition in pool.close() triggered by swagger generated code
        atexit.register(self._api_client.pool.close)
        # Sets the timeout and hardcoded retries parameter for the api client.
        self._api_client.rest_client.pool_manager.connection_pool_kw[
            "timeout"
        ] = channel_timeout
        self._api_client.rest_client.pool_manager.connection_pool_kw["retries"] = Retry(
            total=3, status_forcelist=RETRY_HTTP_STATUS
        )
        self._firewall_client = FirewallApi(self._api_client)
        self._configuration_client = FirewallConfigurationApi(self._api_client)

    def validate(
        self, input: Optional[str] = None, output: Optional[str] = None
    ) -> List[dict]:
        """Validate model input and/or output text.

        Args:
            input: Optional[str]
                The user input text to validate.
            output: Optional[str]
                The model output text to validate.

        Returns:
            List[dict]:
                A list of validation results, each of which is a dictionary of rule
                results for the input or output text.

        Raises:
            ValueError:
                If neither input nor output text is provided or when there was an error
                in the validation request to the RIME backend.

        Example:
            .. code-block:: python

                results = firewall.validate(
                    input="Hello!", output="Hi, how can I help you?"
                )
        """
        if input is None and output is None:
            raise ValueError("Must provide either input or output text to validate.")

        body = GenerativefirewallValidateRequest(
            input=ValidateRequestInput(user_input_text=input),
            output=ValidateRequestOutput(output_text=output),
        )
        with RESTErrorHandler():
            response = self._firewall_client.firewall_validate(body=body)
        return [res.to_dict() for res in response.results]

    def upload_file(self, file_path: Union[Path, str]) -> str:
        """Upload a file to make it accessible to the RIME cluster.

        The uploaded file is stored in the RIME cluster in a blob store
        using its file name.

        Args:
            file_path: Union[Path, str]
                Path to the file to be uploaded to RIME's blob store.

        Returns:
            str:
                A reference to the uploaded file's location in the blob store. This
                reference can be used to refer to that object when writing RIME configs.
                Please store this reference for future access to the file.

        Raises:
            FileNotFoundError
                When the path ``file_path`` does not exist.
            IOError
                When ``file_path`` is not a file.
            ValueError
                When there was an error in obtaining a blobstore location from the
                RIME backend or in uploading ``file_path`` to RIME's blob store.
                When the file upload fails, the incomplete file is
                NOT automatically deleted.

        Example:
             .. code-block:: python

                uploaded_file_path = firewall.upload_file(file_path)
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)

        with RESTErrorHandler():
            file_uploader = GenerativeFirewallFileUploader(self._api_client)
            return file_uploader.upload_file(file_path)

    def update_config(self, firewall_config: dict) -> dict:
        """Update the firewall configuration.

        The update is performed via a PATCH request by merging the provided
        `firewall_config` with the existing config, meaning that any fields not
        explicitly provided in `firewall_config` will not be overwritten.

        Args:
            firewall_config: dict
                A dictionary containing the firewall configuration components to update.

        Returns:
            dict:
                The updated firewall configuration.

        Raises:
            ValueError:
                If `firewall_config` is empty or contains unexpected keys, or when there
                was an error in the update request to the RIME backend.

        Example:
             .. code-block:: python

                updated_config = firewall.update_config(firewall_config)
        """
        _config = firewall_config.copy()
        language = _config.pop("language", None)
        if language is not None and language not in VALID_LANGUAGES:
            raise ValueError(
                f"Provided language {language} is invalid, please choose one of the following values {VALID_LANGUAGES}"
            )
        body = GenerativefirewallFirewallRuleConfig(
            fact_sheet_url=_config.pop("fact_sheet_url", None),
            sensitive_terms_url=_config.pop("sensitive_terms_url", None),
            allowed_topics=_config.pop("allowed_topics", None),
            selected_rules=_config.pop("selected_rules", None),
            language=language,
        )

        if _config:
            raise ValueError(
                "Found unexpected keys in firewall_config: " f"{list(_config.keys())}"
            )
        if all(val is None for val in body.to_dict().values()):
            raise ValueError("Must provide a non-empty firewall_config to update.")

        with RESTErrorHandler():
            response = (
                self._configuration_client.firewall_configuration_configure_firewall(
                    body
                )
            )
        return response.config.to_dict()
