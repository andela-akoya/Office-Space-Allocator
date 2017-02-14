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

	def add_person(person_instance, wants_accomodation = None):
		try:
			if wants_accomodation == None :
				print (Room.allocate_room(person_instance, \
										list(Office.office_list.values())))
			else:
				if wants_accomodation.strip().lower() == "y":
					print (Room.allocate_room(person_instance, \
												list(Office.office_list.values()), \
												list(LivingSpace.livingspace_list
													.values())))
				else:
					print (Room.allocate_room(person_instance, \
												 list(Office.office_list.values())))
		except Exception as e:
			print (e)

	def print_room(room_name):
		try:
			print()
			print (Room.print_room_members(room_name))	
		except Exception as e:
			print (e)

	def print_allocations(filename):
		allocations = Room.get_allocations()
		if filename is None:
			print(allocations)
		else:
			try:
				file = File.create_file(filename)
				File.write(file, allocations)

			except Exception as e:
				print(e)
