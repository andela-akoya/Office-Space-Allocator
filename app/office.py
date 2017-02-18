import random
from os import sys, path

from app.room import Room
from app.staff import Staff
from app.fellow import Fellow
from app.utilities import Utilities

sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))


class Office(Room):
	"""docstring for Office"""
	office_list = {}

	def __init__(self, name):
		super(Office, self).__init__(name)
		self.type = "office"
		self.maximum_capacity = 4

	def create_office(room_names):
		output = []
		for name in room_names:
			try:
				if (Utilities.check_format_validity([name])
						and not Room.exists(name)):
					new_office = Office(name)
					Office.add_to_office_list(new_office)
					Room.add_room(new_office)
					output.append(new_office)
					print("An Office called {} has been successfully created"
						  .format(name.capitalize()))
				else:
					print("A Room with the name {} already"
						  " exist".format(name.capitalize()))
			except Exception as e:
				print(e)
		return output

	def add_to_office_list(office_instance):
		Office.office_list[office_instance.name] = office_instance

	def exist(office_name):
		if office_name.capitalize() in list(Office.office_list.keys()):
			raise Exception("An Office with the name "
							+ office_name
							+ " already exist")

		return True

	def allocate_office(person):
		office = Office.get_random_office()
		if office:
			person.set_assigned_office(office)
			office.add_room_members(person)
			return("{p.surname} has been allocated the office {o.name}\n"
				   .format(p=person, o=office))
		Staff.add_unallocated_staff(person) if isinstance(person, Staff) \
			else Fellow.add_unallocated_fellow(person, True)
		return(("No available office, {p.surname} has been placed on the"
				+ " office waiting list").format(p=person))

	def get_random_office():
		available_offices = Office.get_available_offices()
		return random.choice(available_offices) \
			if available_offices else None

	def get_available_offices():
		available_offices = []
		for office in Office.get_office_list():
			if not office.is_full:
				available_offices.append(office)
		return available_offices

	def get_office_list():
		return list(Office.office_list.values())
