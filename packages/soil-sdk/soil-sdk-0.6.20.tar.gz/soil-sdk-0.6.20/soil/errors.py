"""Exceptions for SOIL-SDK"""


class SoilSDKError(Exception):
    """Common soil-sdk exception"""


class LoginError(SoilSDKError):
    """Exception to raise when unable to login Soil"""


class ExperimentError(SoilSDKError):
    """Exception to raise when an error has occurred while executing a Soil experiment"""


class ObjectNotFound(SoilSDKError):
    """Exception to raise when Soil object could not be found"""


class DictionaryNotFound(ObjectNotFound):
    """Exception to raise when Soil Dictionary could not be found"""


class DataNotFound(ObjectNotFound):
    """Exception to raise when Soil data could not be found"""


class ModuleNotFound(ObjectNotFound):
    """Exception to raise when Soil module could not be found"""


class ObjectNotUploaded(SoilSDKError):
    """Exception to raise when Soil object could not be uploaded"""


class DictionaryNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil Dictionary could not be uploaded"""


class DataNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil data could not be uploaded"""


class ModuleNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil Module could not be uploaded"""


class AlertDataNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil alert could not be uploaded"""


class AlertNotUploaded(AlertDataNotUploaded):
    """Exception to raise when Soil alert condition could not be uploaded"""


class EventNotUploaded(AlertDataNotUploaded):
    """Exception to raise when Soil event alert could not be uploaded"""


class DataStructureError(SoilSDKError):
    """Exception to raise when Soil DataStructure has any error"""


class DataStructureType(DataStructureError):
    """Exception to raise when Soil DataStructure type is not recognised"""


class DataStructurePipelineNotFound(DataStructureError):
    """Exception to raise when Soil DataStructure Pipeline is not found"""
