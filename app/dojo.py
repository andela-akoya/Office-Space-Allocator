from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.office import Office
from app.livingspace import LivingSpace
from app.room import Room

class Dojo(object):
	"""docstring for Dojo"""
	def __init__(self):
		pass


	def create_room(room_type, room_names):
		pass
		

	def delete_room(room_type, room_name):
		pass

	def get_total_rooms():
		pass