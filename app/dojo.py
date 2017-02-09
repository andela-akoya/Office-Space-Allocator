from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.office import Office
from app.livingspace import LivingSpace
from app.room import Room

class Dojo(object):
	"""docstring for Dojo"""
	def __init__(self):
		pass


	def create_room(room_type, room_names):
		type_of_room = room_type.strip().lower()
		output = []

		if type_of_room == "office":
			for room in room_names:
				if not room.strip() in ["\"\"", "\"", "'", "''", ".", "-","?", "_", ","]:
					new_office = Office(room)
					output.append(new_office)
					Office.add_to_office_list(new_office)
					print ("An Office called " + room + " has been successfully created!")
				else:
					print ("Invalid name format")
		elif type_of_room == "livingspace":
			for room in  room_names:
				if not room.strip() in ["\"\"", "\"", "'", "''", ".", "-","?", "_", ","]:
					new_livingspace = LivingSpace(room)
					output.append(new_livingspace)
					LivingSpace.add_to_livingspace_list(new_livingspace)
					print ("A LivingSpace called " + room + " has been successfully created!" )	
				else:
					print ("Invalid name format")
		else:
			print ("Invalid type of room")
		
		return output
		

	def delete_room(room_type, room_name):
		pass

	def get_total_rooms():
		return 1