from data_analytics_core.exceptions.da_exception_class import DataAnalyticsException


class DataAnalyticsInfraException(DataAnalyticsException):
    def __init__(self):
        self.tech_component = "Infrastructure"
        self.code = None
        self.message = None


class FileKeyError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class FileKeyWarning(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message


class ProviderPrefixError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class EventInfoExtractionError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANotExpectedPriceValueErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANotExpectedIDValueErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ParamNotExistentError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ColumnsNotFoundError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ColumnTypeError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ProviderSFTPNameError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DifferingMetadataBetweenFilesWarning(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "WAR.0.00.00"
        self.message = message


class S3ObjectNotFoundWarning(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "WAR.0.00.00"
        self.message = message


class WarningsFoundDuringMetadataCheckWarning(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "WAR.0.00.00"
        self.message = message


class FileTypeError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class NotExpectedFileTypeError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class FileDialectEncodingNotExpectedError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class UnexpectedPathToProcessedFromPrefixError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class ParsedFileError(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQAYearNotExpectedErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonIntegerValueErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonPositiveIntegerValueErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANoPartsPerUnitErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonDateFormatValuesErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonDatetimeFormatErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class DataQANonInePeriodoSpecificFormatErrorInfra(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "ERR.1.00.00"
        self.message = message


class NonStandardCSVFormattWarning(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message


class SLIParsingWarning(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message


class RenamedColumnsAsExpectedWarning(DataAnalyticsInfraException):
    def __init__(self, message):
        self.code = "WARN.0.00.00"
        self.message = message
