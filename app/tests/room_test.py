import unittest
from os import path, sys

from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
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
        """ tests the remove_member method if it successfully
        removes a member if a person instance was passed"""
        self.assertEqual(len(self.room_instance.room_members), 0)
        new_person = Person(1, "Koya", "Gabriel")
        self.room_instance.room_members = new_person
        self.assertEqual(len(self.room_instance.room_members), 1)
        self.room_instance.remove_member(new_person)
        self.assertEqual(len(self.room_instance.room_members), 0)

    def test_add_room_with_a_non_room_instance(self):
        """ tests the add_room method for approprite error
        messages if a non room instance is passed in as value"""
        with self.assertRaises(ValueError) as context:
            Room.add_room(True)
            self.assertEqual(
                "Only a room, office, or livingspace instance can be added",
                context.exception.message)

    def test_add_room_with_an_office_instance(self):
        """ tests the add_room method if it sucessfully adds an
        office instance to the room list if it is passed as value"""
        self.assertEqual(len(Room.get_room_list()), 0)
        new_office = Office("Orange")
        Room.add_room(new_office)
        self.assertEqual(len(Room.get_room_list()), 1)

    def test_add_room_with_a_livingspace_instance(self):
        """ tests the add_room method if it sucessfully adds an
        livingspace instance to the room list if it is passed as value"""
        self.assertEqual(len(Room.get_room_list()), 0)
        new_livingspace = LivingSpace("kfc")
        Room.add_room(new_livingspace)
        self.assertEqual(len(Room.get_room_list()), 1)

    def test_get_random_room_with_an_empty_room_list(self):
        """ tests the get random room method if it returns false when an empty
        room list is passed as argument """
        self.assertFalse(Room.get_random_room([]))

    def test_get_random_room_with_non_empty_room_list(self):
        """ test if a random room is chosen when a room list is passed
        as argument """
        self.assertEqual(len(Room.get_room_list()), 0)
        new_livingspace = LivingSpace("kfc")
        Room.add_room(new_livingspace)
        self.assertEqual(Room.get_random_room(Room.get_room_list()),
                         new_livingspace)

    def test_get_available_rooms_with_an_empty_room_list(self):
        """ tests the get available rooms method if it returns an empty list
         when an empty room list is passed as argument """
        self.assertFalse(Room.get_available_rooms([]))

    def test_get_available_rooms_with_non_empty_room_list(self):
        """ tests the get available rooms method if it returns  a list of
        available rooms when a non empty room list is passed as argument """
        Room.add_room(Office("red"))
        Room.add_room(LivingSpace("kfc"))
        self.assertEqual(
            len(Room.get_available_rooms(Room.get_room_list())), 2)

    def test_get_available_rooms_with_filled_rooms(self):
        """ tests the get available rooms method if it returns an empty
        list when a list of filled rooms is passed as argument """
        new_livingspace = LivingSpace("kfc")
        new_livingspace.room_members = Fellow(1, "koya", "gabriel")
        new_livingspace.room_members = Fellow(2, "Samuel", "ajayi")
        new_livingspace.room_members = Fellow(3, "Delores", "dei")
        new_livingspace.room_members = Fellow(4, "Alamu", "Yusuf")
        Room.get_room_list().append(new_livingspace)
        self.assertFalse(Room.get_available_rooms(Room.get_room_list()))

    def test_get_total_number_of_rooms(self):
        """ test the get_total_number_of_rooms method if it returns
        the total number of rooms that have been created """
        self.assertEqual(len(Room.get_room_list()), 0)
        Room.get_room_list().append(Office("red"))
        Room.get_room_list().append(LivingSpace("kfc"))
        self.assertEqual(Room.get_total_number_of_rooms(), 2)

    def test_get_a_particular_room_with_uncreated_room_name(self):
        """ test the get_a_particular_room method if it returns the
        proper error message if a non existing room name is passed as
        argument """
        Room.get_room_list().append(Office("red"))
        self.assertEqual(Room.get_a_particular_room(
            "blue"), "Room blue doesn't exist")

    def test_get_a_particular_room_with_a_valid_room_name(self):
        """ test the get_a_particular_room method if it returns the
        proper room if an existing room name is passed as
        argument """
        Room.get_room_list().append(Office("Red"))
        self.assertEqual(Room.get_a_particular_room(
            "Red").name, "Red")

    def test_exists_with_non_existing_room_name(self):
        """ test the exists method if it returns false if a non existing
        room name is passed as argument """
        Room.get_room_list().append(Office("red"))
        self.assertFalse(Room.exists("blue"))

    def test_exists_with_an_existing_room_name(self):
        """ test the exists method if it returns true if an existing
        room name is passed as argument """
        Room.get_room_list().append(Office("red"))
        self.assertTrue(Room.exists("red"))

    def test_export_in_database_format(self):
        """ test the export+in_database_format if it returns a
        list of tuple instances """
        Room.get_room_list().append(Office("red"))
        self.assertIsInstance(Room.export_in_database_format(), list)
        self.assertIsInstance(Room.export_in_database_format()[0], tuple)
