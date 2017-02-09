from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

class Room():
	
	total_number_of_rooms = 0

	def __init__(self, name):
		self.name = name
		self.capacity_used = 0
		Room.total_number_of_rooms += 1

	def get_total_number_of_rooms():
		return Room.total_number_of_rooms

	def add_person_to_room(type_of_person, wants_accomodation):
		pass

	