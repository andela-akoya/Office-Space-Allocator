from os import path, sys

from app.person import Person


class Fellow(Person):
	"""This class holds the properties and methods of a fellow object
	and also inherits from the Person class"""

	fellow_list = []
	unallocated_fellows = {"office": [], "livingspace": []}

	def __init__(self, fellow_id, lname, fname, wants_accomodation=False):
		super(Fellow, self).__init__(fellow_id, lname, fname)
		self.__category = "fellow"
		self.__livingspace = None
		self.__wants_accomodation = wants_accomodation

	@property
	def livingspace(self):
		""" returns the value of the livingspace property """
		return self.__livingspace

	@livingspace.setter
	def livingspace(self, livingspace):
		""" sets the value of the livingspace property to the value of the
		argument passed in """
		self.__livingspace = livingspace

	@property
	def wants_accomodation(self):
		""" returns the value of the wants_accomodation property """
		return self.__wants_accomodation

	@wants_accomodation.setter
	def wants_accomodation(self, param):
		""" sets the value of the wants_accomodation property """
		self.__wants_accomodation = param

	@property
	def category(self):
		""" returns the value of the category property """
		return self.__category

	@category.setter
	def category(self, new_category):
		""" sets the value of the category property """
		self.__category = new_category.lower()

	@classmethod
	def add_to_fellow_list(cls, fellow):
		""" adds a fellow to the list of fellows """
		cls.fellow_list.append(fellow)

	@classmethod
	def get_fellow_list(cls):
		""" returns the list containing all fellows """
		return cls.fellow_list

	@classmethod
	def add_unallocated_fellow(cls, fellow, office=False, livingspace=False):
		""" adds a fellow to the unallocated list """
		if office and livingspace:
			cls.unallocated_fellows["office"].append(fellow)
			cls.unallocated_fellows["livingspace"].append(fellow)
		elif office:
			cls.unallocated_fellows["office"].append(fellow)
		else:
			cls.unallocated_fellows["livingspace"].append(fellow)

	@classmethod
	def get_unallocated_fellows(cls):
		""" returns a list containing all unallocated list """
		return cls.unallocated_fellows

	@classmethod
	def remove_from_unallocated_fellow_list(cls, fellow, room_type):
		""" removes a fellow from the unallocated list """
		cls.unallocated_fellows[room_type].remove(fellow)
