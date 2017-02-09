from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.room import Room

class LivingSpace(Room):
	"""docstring for LivingSpace"""
	livingspace_list = {}

	def __init__(self, name):
		super(LivingSpace, self).__init__(name)
		self.type = "livingspace"


	def add_to_livingspace_list(livingspace_instance):
		LivingSpace.livingspace_list[livingspace_instance.name] = livingspace_instance
	
		