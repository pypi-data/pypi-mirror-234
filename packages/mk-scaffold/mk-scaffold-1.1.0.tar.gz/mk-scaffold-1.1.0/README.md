[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/jlecomte/python/mk-scaffold/badges/master/pipeline.svg)](https://gitlab.com/jlecomte/python/mk-scaffold/pipelines)
[![coverage](https://gitlab.com/jlecomte/python/mk-scaffold/badges/master/coverage.svg)](https://jlecomte.gitlab.io/python/mk-scaffold/coverage/index.html)

# mk-Scaffold -- make scaffold

A cookiecutter clone. A command-line utility that creates projects from templates.

## Features

- Conditional questions.
- Templated answers.
- Jinja2 extensions per template project.
- You don't have to know/write Python code to use Cookiecutter.
- Project templates can be in any programming language or markup format:
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name it.
  You can use multiple languages in the same project template.

## Installation from PyPI

You can install the latest version from PyPI package repository.

~~~bash
python3 -mpip install -U mk-scaffold
~~~

## Usage

Sample command line usage:

~~~bash
mk-scaffold clone https://gitlab.com/jlecomte/scaffold-project-template.git
~~~

Sample scaffold template file `scaffold.yml`:

~~~yml
questions:
  - name: "project_name"
    schema:
      min_length: 1

  - name: "project_short_description"
    schema:
      default: "Lorem ipsum sit dolor amet."
      max_length: 120
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Locations

  * GitLab: [https://gitlab.com/jlecomte/python/mk-scaffold](https://gitlab.com/jlecomte/python/mk-scaffold)
  * PyPi: [https://pypi.org/project/mk-scaffold](https://pypi.org/project/mk-scaffold)
