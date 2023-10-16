from prompt_toolkit.validation import ValidationError


def validate(value, schema):
    vartype = schema.get("type", "string")
    if vartype != "string":
        return False, None

    max_length = schema.get("max_length", None)
    if max_length and len(value) > max_length:
        raise ValidationError(message=f"Answer cannot be longer than {max_length} characters")
    return False, None
