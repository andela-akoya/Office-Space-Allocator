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
from app.errors import WrongFormatException


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
		type_of_person = arg['<staff/fellow>'].strip().lower()
		try:
			if type_of_person == "staff":
				new_staff = Staff(arg['<lastname>'], arg['<firstname>'])
				if new_staff:
					print(("Staff {ns.surname} {ns.firstname} has been"
						   + " successfully added").format(ns=new_staff))
					Staff.add_to_staff_list(new_staff)
					Person.add_to_map(new_staff)
					Dojo.allocate_room(new_staff)

			elif type_of_person == "fellow":
				new_fellow = Fellow(arg['<lastname>'], arg['<firstname>'])
				if new_fellow:
					print(("Fellow {nf.surname} {nf.firstname} has been"
						   + " successfully added").format(nf=new_fellow))
					Fellow.add_to_fellow_list(new_fellow)
					Person.add_to_map(new_fellow)
					Dojo.allocate_room(new_fellow, arg['<wants_accomodation>'])
			else:
				print("Invalid type of person")

		except WrongFormatException as e:
			print(e)

	@docopt_cmd_decorator
	def do_print_room(self, arg):
		"""Usage: print_room <room_name> """
		Dojo.print_room(arg['<room_name>'])

	@docopt_cmd_decorator
	def do_print_allocations(self, arg):
		"""Usage: print_allocations [--o=<filename>] """
		try:
			Dojo.print_allocations(arg['--o'])
		except Exception as e:
			print(e)

	@docopt_cmd_decorator
	def do_print_unallocated(self, arg):
		"""Usage: print_unallocated [--o=<filename>] """
		Dojo.print_unallocated(arg['--o'])

	@docopt_cmd_decorator
	def do_reallocate_person(self, arg):
		"""Usage: reallocate_person <person_identifier> <new_room_name> """
		try:
			Dojo.reallocate_person(
				arg['<person_identifier>'], arg['<new_room_name>'])
		except Exception as e:
			print(e)


if __name__ == '__main__':

	try:
		MyInteractive().cmdloop()
	except SystemExit:
		pass
	except KeyboardInterrupt:
		pass
