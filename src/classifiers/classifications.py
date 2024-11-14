from enum import StrEnum


class FileClassification(StrEnum):
    DRIVERS_LICENCE = "drivers_licence"
    BANK_STATEMENT = "bank_statement"
    INVOICE = "invoice"
    UNKNOWN = "unknown"