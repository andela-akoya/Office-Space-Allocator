"""
Usage:
  main.py create_room <room_type> <room_name>...
  main.py add_person <person_name> <staff/fellow> [<wants_accomodation>]
  main.py -h | --help
  main.py -v | --version

Options:
  -h, --help     Show this screen.
  --version      Show version.
"""
import sys, cmd
from docopt import docopt, DocoptExit
from app.dojo import Dojo
from app.staff import Staff
from app.fellow import Fellow
from app.room import Room


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
		pass

	@docopt_cmd_decorator
	def do_add_person(self, arg):
		"""Usage: add_person <lastname> <firstname> <staff/fellow> [<wants_accomodation>] """
		pass
		

if __name__ == '__main__':

	try:
		MyInteractive().cmdloop()
	except SystemExit:
		pass
	except KeyboardInterrupt:
		pass
        
 
