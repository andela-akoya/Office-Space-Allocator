import unittest
from os import sys, path

from app.dojo import Dojo
from app.room import Room
from app.staff import Staff
from app.fellow import Fellow

sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))


class TestRoom(unittest.TestCase):

	def reset_total_number_of_rooms():
		Room.total_number_of_rooms = 0
		Room.room_list = {}

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
		""" test if only rooms with valid name format only are created """
		TestRoom.reset_total_number_of_rooms()
		initial_room_count = Room.get_total_number_of_rooms()
		new_rooms = Dojo.create_room('LivingSpace', ['Python',
													 'Yellow', "\"\""])
		later_room_count = Room.get_total_number_of_rooms()
		self.assertTrue(new_rooms)
		self.assertNotEqual(initial_room_count, later_room_count)
		self.assertEqual(later_room_count, 2)

	def test_create_duplicate_room(self):
		""" the create_room function shouldn't create an already existing
		room """
		TestRoom.reset_total_number_of_rooms()
		new_room1 = Dojo.create_room("Office", ["Orange"])
		initial_room_count = Dojo.get_total_rooms()
		self.assertEqual(initial_room_count, 1)
		new_room2 = Dojo.create_room("Office", ["Orange"])
		later_room_count = Dojo.get_total_rooms()
		self.assertEqual(initial_room_count, later_room_count)

	def test_create_room_with_valid_type_alone(self):
		""" the create_room function shouldn't create a room without a valid
		type like office or livingspace """
		TestRoom.reset_total_number_of_rooms()
		initial_room_count = Dojo.get_total_rooms()
		self.assertEqual(initial_room_count, 0)
		new_room1 = Dojo.create_room("", ["Orange"])
		new_room2 = Dojo.create_room("", ["Red"])
		later_room_count = Dojo.get_total_rooms()
		self.assertFalse(new_room1)
		self.assertFalse(new_room2)
		self.assertEqual(initial_room_count, later_room_count)

	def test_add_staff(self):
		""" test  if a staff is successfully added and allocated an office """
		TestRoom.reset_total_number_of_rooms()
		new_office = Dojo.create_room('Office', ['Orange'])
		self.assertTrue(new_office)
		Dojo.add_person("koya", "gabriel", "staff")
		self.assertEqual(len(new_office[0].room_members), 1)
		Dojo.add_person("John", "Doe", "staff")
		self.assertEqual(len(new_office[0].room_members), 2)

	def test_add_fellow_no_accomodation(self):
		""" test  if a fellow that doesn't want accomodation is successfully
		added and allocated an office only  """
		TestRoom.reset_total_number_of_rooms()
		new_office = Dojo.create_room('Office', ['Orange'])
		new_livingspace = Dojo.create_room('livingspace', ['kfc'])
		self.assertTrue(new_office)
		self.assertTrue(new_livingspace)
		Dojo.add_person("koya", "gabriel", "fellow")
		self.assertEqual(len(new_office[0].room_members), 1)
		self.assertEqual(len(new_livingspace[0].room_members), 0)
		Dojo.add_person("John", "Doe", "fellow")
		self.assertEqual(len(new_office[0].room_members), 2)
		self.assertEqual(len(new_livingspace[0].room_members), 0)

	def test_add_fellow_with_accomodation(self):
		""" test if a fellow that wants accomodation is successfully
		added and allocated an office and a livingspace  """
		TestRoom.reset_total_number_of_rooms()
		new_office = Dojo.create_room('Office', ['Orange'])
		new_livingspace = Dojo.create_room('livingspace', ['kfc'])
		self.assertTrue(new_office)
		self.assertTrue(new_livingspace)
		Dojo.add_person("koya", "gabriel", "fellow", 'y')
		self.assertEqual(len(new_office[0].room_members), 1)
		self.assertEqual(len(new_livingspace[0].room_members), 1)
		Dojo.add_person("John", "Doe", "fellow", 'y')
		self.assertEqual(len(new_office[0].room_members), 2)
		self.assertEqual(len(new_livingspace[0].room_members), 2)

	def test_add_person_with_valid_category(self):
		""" test if only people with valid categorys are successfully
		added and allocated a space  """
		TestRoom.reset_total_number_of_rooms()
		new_office = Dojo.create_room('Office', ['Orange'])
		self.assertTrue(new_office)
		Dojo.add_person("koya", "gabriel", "staff")
		self.assertEqual(len(new_office[0].room_members), 1)
		Dojo.add_person("John", "Doe", "")
		self.assertEqual(len(new_office[0].room_members), 1)
