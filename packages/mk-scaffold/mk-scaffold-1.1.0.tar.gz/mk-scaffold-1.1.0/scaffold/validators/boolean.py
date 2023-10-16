from prompt_toolkit.validation import ValidationError

from ..utils import string_as_bool


def validate(value, schema):
    vartype = schema.get("type", "string")
    if vartype != "boolean":
        return False, None

    try:
        return True, string_as_bool(value)
    except ValueError:
        raise ValidationError(message="Answer must be a boolean (true/false, yes/no)") from None
