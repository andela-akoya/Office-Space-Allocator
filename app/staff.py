from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.person import Person 
class Staff(Person):
	"""docstring for Staff"""
	def __init__(self, lname, fname):
		super(Staff, self).__init__(lname, fname)
		self.category = "staff"
		
		