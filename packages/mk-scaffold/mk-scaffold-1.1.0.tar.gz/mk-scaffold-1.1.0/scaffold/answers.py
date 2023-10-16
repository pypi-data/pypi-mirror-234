import yaml


def load(args, data):
    """
    Load an answers file
    """
    file = args.get("input_file")
    if not file:
        return data

    with open(file, encoding="UTF-8") as fd:
        answers = yaml.safe_load(fd)

    # Copy answers without emptying out values that could have been present
    # in questions file.
    if "answers" not in data:
        data["answers"] = {}
    for k, v in answers.get("answers").items():
        data["answers"][k] = v
    return data
