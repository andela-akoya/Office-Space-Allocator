from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.person import Person 
class Staff(Person):
	"""docstring for Staff"""
	staff_list = []
	unallocated_staff = []

	def __init__(self, lname, fname):
		super(Staff, self).__init__(lname, fname)
		self.category = "staff"

	def add_to_staff_list(staff):
		Staff.staff_list.append(staff)

	def add_unallocated_staff(staff):
		Staff.unallocated_staff.append(staff)

	def get_unallocated_staff():
		return Staff.unallocated_staff

	
		
		
		