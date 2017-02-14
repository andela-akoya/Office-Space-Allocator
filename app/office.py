from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.room import Room

class Office(Room):
	"""docstring for Office"""
	office_list = {}

	def __init__(self, name):
		super(Office, self).__init__(name)
		self.type = "office"
		self.maximum_capacity = 4

	def add_to_office_list(office_instance):
		Office.office_list[office_instance.name] = office_instance

	def exist(office_name):
		if office_name in list(Office.office_list.keys()):
			raise Exception("An Office with the name " \
							+ office_name \
							+ " already exist")

		return True

		

		
		
		
		