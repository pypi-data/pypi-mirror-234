#!/usr/bin/env python

'''README
Usage:
  # pip install sleepyemoji
  # pip install --upgrade sleepyemoji

  from sleepyemoji import sleepyemoji
  from sys import argv, exit

  sleepyemoji(argv[1:])
  exit(0)

Adding Emojis:
  1. New category? Update toolchain/commands.py
  2. Append lists in toolchain/emojis.py
  3. Update pypi package
  4. Update repository
'''

# stdlib
from typing import List
from sys import exit, argv
# custom modules
from toolchain.commands import emoji_logic
# 3rd party
try:
  import typer
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


def sleepyemoji(categories:List[str]) -> str:
  app = typer.Typer()
  @app.command()
  def emoji(categories:List[str]) -> str:
    '''Another example command

    Prints emojis with some metadata, organized by category.

    ───Params\n
    categories:List[str] :: emoji categories to include (casing ignored)

    ───Categories\n
      animals, a\n
      faces, f\n
      hands, h\n
      icons, i\n
      people, p\n
      combos, combinations\n
      all\n

    ───Example\n
      ./sleepyemoji.py a f h

    ───Return\n
    str :: prettytable string
    '''
    return emoji_logic(categories)
  if (__name__ == "sleepyemoji") or (__name__ == '__main__'):
    app()


## Local Testing
# sleepyemoji(argv)
