"""
Ask questions and answer them by prompting the user
"""
import sys
from datetime import datetime

from prompt_toolkit import prompt as user_input
from prompt_toolkit.validation import ValidationError, Validator

from . import utils
from .environment import StrictNativeEnvironment
from .validators import allowed, boolean, default, max_length, min_length, nullable, vartype


def _templatize(what, env, ctx):
    if isinstance(what, str):
        return env.from_string(what).render(**ctx)
    return what


def validate_answer(value, schema):
    """
    Validate the answer and return modified answer if needed.
    """
    # Order matters. By checking nullable and default first
    # we can make assumptions on values (null? not null? etc.)
    validators = [
        vartype,
        nullable,
        default,
        vartype,  # force the default value type to be of type X
        allowed,
        boolean,
        max_length,
        min_length,
    ]

    # Returns (True, Any) if we are to stop iterating,
    # Returns (Any, Value) if we are to replace value by
    # a new value
    for validator in validators:
        valid, new_value = validator.validate(value, schema)
        if new_value is not None:
            value = new_value
        if valid is True:
            return valid, value
    return True, value


def stdin_input(prompt):
    """
    Convenience function in order to be mocked
    """
    return input(prompt)


def prompt_question(question, env, ctx):
    """
    Ask the question until it is answered or canceled
    """
    # Get question details
    name = question["name"]
    prompt = question["prompt"] + ": "
    description = question.get("description")
    schema = question.get("schema", {})

    # if hidden, then return default
    hidden = schema.get("hidden", False)
    hidden = _templatize(hidden, env, ctx)
    if utils.string_as_bool(hidden):
        return name, schema.get("default")

    def prevalidate_answer(x, schema):
        return validate_answer(x, schema)[0]

    validator = Validator.from_callable(lambda x: prevalidate_answer(x, schema))

    while True:
        try:
            if sys.stdin.isatty():
                answer = user_input(
                    prompt,
                    validator=validator,
                    bottom_toolbar=description,
                    validate_while_typing=False,
                )
            else:
                answer = stdin_input(prompt)
            _, answer = validate_answer(answer, schema)
            return name, answer

        except EOFError:
            # ctrl-d was used
            try:
                _, answer = validate_answer(None, schema)
                return name, answer
            except ValidationError:
                continue


def prepare_question(question, answers, env, ctx):
    """
    Determine if the question is to be asked, and
    if so, build a prompt
    Return true if question is to be asked.
    """
    # Get question details
    name = question["name"]
    schema = question.get("schema", {})

    # Will we prompt this question?
    when = question.get("if")
    when = _templatize(when, env, ctx)
    if when is not None:
        question["if"] = when
        if not when:
            return False

    # Prepare answer to prepare default
    answer = (answers or {}).get(question["name"])
    if answer is not None:
        schema["default"] = answer

    # Build default
    # pylint: disable=redefined-outer-name
    default = schema.get("default")
    default = _templatize(default, env, ctx)
    if default is not None:
        schema["default"] = default

    # Build prompt
    question["prompt"] = name
    if default is not None:
        question["prompt"] += f" [{default}]"
    return True


def prompt_questions(args, data):
    """
    For every question in the input file, ask the question
    and record the answer in the context

    Fills in `questions`
    """

    # jinja context, everything of ours is "scaffold".* based
    # globals are set at the root
    ctx = {"scaffold": {}, "year": datetime.now().year}

    # Get user options for jinja from questions file.
    jinja2 = data.get("jinja2", {})

    env = StrictNativeEnvironment(context=data.get("extensions"), path=args["template_dir"], **jinja2)

    questions = data.get("questions") or []
    answers = data.get("answers") or {}
    for question in questions:
        if not prepare_question(question, answers, env, ctx):
            continue

        name, answer = prompt_question(question, env, ctx)
        if name is not None:
            question["value"] = answer
            if question.get("schema", {}).get("type", "string") == "boolean":
                answer = utils.string_as_bool(answer)
            ctx["scaffold"][name] = answer
    return env, ctx
