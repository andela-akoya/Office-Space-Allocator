import random
from os import sys, path

from app.room import Room
from app.staff import Staff
from app.fellow import Fellow
from app.utilities import Utilities
from app.errors import WrongFormatException


class Office(Room):
	"""docstring for Office"""
	office_list = {}

	def __init__(self, name):
		super(Office, self).__init__(name)
		self.__category = "office"
		self.__maximum_capacity = 6

	@property
	def category(self):
		return self.__category

	@category.setter
	def category(self, new_type):
		self.__category = new_type

	@property
	def maximum_capacity(self):
		return self.__maximum_capacity

	@maximum_capacity.setter
	def maximum_capacity(self, new_capacity):
		self.__maximum_capacity = new_capacity

	@classmethod
	def create_office(cls, room_names):
		output = []
		for name in room_names:
			try:
				Utilities.check_format_validity([name])
				if not Room.exists(name):
					new_office = Office(name)
					cls.add_to_office_list(new_office)
					Room.add_room(new_office)
					output.append(new_office)
					print("An Office called {} has been successfully created"
						  .format(name.capitalize()))
				else:
					print("A Room with the name {} already exist"
						  .format(name.capitalize()))
			except WrongFormatException as e:
				print("' is not a valid office name format")
		return output

	@classmethod
	def add_to_office_list(cls, office_instance):
		cls.office_list[office_instance.name] = office_instance

	@classmethod
	def allocate_office(cls, person, office_name=None):
		office = Room.get_a_particular_room(office_name) \
			if office_name else cls.get_random_office()
		if office:
			person.set_assigned_office(office)
			office.add_room_members(person)
			return("{p.surname} has been allocated the office {o.name}\n"
				   .format(p=person, o=office))
		Staff.add_unallocated_staff(person) if isinstance(person, Staff) \
			else Fellow.add_unallocated_fellow(person, True)
		return(("No available office, {p.surname} has been placed on the"
				+ " office waiting list\n").format(p=person))

	@classmethod
	def get_random_office(cls):
		available_offices = cls.get_available_offices()
		return random.choice(available_offices) \
			if available_offices else None

	@classmethod
	def get_available_offices(cls):
		available_offices = []
		for office in cls.get_office_list():
			if not office.is_full:
				available_offices.append(office)
		return available_offices

	@classmethod
	def get_office_list(cls):
		return list(cls.office_list.values())

	@classmethod
	def get_office(cls, office_name):
		return cls.office_list[office_name]

	@classmethod
	def reallocate_person(cls, person, office_name):
		office = cls.get_office(office_name)
		message = "{p.category} {p.surname} {p.firstname} has been " \
			+ "successfully reallocated to {} {}"

		if person.get_assigned_office() is None:
			Staff.remove_from_unallocated_staff_list(
				person)
		else:
			person.get_assigned_office() \
				.remove_member(person)
		person.set_assigned_office(office)
		office.add_room_members(person)
		print(message.format(office_name, "office", p=person))
