from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.person import Person 
class Fellow(Person):
	"""docstring for Fellow"""
	def __init__(self, lname, fname):
		super(Fellow, self).__init__(lname, fname)
		self.category = "fellow"

		