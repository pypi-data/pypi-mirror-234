from prompt_toolkit.validation import ValidationError


def validate(value, schema):
    allowed = schema.get("allowed")
    if allowed is None:
        return False, None

    if value not in allowed:
        allowed = ", ".join(allowed)
        raise ValidationError(message=f"Answer must be within [{allowed}]")

    return False, value
