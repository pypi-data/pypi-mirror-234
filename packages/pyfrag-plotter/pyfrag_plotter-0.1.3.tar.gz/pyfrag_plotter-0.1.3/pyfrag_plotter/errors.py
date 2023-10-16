from typing import Optional

# ====================================================================================================
# Base Error =========================================================================================
# ====================================================================================================


class PyFragError(ValueError):
    def __init__(self, message, key: Optional[str] = None):
        if key is not None:
            message = f"{key} is not valid. {message}"
        super().__init__(message)
        self.key = key


# ====================================================================================================
# PyFrag Warning =====================================================================================
# ====================================================================================================

class PyFragResultsProcessingWarning(Warning):
    """An error that occurs when processing PyFrag results."""

    def __init__(self, message, section: str):
        if section is not None:
            message = f"Error in {section}. {message}"
        super().__init__(message)
        self.key = section

# ====================================================================================================
# PyFrag Errors ======================================================================================
# ====================================================================================================


class PyFragInputError(ValueError):
    """An error that occurs when the PyFrag input is invalid."""

    def __init__(self, message, key: Optional[str] = None):
        if key is not None:
            message = f"{key} is not valid. {message}"
        super().__init__(message)
        self.key = key


class PyFragResultsProcessingError(PyFragError):
    """An error that occurs when processing PyFrag results."""


class PyFragConfigError(PyFragError):
    """An error that occurs when the PyFrag configuration is invalid."""


class PyFragResultsObjectError(PyFragError):
    """An error that occurs when a PyFrag results object is invalid."""


class PyFragConfigValidationError(PyFragError):
    """An error that occurs when the PyFrag config is invalid."""
