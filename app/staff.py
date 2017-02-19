from os import sys, path

from app.person import Person

sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))


class Staff(Person):
	"""docstring for Staff"""
	staff_list = []
	unallocated_staff = []

	def __init__(self, lname, fname):
		super(Staff, self).__init__(lname, fname)
		self.category = "staff"

	def get_category(self):
		return self.category

	def set_category(self, new_category):
		self.category = new_category.lower()

	@classmethod
	def add_to_staff_list(cls, staff):
		cls.staff_list.append(staff)

	@classmethod
	def add_unallocated_staff(cls, staff):
		cls.unallocated_staff.append(staff)

	@classmethod
	def get_unallocated_staff(cls):
		return cls.unallocated_staff

	@classmethod
	def remove_from_unallocated_staff_list(cls, staff):
		cls.unallocated_staff.remove(staff)
