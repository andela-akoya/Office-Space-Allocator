import re
from datetime import datetime
from os import path, sys

from app.customfile import Customfile
from app.database import Database
from app.errors import WrongFormatException
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.person import Person
from app.room import Room
from app.staff import Staff
from app.utilities import Utilities


class Dojo(object):
	"""The class holds all the properties and methods of a Dojo model"""

	@classmethod
	def create_room(cls, room_type, room_names):
		""" This method creates a particular type of room or rooms
		based on the room_type and room name(s) passed as arguments """

		type_of_room = room_type.strip().lower()
		if type_of_room == "office":
			return Office.create_office(room_names)
		elif type_of_room == "livingspace":
			return LivingSpace.create_livingspace(room_names)
		else:
			print("Invalid type of room")

	@classmethod
	def get_total_rooms(cls):
		""" this method returns the total number of rooms that has been
		created """

		return Room.get_total_number_of_rooms()

	@classmethod
	def add_person(cls, surname, firstname, category, wants_accomodation=None,
				   person_id=None):
		""" this method creates a person object and assigns a room to the
		person  """

		type_of_person = category.strip().lower()
		try:
			if type_of_person == "staff":
				new_staff = Staff(person_id, surname, firstname)
				if new_staff:
					print(("Staff {ns.surname} {ns.firstname} with id "
						   + "{ns.uniqueId} has been successfully added.")
						  .format(ns=new_staff))
					Staff.add_to_staff_list(new_staff)
					Person.add_to_person_list(new_staff)
					cls.allocate_room(new_staff)

			elif type_of_person == "fellow":
				new_fellow = Fellow(person_id, surname, firstname, True) \
					if wants_accomodation in ['y', 'Y'] \
					else Fellow(person_id, surname, firstname)
				if new_fellow:
					print(("Fellow {nf.surname} {nf.firstname} with id "
						   + "{nf.uniqueId} has been successfully added.")
						  .format(nf=new_fellow))
					Fellow.add_to_fellow_list(new_fellow)
					Person.add_to_person_list(new_fellow)
					cls.allocate_room(new_fellow, wants_accomodation)
			else:
				print("Invalid type of person")

		except WrongFormatException as e:
			print(e)

	@classmethod
	def allocate_room(cls, person, wants_accomodation=None):
		""" This method allocates a room to a person based on the
		person's category """

		if(not(wants_accomodation in ['y', 'Y'])):
			print(Office.allocate_office(person))
		else:
			print("{}{}".format(Office.allocate_office(person),
								LivingSpace.allocate_livingspace(person)))

	@classmethod
	def print_room(cls, room_name):
		""" This method prints the information of the members of a particular
		room based on the room name passed as arguments """

		print("\n{}".format(Room.print_room_members(room_name)))

	@classmethod
	def print_allocations(cls, filename, append_flag=False, override_flag=False):
		""" This method prints all the allocations that has been made onto
		the console or to a file if a file name is passed as argument """

		allocations = Room.get_allocations()
		if filename is None:
			print(allocations)
		else:
			try:
				new_file = Customfile.create_file(filename, append_flag,
												  override_flag)
				Customfile.write(new_file, allocations)
			except FileExistsError as e:
				print(e)
			except WrongFormatException as e:
				print(e)

	@classmethod
	def print_unallocated(cls, filename, append_flag=False, override_flag=False):
		""" This method prints all the unallocated staff and fellow onto
		the console or to a file if a file name is passed as argument """

		unallocated = Person \
			.get_unallocated(Staff.get_unallocated_staff(),
							 Fellow.get_unallocated_fellows())
		if not filename:
			print(unallocated)
		else:
			try:
				new_file = Customfile.create_file(filename, append_flag,
												  override_flag)
				Customfile.write(new_file, unallocated)
			except FileExistsError as e:
				print(e)

	@classmethod
	def reallocate_person(cls, identifier, room_name):
		""" This method reallocates a person to another room based on the
		room name passed in as argument """

		try:
			person_id = int(identifier)
			if Person.exist(person_id):
				person, = [person for person in Person.get_list_of_persons()
						   if person.uniqueId == person_id]
				if Room.exists(room_name):
					room, = [room for room in Room.get_room_list()
							 if room.name == room_name.capitalize()]
					if len(room.room_members) != room.maximum_capacity:
						if not (person in room.room_members):
							if isinstance(person, Staff):
								if room.room_type == "office":
									Office.reallocate_person(person, room_name)
								else:
									print(("Room {} is a livingspace and "
										   + "can't be assigned to a staff")
										  .format(room_name))
							else:
								if room.room_type == "office":
									Office.reallocate_person(person, room_name)
								else:
									LivingSpace.reallocate_person(person,
																  room_name)
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

			else:
				print("Person with the id {} doesn't exist".format(person_id))
		except ValueError:
			print("Wrong id format. id must be a number")

	@classmethod
	def load_people(cls, filename):
		""" This method load a list of persons from a text file and
		adds them to the system """

		error_messages = [
			"Errors\n---------",
			"The following people couldn't be loaded"
			+ " because of incomplete information\n"
		]
		try:
			file_to_be_loaded = Customfile.open_file(filename)
			with file_to_be_loaded as data_file:
				for entry in data_file:
					data = entry.strip().split(" ")
					if len(data) > 2:
						surname, firstname, category = data[0:3]
						wants_accomodation = data[3] \
							if len(data) > 3 else None
						cls.add_person(surname, firstname,
									   category, wants_accomodation)
					else:
						error_messages.append(" ".join(data))
				if len(error_messages) > 2:
					print("\n".join(error_messages))
				data_file.close()

		except FileNotFoundError as e:
			print(e)

	@classmethod
	def load_rooms(cls, filename):
		""" This method loads rooms from a text file and adds them into the
		system """
		error_messages = [
			"Errors\n---------",
			"The following rooms couldn't be loaded"
			+ " because of incomplete information\n"
		]
		try:
			file_to_be_loaded = Customfile.open_file(filename)
			with file_to_be_loaded as data_file:
				for entry in data_file:
					data = entry.strip().split(" ")
					if len(data) > 1:
						room_type = data[0]
						room_names = data[1:]
						cls.create_room(room_type, room_names)
					else:
						error_messages.append(" ".join(data))
				if len(error_messages) > 2:
					print("\n".join(error_messages))
				data_file.close()

		except FileNotFoundError as e:
			print(e)

	@classmethod
	def save_state(cls, db_name):
		""" this method saves the current state of the system (i.e persist the
		generated data in the system into a database). """

		database_path = path.dirname(path.abspath(__file__)) \
			+ "/data/database/"
		database_name = db_name or \
			("-").join(re.findall(r"[\w']+",
								  str(datetime.now()).split(".")[0]))

		if not Customfile.exist(database_path, database_name + ".db"):
			new_database = Database(database_path + database_name + ".db")
			new_database.save(
				Room.export_in_database_format(),
				Person.export_in_database_format()
			)
		else:
			error = "Database with the name {} already exist. "\
					+ "You can either specify another name or override the " \
					+ "existing database.\n"\
					+ "To override specify the [override] command "
			print(error.format(database_name + ".db"))

	@classmethod
	def load_state(cls, database_name):
		""" This method load a state from the database and set the system to
		that state """

		database_path = path.dirname(path.abspath(__file__)) \
			+ "/data/database/"
		if database_name:
			if Customfile.exist(database_path, database_name + ".db"):
				cls.reset_state()
				new_database = Database(database_path + database_name + ".db")
				new_database.load()
			else:
				error = "Database with the name {} does not exist."\
						.format(database_name + ".db")
				print(error)

	@classmethod
	def rename_room(cls, old_room_name, new_room_name):
		""" This method changes the name of an existing room into a new
		one based on the new_room_name passed in as argument """

		if Room.exists(old_room_name):
			if not Room.exists(new_room_name):
				Room.get_a_particular_room(old_room_name).name = new_room_name
				print("Room {} has been suceessfully renamed to {}"
					  .format(old_room_name, new_room_name))
			else:
				print("Room {} already exist. Please choose another name"
					  .format(new_room_name))
		else:
			print(("Room {} doesn't exist, therefore changes couldn't be "
				   + "made.").format(old_room_name))

	@classmethod
	def reset_state(cls):
		""" clears the current state of the app, deleting
		all generated data """
		LivingSpace.reset()
		Office.reset()
		Room.reset()
		Staff.reset()
		Fellow.reset()
		Person.reset()
