import cmd
import os
import platform
import sys

from app.dojo import Dojo
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.person import Person
from app.room import Room
from app.staff import Staff
from docopt import DocoptExit, docopt


def docopt_cmd(callback):

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
	"""The class holds the methods for an interractive console"""
	intro = 'Welcome to the Dojo Space Allocator Program!' \
			+ ' (type help for a list of commands.)'
	prompt = ">>> "

	@docopt_cmd
	def do_create_room(self, arg):
		"""Usage: create_room <room_type> <room_name>..."""
		Dojo.create_room(arg['<room_type>'], arg['<room_name>'])

	@docopt_cmd
	def do_add_person(self, arg):
		"""Usage: add_person <lastname> <firstname> <staff/fellow> [<wants_accomodation>] """
		Dojo.add_person(arg['<lastname>'], arg['<firstname>'],
						arg['<staff/fellow>'], arg['<wants_accomodation>'])

	@docopt_cmd
	def do_print_room(self, arg):
		"""Usage: print_room <room_name> """
		Dojo.print_room(arg['<room_name>'])

	@docopt_cmd
	def do_print_allocations(self, arg):
		"""Usage: print_allocations [(--o=<filename> [override|append])] """
		Dojo.print_allocations(arg['--o'], arg['append'], arg['override'])

	@docopt_cmd
	def do_print_unallocated(self, arg):
		"""Usage: print_unallocated [(--o=<filename> [override|append])] """
		Dojo.print_unallocated(arg['--o'], arg['append'], arg['override'])

	@docopt_cmd
	def do_reallocate_person(self, arg):
		"""Usage: reallocate_person <person_identifier> <new_room_name> """
		Dojo.reallocate_person(
			arg['<person_identifier>'], arg['<new_room_name>'])

	@docopt_cmd
	def do_load_people(self, arg):
		"""Usage: load_people <filename> """
		Dojo.load_people(arg['<filename>'])

	@docopt_cmd
	def do_load_rooms(self, arg):
		"""Usage: load_rooms <filename> """
		Dojo.load_rooms(arg['<filename>'])

	@docopt_cmd
	def do_save_state(self, arg):
		"""Usage: save_state [--db=<sqlite_database>] [override] """
		Dojo.save_state(arg['--db'])

	@docopt_cmd
	def do_load_state(self, arg):
		"""Usage: load_state <sqlite_database> """
		Dojo.load_state(arg['<sqlite_database>'])

	@docopt_cmd
	def do_rename_room(self, arg):
		"""Usage: rename_room <old_room_name> <new_room_name>"""
		Dojo.rename_room(arg['<old_room_name>'], arg['<new_room_name>'])

	@docopt_cmd
	def do_clear(self, arg):
		"""Usage: clear"""
		os.system("cls") if platform.system().lower() == "windows" \
			else os.system("tput reset")

	@docopt_cmd
	def do_reset_state(self, arg):
		"""Usage: reset_state"""
		Dojo.reset_state()

	def do_quit(self, arg):
		"""Usage: quit"""
		print("********** Good Bye **********")
		exit()


if __name__ == '__main__':
	MyInteractive().cmdloop()
