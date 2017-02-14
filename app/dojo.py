from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.office import Office
from app.livingspace import LivingSpace
from app.room import Room
from app.utilities import Utilities
from app.staff import Staff
from app.fellow import Fellow
from app.file import File
from app.person import Person

class Dojo(object):
	"""docstring for Dojo"""
	def __init__(self):
		pass


	def create_room(room_type, room_names):
		type_of_room = room_type.strip().lower()
		output = []

		if type_of_room == "office":
			for name in room_names:
				try:
					if (Utilities.check_format_validity([name]) \
							and not Room.exists(name.capitalize())):
						new_office = Office(name.capitalize())
						output.append(new_office)
						Office.add_to_office_list(new_office)
						Room.add_room(new_office)
						print ("An Office called " \
								+ name + " has been successfully created!")
					else:
						print("A Room with the name {} already exist" \
								.format(name))

					
				except Exception as e:
					print (e)
								
		elif type_of_room == "livingspace":
			for name in  room_names:
				try:
					if (Utilities.check_format_validity([name]) \
							 and not Room.exists(name.capitalize())):
						new_livingspace = LivingSpace(name.capitalize())
						output.append(new_livingspace)
						LivingSpace.add_to_livingspace_list(new_livingspace)
						Room.add_room(new_livingspace)
						print ("A LivingSpace called "  \
								+ name + " has been successfully created!" )	
					else:
						print("A Room with the name {} already exist" \
								.format(name))

				except Exception as e:
					print (e)
		else:
			print ("Invalid type of room")
		
		return output