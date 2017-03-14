from os import path, sys

from app.errors import WrongFormatException
from app.utilities import Utilities


class Person():
	"""
	The class is the base class for both fellow and staff class
	"""

	list_of_persons = []

	def __init__(self, person_id, lname, fname):
		try:
			Utilities.check_format_validity([lname, fname])
		except WrongFormatException:
			raise WrongFormatException(
				"Firstname or Lastname is not a valid name format")

		self.__uniqueId = person_id or Utilities.generate_person_id(
			Person.get_id_list())
		self.__surname = lname.capitalize()
		self.__firstname = fname.capitalize()
		self.__office = None

	@property
	def uniqueId(self):
		# This method returns the value of the person unique id property
		return self.__uniqueId

	@uniqueId.setter
	def uniqueId(self, new_id):
		# This method sets the value of the unique id property
		if isinstance(new_id, int):
			self.__uniqueId = new_id
		else:
			raise ValueError("Only integers are acceptable format")

	@property
	def surname(self):
		# Returns thevalue of the surname property
		return self.__surname

	@surname.setter
	def surname(self, new_surname):
		# Sets the value of the surname property
		self.__surname = new_surname.capitalize()

	@property
	def firstname(self):
		# Returns the value of the firstname property
		return self.__firstname

	@firstname.setter
	def firstname(self, new_firstname):
		# sets the value of the firstname property
		self.__firstname = new_firstname.capitalize()

	@property
	def office(self):
		# returns the value of the office property
		return self.__office

	@office.setter
	def office(self, office):
		# sets the value of the office property
		self.__office = office

	@property
	def livingspace(self):
		# returns none value for livingspace property by default
		return None

	@property
	def wants_accomodation(self):
		# returns false value for the wants_accomodation property by default
		return False

	@classmethod
	def get_unallocated(cls,unallocated_staff_list,unallocated_fellow_list):
		# this method returns the unallocated persons both in the staff and
		# fellow category
		output = ["Unallocated List \n---------------------\n"]
		serial_no = 0
		for staff in unallocated_staff_list:
			serial_no += 1
			output.append(("{}. Staff {s.surname} {s.firstname} ({s.uniqueId})\n")
						  .format(serial_no, s=staff))

		for fellow in unallocated_fellow_list["office"]:
			serial_no += 1
			if fellow in unallocated_fellow_list["livingspace"]:
				output.append(("{}. Fellow {f.surname} {f.firstname} ({f.uniqueId})"
							   + " (Office $ Livingspace)\n")
							  .format(serial_no, f=fellow))
			else:
				output.append(("{}. Fellow {f.surname} {f.firstname} ({f.uniqueId})"
							   + " (Office)\n").format(serial_no, f=fellow))

		for fellow in unallocated_fellow_list["livingspace"]:

			if not fellow in unallocated_fellow_list["office"]:
				serial_no += 1
				output.append(("{}. Fellow {f.surname} {f.firstname} "
							   + "(Livingspace)\n").format(serial_no,
														   f=fellow))

		return "\n".join(output)

	@classmethod
	def add_to_person_list(cls, person):
		# this method adds a person object to the list of persons
		cls.list_of_persons.append(person)

	@classmethod
	def get_id_list(cls):
		# returns all the persons unique id that has been generated.
		return [person.uniqueId for person in cls.list_of_persons]

	@classmethod
	def get_list_of_persons(cls):
		# returns a list of all the persons that has been created
		return cls.list_of_persons

	@classmethod
	def exist(cls, person_identifier):
		# checks if a person exists using the person's identifier
		# passed in as argument
		return person_identifier in [person.uniqueId
									 for person in cls.list_of_persons]

	@classmethod
	def export_in_database_format(cls):
		# this method exports all persons data in a format that is
		# importable to a database
		output = []
		for person in cls.list_of_persons:
			office = "None" if not person.office else person.office.name
			livingspace = "None" if not person.livingspace \
				else person.livingspace.name
			output.append(
				(person.uniqueId, person.surname, person.firstname,
				 person.category, office, livingspace,
				 person.wants_accomodation)
			)

		return output

	@classmethod
	def reset(cls):
		# Erases all the data in the person list
		cls.list_of_persons = []

	@classmethod
	def get_person(cls, id):
		try:
			person_id = int(id)
			for person in cls.list_of_persons:
				if person.uniqueId == person_id:
					return person
		except ValueError:
			raise ValueError("Wrong id format. id must be a number")
