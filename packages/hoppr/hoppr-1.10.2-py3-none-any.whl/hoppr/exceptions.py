"""Hoppr exceptions and warnings."""


class HopprError(RuntimeError):
    """Base exception raised within the hoppr app."""


class HopprPluginError(HopprError):
    """Exception raised for errors working with plug-ins."""


class HopprLoadDataError(HopprError):
    """Exception raised for errors loading json/yml data."""


class HopprCredentialsError(HopprError):
    """Exception raised for errors loading credential data."""


class HopprExperimentalWarning(UserWarning):
    """Warning raised when experimental features are accessed."""
