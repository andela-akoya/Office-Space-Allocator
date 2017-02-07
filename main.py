"""
Usage:
  create_room <room_type> <room_name>...
  add_person <person_name> <FELLOW | STAFF> [wants_accomodation]
  (-h | --help)
  (-v | --version)

Options:
  -h, --help     Show this screen.
  --version      Show version.
"""
import sys, cmd
from docopt import docopt, DocoptExit


if __name__ == '__main__':
  arguments = docopt(__doc__, version='Office Space Allocator 2.0')

