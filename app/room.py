import random
from os import sys, path

from app.fellow import Fellow
from app.staff import Staff
from app.person import Person

sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))


class Room():

	total_number_of_rooms = 0
	room_list = {}

	def __init__(self, room_name):
		self.name = room_name.capitalize()
		self.is_full = False
		self.room_members = []
		Room.total_number_of_rooms += 1

	def get_room_name(self):
		return self.name

	def set_room_name(self, new_room_name):
		self.name = new_room_name.capitalize()

	def add_room_members(self, person):
		self.room_members.append(person)
		if len(self.room_members) == self.maximum_capacity:
			self.is_full = True

	def get_room_members(self):
		return self.room_members

	@classmethod
	def add_room(cls, room):
		cls.room_list[room.name] = room
		print(room.room_list)

	@classmethod
	def get_random_room(cls, room_list):
		available_rooms = cls.get_available_rooms(room_list)
		if available_rooms:
			return random.choice(available_rooms)

		return False

	@classmethod
	def get_available_rooms(cls, room_list):
		available_rooms = []
		for room in room_list:
			if not room.is_full:
				available_rooms.append(room)

		return available_rooms

	@classmethod
	def print_room_members(cls, room_name):
		output = []
		name = room_name.capitalize()
		if name in list(cls.room_list.keys()):
			output.append("{:15} {}".format("Surname", "Firstname"))
			for member in cls.room_list[name].room_members:
				output.append("{:15} {} "
							  .format(member.surname, member.firstname))

			return "\n".join(output)

		return("The room with the name {} does not exist".format(room_name))

	@classmethod
	def get_total_number_of_rooms(cls):
		return cls.total_number_of_rooms

	def get_capacity_used(self):
		return self.capacity_used

	@classmethod
	def exists(cls, room_name):
		if room_name.capitalize() in list(cls.room_list.keys()):
			return True

		return False

	@classmethod
	def get_allocations(cls):
		output = ""
		for room in list(cls.room_list.values()):
			output += "{} Room\n".format(room.name)
			output += (len(room.name + " Room") * "-") + "\n"
			for member in room.room_members:
				output += "{m.surname} {m.firstname}, ".format(m=member)
			output += "\n\n\n"

		return output

	def reallocate_person(identifier, room_name):
		if Person.exist(identifier):
			if Room.exists(room_name):
				person = Person.id_map[identifier]
				room = Room.room_list[room_name]
				if isinstance(person, Staff):
					if isinstance(room, Office):
						if not room.is_full:
							present_office = person.get_assigned_office()
							if present_office is None:
								Staff.remove_from_unallocated_staff_list(
									person)
							else:
								present_office.get_room_members() \
									.remove(person)
							person.set_assigned_office(room)
							room.add_room_members(person)
						else:
							raise Exception(("{r.name} is filled up and "
											 + "can't accept any more member ")
											.format(r=room))
					else:
						raise Exception(("{r.name} is a livingspace and "
										 + " can't be assigned to a Staff")
										.format(r=room))
				else:
					if not room.is_full:
						if isinstance(room, Office):
							present_office = person.get_assigned_office()
							if present_office is None:
								Fellow.remove_from_unallocated_fellow_list(
									person, "office")
							else:
								present_office.get_room_members() \
									.remove(person)

							person.set_assigned_office(room)
							room.add_room_members(person)
						else:
							if person.get_wants_accomodation():
								livingspace =  person \
									.get_assigned_livingspace()
								if Livingspace is None:
									Fellow.remove_from_unallocated_fellow_list(
										person, "livingspace")
								else:
									livingspace.get_room_members() \
										.remove(person)

								person.set_assigned_livingspace(room)
								room.add_room_members(person)

							else:
								raise Exception(("Fellow {p.suraname} "
												 + "{p.firstname} never "
												 + "registered for accomodation"
												 + "so can't be granted a "
												 + "a livingspace")
												.format(p=person))
					else:
						raise Exception(("{r.name} is filled up and "
										 + "can't accept any more member ")
										.format(r=room))

			else:
				raise Exception("Room doesn't exist")
		else:
			raise Exception("Person doesn't exist")
