import random
from os import path, sys

from app.fellow import Fellow
from app.person import Person
from app.staff import Staff


class Room():
	""" This class hold all properties and methods of a Room model """

	list_of_rooms = []  # holds all the rooms created

	def __init__(self, room_name):
		self.__name = room_name.capitalize()
		self.__room_members = []

	@property
	def name(self):
		""" This method returns the name property value"""
		return self.__name

	@name.setter
	def name(self, new_room_name):
		""" This method sets the name property value """
		if new_room_name and isinstance(new_room_name, str):
			self.__name = new_room_name.capitalize()
		else:
			raise ValueError("Room name must be a string and can't be empty")

	@property
	def room_members(self):
		""" This method returns the room members property value"""
		return self.__room_members

	@room_members.setter
	def room_members(self, person):
		""" Thhis method sets the room member property """
		if not isinstance(person, Person):
			raise ValueError(
				"Only a person, staff, or fellow instance can be added")
		self.__room_members.append(person)

	def remove_member(self, person):
		""" this method removes a member from a room member list """
		if not isinstance(person, Person):
			raise ValueError(
				"Only a person, staff, or fellow instance can be removed")
		self.__room_members.remove(person)

	@classmethod
	def add_room(cls, room):
		""" Adds a room  to the list of rooms """
		if not isinstance(room, Room):
			raise ValueError(
				"Only a room, office, or livingspace instance can be added")
		cls.list_of_rooms.append(room)

	@classmethod
	def get_random_room(cls, room_list):
		""" this method gets a random room from a list of
		available rooms """
		available_rooms = cls.get_available_rooms(room_list)
		return random.choice(available_rooms) if available_rooms else False

	@classmethod
	def get_available_rooms(cls, room_list):
		""" this method gets rooms that can still accomodate from
		the list of all rooms """
		return [room for room in room_list
				if len(room.room_members) != room.maximum_capacity] \
			if room_list else []

	@classmethod
	def print_room_members(cls, room_name):
		""" this method returns a well formattted data of all the
		members of a particular room """
		output = []
		name = room_name.capitalize()
		if name in [room.name for room in cls.list_of_rooms]:
			output.append("{:4} {:15} {:15} {}"
						  .format("ID", "Surname", "Firstname", "Category"))
			for member in [room.room_members for room in cls.list_of_rooms
						   if room.name == name][0]:
				output.append("{:4} {:15} {:15} {}"
							  .format(member.uniqueId, member.surname,
									  member.firstname, member.category))

			return "\n".join(output)

		return("The room with the name {} does not exist".format(room_name))

	@classmethod
	def get_total_number_of_rooms(cls):
		""" returns the total number of rooms created """
		return len(cls.list_of_rooms)

	@classmethod
	def exists(cls, room_name):
		""" this methods checks whether a room exists or has been created """
		return room_name.capitalize() in [room.name for room in cls.list_of_rooms]

	@classmethod
	def get_room_list(cls):
		""" this method returns the list of rooms """
		return cls.list_of_rooms

	@classmethod
	def get_allocations(cls):
		""" this method returns all the rooms that have been allocated and
		also its occupants """
		output = ""
		for room in cls.list_of_rooms:
			if room.room_members:
				output += "{} Room ({})\n".format(room.name, room.room_type)
				output += (len(room.name + " Room " +
							   str(room.room_type)) * "-") + "\n"
				for member in room.room_members:
					output += "{m.surname} {m.firstname}, ".format(m=member)
				output += "\n\n"

		return output

	@classmethod
	def export_in_database_format(cls):
		""" this method exports all rooms data in a format that is
		importable to a database """
		return [(room.name, room.room_type) for room in cls.list_of_rooms]

	@classmethod
	def get_a_particular_room(cls, room_name):
		""" this method returns a particular room from the list of
		rooms based on the room name provided as argument """
		output = [room for room in cls.list_of_rooms if room.name ==
				  room_name.capitalize()]
		return output[0] if output \
			else "Room {} doesn't exist".format(room_name)

	@classmethod
	def reset(cls):
		""" erases the room list """
		cls.list_of_rooms = []
