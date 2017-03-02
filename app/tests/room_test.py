import unittest

from app.room import Room


class TestRoom(unittest.TestCase):

    def setUp(self):
        self.room_instance = Room("test")

    def tearDown(self):
        Room.total_number_of_rooms = 0
        Room.list_of_rooms = []

    def test_instantiates_room(self):
        "test if a room was sucessfully instantiated"
        self.assertTrue(self.room_instance)

    def test_instance_of_room_created(self):
        """ test if the instance of the room object created
        is a Room instance """
        self.assertIsInstance(self.room_instance, Room)
