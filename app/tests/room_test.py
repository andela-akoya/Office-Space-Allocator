import unittest
from os import path, sys

from app.person import Person
from app.room import Room


class TestRoom(unittest.TestCase):

    def setUp(self):
        self.room_instance = Room("test")

    def tearDown(self):
        Room.list_of_rooms = []

    def test_instantiates_room(self):
        "test if a room was sucessfully instantiated"
        self.assertTrue(self.room_instance)

    def test_instance_of_room_created(self):
        """ test if the instance of the room object created
        is a Room instance """
        self.assertIsInstance(self.room_instance, Room)

    def test_name_property_of_instantiated_room(self):
        """ test if the name was appropriate set based on
        the passed argument """
        self.assertEqual(self.room_instance.name, "test".capitalize())

    def test_room_members_property_of_instantiated_room(self):
        """ test if the number of room members is 0 when the
        room is initially instantiated"""
        self.assertEqual(len(self.room_instance.room_members), 0)

    def test_name_property_setter_with_valid_name_argument(self):
        """ test the name property setter if it successfully
        changes the name property of a room with the valid argument
        passed in
        """
        self.assertEqual(self.room_instance.name, "test".capitalize())
        self.room_instance.name = "Orange"
        self.assertEqual(self.room_instance.name, "Orange")

    def test_name_property_setter_with_invalid_name_argument(self):
        """ test if the name property setter if approprite error
        message is returned for an empty string passed as argument
        """
        self.assertEqual(self.room_instance.name, "test".capitalize())
        with self.assertRaises(ValueError) as context:
            self.room_instance.name = ""
            self.assertEqual("Room name must be a string and can't be empty",
                             context.exception.message)

    def test_room_members_property_setter_with_person_instance(self):
        """ test the setter method for the room members property if it
        properly sets the property if a person instance is passed"""
        self.assertEqual(len(self.room_instance.room_members), 0)
        new_person = Person(1, "koya", "gabriel")
        self.room_instance.room_members = new_person
        self.assertEqual(len(self.room_instance.room_members), 1)

    def test_room_members_property_setter_with_non_person_instance(self):
        """ test the setter method for the room members property if it
        returns the proper error message if non person instance is passed
        as value"""
        self.assertEqual(len(self.room_instance.room_members), 0)
        with self.assertRaises(ValueError) as context:
            self.room_instance.room_members = ""
            self.assertEqual("Only a person, staff, or fellow instance can be removed",
                             context.exception.message)

    def test_remove_member_with_a_non_person_instance(self):
        """ tests the remove_member method for approprite error
        messages if a non person instance is passed in as value"""
        self.assertEqual(len(self.room_instance.room_members), 0)
        with self.assertRaises(ValueError) as context:
            self.room_instance.remove_member("")
            self.assertEqual("Only a person, staff, or fellow instance can be removed",
                             context.exception.message)

    def test_remove_member_with_a_person_instance(self):
        """ tests the remove_member method for approprite error
        messages if a non person instance is passed in as value"""
        self.assertEqual(len(self.room_instance.room_members), 0)
        new_person = Person(1, "Koya", "Gabriel")
        self.room_instance.room_members = new_person
        self.assertEqual(len(self.room_instance.room_members), 1)
        self.room_instance.remove_member(new_person)
        self.assertEqual(len(self.room_instance.room_members), 0)
