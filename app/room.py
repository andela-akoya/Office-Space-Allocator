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

	def remove_member(self, person):
		self.room_members.remove(person)

	@classmethod
	def add_room(cls, room):
		cls.room_list[room.name] = room

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
	def get_room_list(cls):
		return cls.room_list

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

	@classmethod
	def reallocate_person(cls, person, room_name):
		message = "{p.category} {p.surname} {p.firstname} has been " \
			+ "successfully reallocated to {} {}"
		if Room.exists(room_name):
			room = cls.get_room_list()[room_name]
			if not room.is_full:
				if not (person in room.get_room_members()):
					if isinstance(person, Staff):
						if room.get_type() == "office":
							if person.get_assigned_office() is None:
								Staff.remove_from_unallocated_staff_list(
									person)
							else:
								person.get_assigned_office() \
									.remove_member(person)
							person.set_assigned_office(room)
							room.add_room_members(person)
							print(message.format(room_name, "office", p=person))
						else:
							print(("Room {} is a livingspace and can't be "
								   + "assigned to a staff").format(room_name))
					else:
						if room.get_type() == "office":
							if person.get_assigned_office() is None:
								Fellow.remove_from_unallocated_fellow_list(
									person, "office")
							else:
								person.get_assigned_office() \
									.remove_member(person)
							person.set_assigned_office(room)
							room.add_room_members(person)
							print(message.format(room_name, "office", p=person))
						else:
							if person.get_wants_accomodation():
								if person.get_assigned_livingspace() is None:
									Fellow.remove_from_unallocated_fellow_list(
										person, "livingspace")
								else:
									person.get_assigned_livingspace() \
										.remove_member(person)
								person.set_assigned_livingspace(room)
								room.add_room_members(person)
								print(message
									  .format(room_name, "livingspace", p=person))
							else:
								cls
								print(("Fellow {p.surname} "
									   + "{p.firstname} never "
									   + "registered for accomodation "
									   + "so can't be reallocated to a "
									   + "a livingspace")
									  .format(p=person))
				else:
					print(("{p.surname} {p.firstname} already belongs "
						   + "to room {}, therefore can't be "
						   + "reallocated to the same room")
						  .format(room_name, p=person))
			else:
				print("Room {} is filled up, please input another room"
					  .format(room_name))
		else:
			print("Room {} doesn't exist".format(room_name))
