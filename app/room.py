from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
import random
from app.fellow import Fellow
from app.staff import Staff
from app.person import Person

class Room():
	
	total_number_of_rooms = 0
	room_list = {}

	def __init__(self, name):
		self.name = name
		self.is_full = False
		self.room_members = []
		Room.total_number_of_rooms += 1

	def add_room(room):
		Room.room_list[room.name] = room