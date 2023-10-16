import os
import shutil
import sys

import jinja2
from boltons import fileutils

from .. import answers, questions, template
from ..environment import StrictEnvironment, StrictNativeEnvironment


def clone_tree(args, data, ctx):
    # TODO: Verify before questions
    #
    # Get user options
    jinja_vars = data.get("jinja2", {})
    nenv = StrictNativeEnvironment(context=data.get("extensions"), path=args["template_dir"], **jinja_vars)
    env = StrictEnvironment(context=data.get("extensions"), path=args["template_dir"], **jinja_vars)

    # Get the template source directory (from command line)
    # It's the folder containing another folder named "template"
    source_path = args["template_dir"]
    source_path = os.path.join(source_path, "template")
    source_path = os.path.abspath(source_path)

    if not os.path.isdir(source_path):
        sys.exit('error: no "template" named folder found in source template directory. No templating can be done')

    # For every source file, replace templates, and create file
    output = args.get("output_dir", ".")
    for src in fileutils.iter_find_files(source_path, "*", include_dirs=True):
        dst = os.path.relpath(src, source_path)
        try:
            dst = nenv.from_string(dst).render(**ctx)
        except jinja2.exceptions.UndefinedError as err:
            sys.exit(f'error: templating error during "{src}" file: {err}')
        dst = os.path.join(output, dst)

        if os.path.islink(src):
            # TODO: Change destination
            assert False, "change link destination"
        elif os.path.isdir(src):
            fileutils.mkdir_p(dst)
        else:
            fileutils.mkdir_p(os.path.dirname(dst))
            try:
                with open(src, encoding="UTF-8") as fd:
                    dst_contents = fd.read()
                    dst_contents = env.from_string(dst_contents).render(**ctx)
                with open(dst, mode="w", encoding="UTF-8") as fd:
                    fd.write(str(dst_contents))
                shutil.copymode(src, dst)

            except UnicodeDecodeError:
                with open(src, mode="rb") as fd:
                    dst_contents = fd.read()
                with open(dst, mode="wb") as fd:
                    fd.write(dst_contents)
                shutil.copymode(src, dst)

            except jinja2.exceptions.UndefinedError as err:
                sys.exit(f'error: while rendering "{src}", encountered template error: {err}')
            except jinja2.exceptions.TemplateSyntaxError as err:
                sys.exit(f'error: while rendering "{src}", encountered template error: {err}')

    return ctx


def clean_tree(args, env, ctx, files):
    if not files:
        return

    # Prepare path
    output_dir = args["output_dir"]
    template_path = os.path.join(os.getcwd(), output_dir)
    template_path = os.path.abspath(template_path)

    # files is the name of the dict, not a file on filesystem
    for field in files:
        paths = field["path"]
        if not isinstance(paths, list):
            paths = [paths]

        for path in paths:
            path = env.from_string(path).render(**ctx)

            # we'll read the action field by default
            action_field = "action"

            when = field["if"]
            when = env.from_string(when).render(**ctx)
            if not when:
                if field.get("else") is None:
                    continue
                # switch to else case
                action_field = "else"

            path = os.path.abspath(os.path.join(template_path, path))
            if not path.startswith(template_path):
                sys.exit("error: can only delete files in template's subpath")

            if not os.path.exists(path):
                # file disapeared, skip
                continue

            action = field[action_field].lower()
            if action == "remove":
                if os.path.islink(path):
                    os.remove(path)
                elif os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            elif action == "move":
                dest = field.get("dest", "")
                dest = env.from_string(dest).render(**ctx)
                dest = os.path.abspath(os.path.join(template_path, dest))
                if not dest.startswith(template_path):
                    sys.exit("error: can only move files into template's subpath")

                shutil.move(path, dest)
            else:
                sys.exit(f'error: unknown "action" (or "else") for file path "{path}"')


def clone(args):
    """
    Ask the questions, and clone the tree, not a repository
    """
    # Get local folder from which we can load files from
    data = template.get(args)
    data = answers.load(args, data)
    env, ctx = questions.prompt_questions(args, data)

    ctx = clone_tree(args, data, ctx)

    bus = data.get("files") or []
    clean_tree(args, env, ctx, bus)
