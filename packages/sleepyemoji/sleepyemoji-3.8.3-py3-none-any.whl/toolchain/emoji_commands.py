# stdlib
from typing import List
from sys import exit
# custom
from toolchain.emojis import *
# 3rd party
try:
  from prettytable import PrettyTable
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


#───Commands─────────────────
def emoji_logic(categories:List[str]) -> str:
  '''adds categories to output table provided in input array'''

  cats = [i.lower() for i in categories]
  res  = PrettyTable()

  res.field_names = [
    "Emoji", "Discord Value", "iOS Descriptor"
  ]

  if ('animals' in cats) or ('a' in cats) or ('all' in cats):
    res.add_rows(animals)
  if ('faces' in cats) or ('f' in cats) or ('all' in cats):
    res.add_rows(faces)
  if ('hands' in  cats) or ('h' in cats) or ('all' in cats):
    res.add_rows(hands)
  if ('icons' in cats) or ('i' in cats) or ('all' in cats):
    res.add_rows(icons)
  if ('people' in cats) or ('p' in cats) or ('all' in cats):
    res.add_rows(people)
  if ('combos' in cats) or ('combinations' in cats) or ('all' in cats):
    res.add_rows(combos)

  print(res)
  return res
