# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cappa', 'cappa.completion']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.15,<0.16',
 'rich',
 'typing-extensions>=4.7.1,<5.0.0',
 'typing-inspect>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'cappa',
    'version': '0.7.0',
    'description': '',
    'long_description': '# Cappa\n\n[![Actions Status](https://github.com/DanCardin/cappa/actions/workflows/test.yml/badge.svg)](https://github.com/dancardin/cappa/actions)\n[![Coverage Status](https://coveralls.io/repos/github/DanCardin/cappa/badge.svg?branch=main)](https://coveralls.io/github/DanCardin/cappa?branch=main)\n[![Documentation Status](https://readthedocs.org/projects/cappa/badge/?version=latest)](https://cappa.readthedocs.io/en/latest/?badge=latest)\n\n- [Full documentation here](https://cappa.readthedocs.io/en/latest/).\n- [Comparison vs existing libraries.](https://cappa.readthedocs.io/en/latest/comparison.html).\n- [Annotation inference details](https://cappa.readthedocs.io/en/latest/annotation.html)\n- ["invoke" (click-like) details](https://cappa.readthedocs.io/en/latest/invoke.html)\n\nCappa is a declarative command line parsing library, taking much of its\ninspiration from the "Derive" API from the\n[Clap](https://docs.rs/clap/latest/clap/_derive/index.html) written in Rust.\n\n```python\nfrom dataclasses import dataclass\nimport cappa\nfrom typing_extensions import Annotated\n\n\n@dataclass\nclass Example:\n    positional_arg: str\n    boolean_flag: bool\n    single_option: Annotated[int | None, cappa.Arg(long=True)]\n    multiple_option: Annotated[list[str], cappa.Arg(short=True)]\n\n\nargs: Example = cappa.parse(Example)\n```\n\nProduces the following CLI:\n\n```\nmeow.py --boolean-flag [--single-option single_option] -m\n               multiple_option [-h]\n               positional_arg\n\nPositional Arguments:\n  positional_arg\n\nOptions:\n  --boolean-flag\n  --single-option single_option\n  -m multiple_option\n\nHelp:\n  -h, --help            Show this message and exit\n```\n\nIn this way, you can turn any dataclass-like object (with some additional\nannotations, depending on what you\'re looking for) into a CLI.\n\nYou\'ll note that `cappa.parse` returns an instance of the class. This API should\nfeel very familiar to `argparse`, except that you get the fully typed dataclass\ninstance back instead of a raw `Namespace`.\n\n## Invoke\n\n["invoke" documentation](https://cappa.readthedocs.io/en/latest/invoke.html)\n\nThe "invoke" API is meant to feel more like the experience you get when using\n`click` or `typer`. You can take the same dataclass, but register a function to\nbe called on successful parsing of the command.\n\n```python\nfrom dataclasses import dataclass\nimport cappa\nfrom typing_extensions import Annotated\n\ndef function(example: Example):\n    print(example)\n\n@cappa.command(invoke=function)\nclass Example:  # identical to original class\n    positional_arg: str\n    boolean_flag: bool\n    single_option: Annotated[int | None, cappa.Arg(long=True)]\n    multiple_option: Annotated[list[str], cappa.Arg(short=True)]\n\n\ncappa.invoke(Example)\n```\n\n(Note the lack of the dataclass decorator. You can optionally omit or include\nit, and it will be automatically inferred).\n\nAlternatively you can make your dataclass callable, as a shorthand for an\nexplcit invoke function:\n\n```python\n@dataclass\nclass Example:\n    ...   # identical to original class\n\n    def __call__(self):\n       print(self)\n```\n\nNote `invoke=function` can either be a reference to some callable, or a string\nmodule-reference to a function (which will get lazily imported and invoked).\n\nWith a single top-level command, the click-like API isn\'t particularly valuable\nby comparison. Click\'s command-centric API is primarily useful when composing a\nnumber of nested subcommands.\n\n## Subcommands\n\nThe useful aspect of click\'s functional composability is that you can define\nsome number of subcommands functions under a parent command, whichever\nsubcommand the function targets will be invoked.\n\n```python\nimport click\n\n@click.group(\'example\')\ndef example():\n    ...\n\n@example.command("print")\n@click.option(\'--loudly\', is_flag=True)\ndef print_cmd(loudly):\n    if loudly:\n      print("PRINTING!")\n    else:\n      print("printing!")\n\n@example.command("fail")\n@click.option(\'--code\', type: int)\ndef fail_cmd(code):\n    raise click.Exit(code=code)\n\n# Called like:\n# /example.py print\n# /example.py fail\n```\n\nWhereas with argparse, you\'d have had to manually match and call the funcitons\nyourself. This API does all of the hard parts of deciding which function to\ncall.\n\nSimilarly, you can achieve the same thing with cappa.\n\n```python\nfrom __future__ import annotations\nfrom dataclasses import dataclass\nimport cappa\n\n@dataclass\nclass Example:\n    cmd: cappa.Subcommands[Print | Fail]\n\n\ndef print_cmd(print: Print):\n    if print.loudly:\n        print("PRINTING!")\n    else:\n        print("printing!")\n\n@cappa.invoke(invoke=print_cmd)\nclass Print:\n    loudly: bool\n\n@dataclass\nclass Exit:\n    code: int\n\n    def __call__(self):  # again, __call__ is shorthand for the above explicit `invoke=` form.\n        raise cappa.Exit(code=code)\n\ncappa.invoke(Example)\n```\n',
    'author': 'DanCardin',
    'author_email': 'ddcardin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
