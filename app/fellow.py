from os import sys, path

from app.person import Person

sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))


class Fellow(Person):
	"""docstring for Fellow"""

	fellow_list = []
	unallocated_fellows = {"office": [], "livingspace": []}

	def __init__(self, lname, fname):
		super(Fellow, self).__init__(lname, fname)
		self.category = "fellow"
		self.livingspace = None
		self.wants_accomodation = False

	def set_assigned_livingspace(self, livingspace):
		self.livingspace = livingspace

	def get_assigned_livingspace(self):
		return self.livingspace

	def set_wants_accomodation(self, param):
		self.wants_accomodation = param

	def get_wants_accomodation(self):
		return self.wants_accomodation

	def set_category(self, new_category):
		self.category = new_category.lower()

	def get_category(self):
		return self.category

	@classmethod
	def add_to_fellow_list(cls, fellow):
		cls.fellow_list.append(fellow)

	@classmethod
	def add_unallocated_fellow(cls, fellow, office=False, livingspace=False):
		if office and livingspace:
			cls.unallocated_fellows["office"].append(fellow)
			cls.unallocated_fellows["livingspace"].append(fellow)
		elif office:
			cls.unallocated_fellows["office"].append(fellow)
		else:
			cls.unallocated_fellows["livingspace"].append(fellow)

	@classmethod
	def get_unallocated_fellows(cls):
		return cls.unallocated_fellows

	@classmethod
	def remove_from_unallocated_fellow_list(cls, fellow, room_type):
		cls.unallocated_fellows[room_type].remove(fellow)
