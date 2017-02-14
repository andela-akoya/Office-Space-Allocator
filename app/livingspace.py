from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.room import Room

class LivingSpace(Room):
	"""docstring for LivingSpace"""

	livingspace_list = {}

	def __init__(self, name):
		super(LivingSpace, self).__init__(name)
		self.type = "livingspace"
		self.maximum_capacity = 6


	def add_to_livingspace_list(livingspace):
		LivingSpace.livingspace_list[livingspace.name] = livingspace
	

	def exist(livingspace_name):
		if livingspace_name in list(LivingSpace.livingspace_list.keys()):
			raise Exception("A livingspace with the name " \
							+ livingspace_name  \
							+ " already exist")

		return True
	
		