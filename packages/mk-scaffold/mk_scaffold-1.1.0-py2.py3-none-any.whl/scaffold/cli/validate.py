"""
Scheme validation of scaffold.yml file
"""

import json
import os
import sys

import cerberus
import yaml

from .. import template

# https://docs.python-cerberus.org/en/stable/validation-rules.html
SCHEMA = r"""
---
extensions:
  type: list
  default: []
  schema:
    type: string

jinja2:
  type: dict
  default: {}
  schema:
    lstrip_blocks:
      type: boolean
    trim_blocks:
      type: boolean

files:
  type: list
  default: []
  schema:
    type: dict
    default: {}
    nullable: true
    schema:
      path:
        type: string
        required: true
      if:
        type: [string, boolean]
      action:
        type: string
        required: true

questions:
  type: list
  default: []
  schema:
    type: dict
    default: {}
    nullable: true
    schema:
      name:
        type: string
        regex: '^\S+$'
        required: true
      description:
        type: string
      value:
        type: [string, boolean]
      if:
        type: [string, boolean]
      schema:
        type: dict
        default: {}
        nullable: true
        schema:
          type:
            type: string
            allowed: ["string", "boolean"]
          default:
            type: [string, boolean]
          hidden:
            type: boolean
            default: false
          nullable:
            type: boolean
            default: true
          min_length:
            type: integer
            min: 0
          max_length:
            type: integer
            min: 0
          allowed:
            type: list
            schema:
              type: string
"""


def _validate_schema(args):
    """
    Validate the YAML part of the template
    """
    data = template.get(args)
    schema = yaml.safe_load(SCHEMA)
    validator = cerberus.Validator(schema)
    if not validator.validate(data):
        sys.exit("error: YAML schema validation error. Location:\n" + str(json.dumps(validator.errors, indent=2)))
    return data


def _validate_template_existance(args):
    """
    Validate that a folder named 'template' exists
    """
    path = args["template_dir"]
    path = os.path.join(path, "template")
    if not os.path.isdir(path):
        sys.exit('error: no "template" directory found in source template location')


def _validate_file_actions(data):
    for file in data.get("files", []):
        action = file.get("action")
        if action not in ["remove"]:
            sys.exit(f'error: unknown file action "{action}"')


def _validate_questions(data):
    for question in data.get("questions", []):
        schema = question.get("schema")
        if not schema:
            continue

        if "allowed" in schema:
            if schema.get("type", "string") != "string":
                sys.exit('error: field "allowed" only allows using a "string" type')
            if "min_length" in schema:
                print('warning: presence of field "allowed" with a "min_length" type')
            if "max_length" in schema:
                print('warning: presence of field "allowed" with a "max_length" type')

        if schema.get("hidden", False):
            if schema.get("default") is None:
                sys.exit('error: field "hidden" requires a "default" value')


def validate(args):
    """
    Called from cli
    """
    data = _validate_schema(args)
    _validate_template_existance(args)
    _validate_questions(data)
    _validate_file_actions(args)
