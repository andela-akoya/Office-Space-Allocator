from os import path, sys

from app.person import Person


class Staff(Person):
	"""
    This class implements staff specific functionalities and inherits from
    the person class.
    """
	staff_list = []
	unallocated_staff = []

	def __init__(self, staff_id,  lname, fname):
		super(Staff, self).__init__(staff_id, lname, fname)
		self.__category = "staff"

	@property
	def category(self):
		# this method returns the value of the category property
		return self.__category

	@category.setter
	def category(self, new_category):
		# this method sets the value of the category property
		self.__category = new_category.lower()

	@classmethod
	def add_to_staff_list(cls, staff):
		# this method adds a staff to the list of staff
		cls.staff_list.append(staff)

	@classmethod
	def get_staff_list(cls):
		# returns a list containing all staff
		return cls.staff_list

	@classmethod
	def add_unallocated_staff(cls, staff):
		# This method adds a staff to the unallocated list
		cls.unallocated_staff.append(staff)

	@classmethod
	def get_unallocated_staff(cls):
		# returns a list of all the unallocated staff
		return cls.unallocated_staff

	@classmethod
	def remove_from_unallocated_staff_list(cls, staff):
		# removes a staff from the list of unallocated staff
		cls.unallocated_staff.remove(staff)

	@classmethod
	def reset(cls):
		# Erases all the data in the staff list and unallocated staff list
		cls.staff_list = []
		cls.unallocated_staff = []
