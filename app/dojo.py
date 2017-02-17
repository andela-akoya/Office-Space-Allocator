from os import sys, path
sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))
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
		if type_of_room == "office":
			return Office.create_office(room_names)
		elif type_of_room == "livingspace":
			return LivingSpace.create_livingspace(room_names)
		else:
			print("Invalid type of room")

	def allocate_room(person, wants_accomodation=None):
		try:
			if((wants_accomodation is None) or (wants_accomodation.lower() != "y")):
				print(Office.allocate_office(person))
			else:
				print(Office.allocate_office(person),
					  LivingSpace.allocate_livingspace(person))
		except Exception as e:
			pass

	def print_room(room_name):
		try:
			print("\n", Room.print_room_members(room_name))
		except Exception as e:
			print(e)

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

	def print_unallocated(filename):
		unallocated = Person.get_unallocated(Staff.get_unallocated_staff(),
											 Fellow.get_unallocated_fellows())
		if filename is None:
			print(unallocated)
		else:
			try:
				file = File.create_file(filename)
				File.write(file, unallocated)

			except Exception as e:
				print(e)

	def reallocate_person(identifier, new_room_name):
		person_id = None
		try:
			person_id = int(identifier)
		except Exception:
			print("Wrong id format")
			return None

		try:
			Room.reallocate_room(person_id, new_room_name.capitalize())
		except Exception as e:
			print(e)

	def get_total_rooms():
		return Room.get_total_number_of_rooms()
