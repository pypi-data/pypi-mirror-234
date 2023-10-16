from prompt_toolkit.validation import ValidationError


def validate(value, schema):
    # ctrl-d gives us a None
    if value is None:
        return False, None

    vartype = schema.get("type", "string")
    if vartype == "string":
        value = str(value)

    return False, value
