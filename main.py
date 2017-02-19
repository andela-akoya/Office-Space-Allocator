"""
Usage:
  main.py create_room <room_type> <room_name>...
  main.py add_person <person_name> <staff/fellow> [<wants_accomodation>]
  main.py print_room <room_name>
  main.py print_allocations [--o=<filename>]
  main.py print_unallocated [--o=<filename>]
  main.py reallocate_person <person_identifier> <new_room_name>
  main.py -h | --help
  main.py -v | --version

Options:
  -h, --help     Show this screen.
  --version      Show version.
"""
import sys
import cmd

from docopt import docopt, DocoptExit

from app.dojo import Dojo
from app.staff import Staff
from app.fellow import Fellow
from app.room import Room
from app.person import Person


def docopt_cmd_decorator(callback):

	def fn(self, arg):
		try:
			opt = docopt(fn.__doc__, arg)

		except DocoptExit as exception:

			print('Command not valid')
			print(exception)
			return

		except SystemExit:
			return

		return callback(self, opt)

	fn.__name__ = callback.__name__
	fn.__doc__ = callback.__doc__
	fn.__dict__.update(callback.__dict__)
	return fn


class MyInteractive(cmd.Cmd):
	"""docstring for MyInteractive"""
	intro = 'Welcome to the Dojo Space Allocator Program!' \
		+ ' (type help for a list of commands.)'
	prompt = ">>> "

	@docopt_cmd_decorator
	def do_create_room(self, arg):
		"""Usage: create_room <room_type> <room_name>..."""
		Dojo.create_room(arg['<room_type>'], arg['<room_name>'])

	@docopt_cmd_decorator
	def do_add_person(self, arg):
		"""Usage: add_person <lastname> <firstname> <staff/fellow> [<wants_accomodation>] """
		Dojo.add_person(arg['<lastname>'], arg['<firstname>'],
						arg['<staff/fellow>'], arg['<wants_accomodation>'])

	@docopt_cmd_decorator
	def do_print_room(self, arg):
		"""Usage: print_room <room_name> """
		Dojo.print_room(arg['<room_name>'])

	@docopt_cmd_decorator
	def do_print_allocations(self, arg):
		"""Usage: print_allocations [--o=<filename>] """
		Dojo.print_allocations(arg['--o'])

	@docopt_cmd_decorator
	def do_print_unallocated(self, arg):
		"""Usage: print_unallocated [--o=<filename>] """
		Dojo.print_unallocated(arg['--o'])

	@docopt_cmd_decorator
	def do_reallocate_person(self, arg):
		"""Usage: reallocate_person <person_identifier> <new_room_name> """
		Dojo.reallocate_person(
			arg['<person_identifier>'], arg['<new_room_name>'].capitalize())

if __name__ == '__main__':

	try:
		MyInteractive().cmdloop()
	except SystemExit:
		pass
	except KeyboardInterrupt:
		pass
