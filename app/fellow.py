from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.person import Person 

class Fellow(Person):
	"""docstring for Fellow"""

	fellow_list = []
	unallocated_fellows = {"office" : [], "livingspace" : []}
	
	def __init__(self, lname, fname):
		super(Fellow, self).__init__(lname, fname)
		self.category = "fellow"
		self.livingspace = ""

	def add_to_fellow_list(fellow):
		Fellow.fellow_list.append(fellow)

	def add_unallocated_fellow(fellow, office=False, livingspace = False):
		if office and livingspace:
			Fellow.unallocated_fellows["office"].append(fellow)
			Fellow.unallocated_fellows["livingspace"].append(fellow)
		elif office:
			Fellow.unallocated_fellows["office"].append(fellow)
		else:
			Fellow.unallocated_fellows["livingspace"].append(fellow)

	def get_unallocated_fellows():
		return Fellow.unallocated_fellows

	def set_assigned_livingspace(self, livingspace):
		self.livingspace = livingspace


	