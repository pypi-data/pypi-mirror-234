from prompt_toolkit.validation import ValidationError


def validate(value, schema):
    # ignore ctrl-d
    if value is None:
        return False, None
    # value must be "" to set a default
    if value != "":
        return False, None

    default = schema.get("default")
    if default is not None:
        return False, default

    # there's no default, yet answer was "", so
    # show an error message
    nullable = schema.get("nullable", False)
    if nullable:
        raise ValidationError(message="Answer, or empty (ctrl-d), is required")
    else:
        raise ValidationError(message="Answer is required")
