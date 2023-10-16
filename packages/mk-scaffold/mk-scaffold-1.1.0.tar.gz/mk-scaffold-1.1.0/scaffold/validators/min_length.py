from prompt_toolkit.validation import ValidationError


def validate(value, schema):
    vartype = schema.get("type", "string")
    if vartype != "string":
        return False, None

    min_length = schema.get("min_length", None)
    if min_length and len(value) < min_length:
        raise ValidationError(message=f"Answer cannot be shorter than {min_length} characters")
    return False, None
