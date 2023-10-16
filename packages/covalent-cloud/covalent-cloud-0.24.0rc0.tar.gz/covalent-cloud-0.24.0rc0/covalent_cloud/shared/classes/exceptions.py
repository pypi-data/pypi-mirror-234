# Copyright 2023 Agnostiq Inc.


from rich.console import Console

"""Covalent Cloud SDK Exception module."""


class CovalentSDKError(Exception):
    """Covalent Cloud SDK Base Exception class.

    Attributes:
        message (str): Explanation of the error.
        code (str): String enum representing error analogous to error code.
    """

    def __init__(self, message: str = "Generic Error", code: str = "error/generic") -> None:
        """
        Initializes a new instance of the CovalentSDKError class.

        Args:
            message (str): Explanation of the error.
            code (str): String enum representing error analogous to error code.

        """
        self.message = message
        self.code = code
        super().__init__(f"[{code}] {message}")

    def rich_print(self, level: str = "warning") -> None:
        """Print using the Rich module.

        Args:
            level: The level of the message to print.  Defaults to "warning".

        """
        console = Console()
        if level == "warning":
            console.print(f"[bold yellow1]WARNING: {self.message}[bold yellow1]")
        elif level == "error":
            console.print(f"[bold red1]ERROR: {self.message}[bold red1]")


class CovalentAPIKeyError(CovalentSDKError):
    """Covalent Cloud SDK API Key Error class."""

    def __init__(self, message, code) -> None:
        super().__init__(message, code)


class CovalentGenericAPIError(CovalentSDKError):
    """Covalent Cloud Server Generic API Error class."""

    def __init__(self, error) -> None:
        try:
            error_message = error.response.json()["detail"]
            error_code = error.response.json()["code"]
        except:
            error_message = "Unknown Error"
            error_code = "error/unknown"

        super().__init__(error_message, error_code)
