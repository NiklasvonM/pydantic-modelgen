class SchemaConversionError(Exception):
    """Raised when there's an error converting a JSON schema to a Pydantic field."""


class EnumConversionError(Exception):
    """Raised when there's an error converting an enum value to a Pydantic field."""
