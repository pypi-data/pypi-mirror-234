"""Context manager to handle REST errors."""
import ast
from http import HTTPStatus
from types import TracebackType
from typing import Optional, Type

from rime_sdk.swagger.swagger_client.rest import ApiException


class RESTErrorHandler:
    """Class that can be used as a context manager.

    Used so that we handle REST errors in a uniform way in the code base.
    """

    def __enter__(self) -> None:
        """Needed for context manager usage."""

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Handle exceptions in custom way on exit."""
        # Check if an exception was raised.
        if exc_type is not None:
            # For ApiException errors, we only raise the details.
            if isinstance(exc, ApiException):
                if exc.body:
                    # Authentication (401) errors need to be handled separately as they are nginx messages
                    if exc.status == HTTPStatus.UNAUTHORIZED:
                        raise ValueError(
                            f"{exc.reason}: Your API token is either invalid or "
                            f"expired. Please generate a new API token from the API "
                            f"Access Tokens page under Workspace Settings."
                        ) from None
                    else:
                        body_string = exc.body.decode("UTF-8")
                        # Safely interpret string as a python dict to pull out message
                        body_dict = ast.literal_eval(body_string)
                        raise ValueError(
                            f"{exc.reason}: {body_dict['message']}"
                        ) from None
                else:
                    raise ValueError(exc.reason) from None
        # Returning None will raise any other error messages as they were.
        return None
