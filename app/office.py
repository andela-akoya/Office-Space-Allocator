from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.room import Room

class Office(Room):
	"""docstring for Office"""
	office_list = {}

	def __init__(self, name):
		super(Office, self).__init__(name)
		self.type = "office"

	def add_to_office_list(office_instance):
		pass
		

		
		
		
		