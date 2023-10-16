from prompt_toolkit.validation import ValidationError


def validate(value, schema):
    # ctrl-d gives us a None
    if value is not None:
        return False, None

    nullable = schema.get("nullable", False)
    if nullable:
        return True, ""
    raise ValidationError(message="Answer is required")
