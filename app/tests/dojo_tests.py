import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from app.dojo import Dojo
from app.room import Room
from app.staff import Staff
from app.fellow import Fellow


class TestRoom(unittest.TestCase):

	def setUp(self):
		self.dojo_instance = Dojo()

	def reset_total_number_of_rooms():
		Room.total_number_of_rooms = 0

	def test_create_room(self):
		""" tests whether a room was created """
		TestRoom.reset_total_number_of_rooms()
		initial_room_count = Room.get_total_number_of_rooms()
		new_room = Dojo.create_room('Office', ['purple'])
		latter_room_count = Room.get_total_number_of_rooms()
		self.assertTrue(new_room)
		self.assertEqual(latter_room_count - initial_room_count, 1)
		self.assertNotEqual(initial_room_count, latter_room_count)

	def test_create_multiple_rooms(self):
		''' test if multiple rooms were successfully created '''
		TestRoom.reset_total_number_of_rooms()
		initial_room_count = Room.get_total_number_of_rooms()
		new_rooms = Dojo.create_room('Office', ['red', 'green', 'blue'])
		latter_room_count = Room.get_total_number_of_rooms()
		self.assertTrue(new_rooms)
		self.assertEqual(latter_room_count - initial_room_count, 3)
		self.assertNotEqual(initial_room_count, latter_room_count)

	def test_create_rooms_with_valid_name_format(self):
		""" test if only rooms with valid names format only are created """
		TestRoom.reset_total_number_of_rooms()
		initial_room_count = Room.get_total_number_of_rooms()
		new_rooms = Dojo.create_room(
					'LivingSpace', ['Orange', 'Yellow', "\"\""])
		latter_room_count = Room.get_total_number_of_rooms()
		self.assertTrue(new_rooms)
		self.assertNotEqual(initial_room_count, latter_room_count)
		self.assertEqual(latter_room_count, 2)

	def test_create_duplicate_room(self):
		""" the create_room function shouldn't create an already existing 
		room within the same type category """
		new_room1 = Dojo.create_room("Office", "Orange")
		initial_room_count = Dojo.get_total_rooms()
		self.assertEqual(initial_room_count, 1)
		new_room2 = Dojo.create_room("Office", "Orange")
		latter_room_count = Dojo.get_total_rooms()
		self.assertEqual(new_room2, "An Office called Orange already exist")
		self.assertEqual(initial_room_count, latter_room_count)

	# def test_remove_room(self):
	# 	""" test checks if function successfully removes a specicified room name and room type """
	# 	new_room1 = self.dojo_instance.create_room("Office", ["Orange"])
	# 	initial_room_count = Dojo.get_total_rooms()
	# 	self.assertEqual(initial_room_count, 1)
	# 	Dojo.remove_room(new_room1)
	# 	latter_room_count = Dojo.get_total_rooms()
	# 	self.assertEqual(latter_room_count, 0)

	# def test_add_person(self):
	# 	""" test  if a person is successfully added to an office """
	# 	new_office = Dojo.create_room('Office', ['Orange'])
	# 	self.assertTrue(new_office)
	# 	new_staff = Staff("Koya", "Gabriel")
	# 	self.assertTrue(new_staff)
	# 	Dojo.add_person(new_staff)
	# 	self.assertEqual(len(new_office.room_members), 1)
	# 	new_staff2 = Staff("John", "Doe")
	# 	self.assertTrue(new_staff2)
	# 	self.assertEqual(len(new_office.room_members), 2)






		









	
