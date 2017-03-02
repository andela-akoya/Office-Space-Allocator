import unittest
from os import path, sys

from app.dojo import Dojo
from app.errors import WrongFormatException
from app.fellow import Fellow
from app.livingspace import LivingSpace
from app.office import Office
from app.person import Person
from app.room import Room
from app.staff import Staff

sys.path.append(path.dirname(path.dirname(
    path.dirname(path.abspath(__file__)))))


class TestDojo(unittest.TestCase):

    def setUp(self):
        self.filepath = path.dirname(path.dirname(path.abspath(__file__))) \
            + "\\data\\documents\\"

    def tearDown(self):
        Room.total_number_of_rooms = 0
        Room.list_of_rooms = []
        Office.office_list = {}
        LivingSpace.livingspace_list = {}
        Staff.staff_list = []
        Fellow.fellow_list = []

    def test_create_room(self):
        """ tests whether a room was created """
        initial_room_count = Room.get_total_number_of_rooms()
        new_room = Dojo.create_room('Office', ['purple'])[0]
        latter_room_count = Room.get_total_number_of_rooms()
        self.assertTrue(new_room)
        self.assertEqual(latter_room_count - initial_room_count, 1)

    def test_create_multiple_rooms(self):
        ''' test if multiple rooms were successfully created '''
        initial_room_count = Room.get_total_number_of_rooms()
        new_rooms = Dojo.create_room('Office', ['red', 'green', 'blue'])
        latter_room_count = Room.get_total_number_of_rooms()
        self.assertTrue(new_rooms)
        self.assertEqual(latter_room_count - initial_room_count, 3)

    def test_create_rooms_with_valid_name_format(self):
        """ test the create_room function if only rooms
        with valid name format only are created """
        initial_room_count = Room.get_total_number_of_rooms()
        new_rooms = Dojo.create_room('LivingSpace', ['Python',
                                                     'Yellow', "\"\""])
        later_room_count = Room.get_total_number_of_rooms()
        self.assertTrue(new_rooms)
        self.assertNotEqual(later_room_count, 3)
        self.assertEqual(later_room_count, 2)

    def test_create_duplicate_room(self):
        """ the create_room function shouldn't create an already existing
        room """
        new_room1 = Dojo.create_room("Office", ["Orange"])[0]
        initial_room_count = Dojo.get_total_rooms()
        self.assertEqual(initial_room_count, 1)
        new_room2 = Dojo.create_room("Office", ["Orange"])
        later_room_count = Dojo.get_total_rooms()
        self.assertFalse(new_room2)
        self.assertEqual(initial_room_count, later_room_count)

    def test_create_room_with_valid_type_alone(self):
        """ the create_room function shouldn't create a room without a valid
        type like office or livingspace """
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
        new_office = Dojo.create_room('Office', ['Orange'])[0]
        self.assertTrue(new_office)
        Dojo.add_person("koya", "gabriel", "staff")
        self.assertEqual(len(new_office.room_members), 1)

    def test_add_fellow_no_accomodation(self):
        """ test  if a fellow that doesn't want accomodation is successfully
        added and allocated an office only  """
        new_office = Dojo.create_room('Office', ['Orange'])[0]
        new_livingspace = Dojo.create_room('livingspace', ['kfc'])[0]
        Dojo.add_person("koya", "gabriel", "fellow")
        self.assertEqual(len(new_office.room_members), 1)
        self.assertEqual(len(new_livingspace.room_members), 0)

    def test_add_fellow_with_accomodation(self):
        """ test if a fellow that wants accomodation is successfully
        added and allocated an office and a livingspace  """
        new_office = Dojo.create_room('Office', ['Orange'])[0]
        new_livingspace = Dojo.create_room('livingspace', ['kfc'])[0]
        Dojo.add_person("koya", "gabriel", "fellow", 'y')
        self.assertEqual(len(new_office.room_members), 1)
        self.assertEqual(len(new_livingspace.room_members), 1)

    def test_add_person_with_valid_category(self):
        """ test if only people with valid categorys are successfully
        added and allocated a space  """
        new_office = Dojo.create_room('Office', ['Orange'])[0]
        Dojo.add_person("koya", "gabriel", "staff")
        self.assertEqual(len(new_office.room_members), 1)
        Dojo.add_person("John", "Doe", "")
        self.assertEqual(len(new_office.room_members), 1)

    def test_add_person(self):
        """ test if a person instance was created"""
        new_office = Dojo.create_room('Office', ['Orange'])[0]
        Dojo.add_person("koya", "gabriel", "staff")
        person = new_office.room_members[0]
        self.assertIsInstance(person, Person)

    def test_add_person_to_unallocated_list(self):
        """
        test if the add_person function adds the person to the
        unallocated list if no rooms are available
        """
        Dojo.add_person("koya", "gabriel", "staff")
        Dojo.add_person("John", "fauls", "fellow", "y")
        self.assertEqual(len(Staff.get_unallocated_staff()), 1)
        self.assertEqual(len(Fellow.get_unallocated_fellows()['office']), 1)
        self.assertEqual(
            len(Fellow.get_unallocated_fellows()['livingspace']), 1)

    def test_print_room_with_wrong_room_name(self):
        """
        test the print_room function if appropriate message
        will be returned if a non existing room name is passed in as
        value
        """
        Dojo.print_room("orange")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "The room with the name {} does not exist"
                         .format("orange"))

    def test_print_room(self):
        """
        test the print_room function if no warning message
        will be returned if an existing room name is passed in as
        value
        """
        new_office = Dojo.create_room("office", ["orange"])[0]
        Dojo.print_room("orange")
        output = sys.stdout.getvalue().strip()
        self.assertNotEqual(output, "The room with the name {} does not exist"
                            .format("orange"))

    def test_print_allocations_with_existing_filename(self):
        """
        test the print_allocations for a warning
        message if an already existing filename is
        inputed as value.
        """
        filename = "file1.txt"
        open(self.filepath + filename, "w").close()
        Dojo.print_allocations("file1")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "file1.txt already exist")

    def test_print_allocations_with_new_filename(self):
        """
        test the print_allocations whether it successfully create
        a new file if a non-existing filename is passed as value.
        """
        filename = "file2.txt"
        Dojo.print_allocations("file2")
        self.assertTrue(path.isfile(self.filepath + filename))

    def test_print_unallocated_with_existing_filename(self):
        """
        test the print_unallocated for a warning
        message if an already existing filename is
        inputed as value.
        """
        filename = "file3.txt"
        open(self.filepath + filename, "w").close()
        Dojo.print_unallocated("file3")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "file3.txt already exist")

    def test_print_unallocated_with_new_filename(self):
        """
        test the print_unallocated whether it successfully create
        a new file if a non-existing filename is passed as value.
        """
        filename = "file4.txt"
        Dojo.print_allocations("file4")
        self.assertTrue(path.isfile(self.filepath + filename))

    def test_reallocate_person(self):
        """
        tests the reallocate_person function if it successfully
        reallocates a person to a specified room
        """
        new_office = Dojo.create_room("office", ["red"])[0]
        self.assertEqual(len(new_office.room_members), 0)
        Dojo.add_person("koya", "gabriel", "staff")
        person = Staff.get_staff_list()[0]
        self.assertEqual(len(new_office.room_members), 1)
        self.assertEqual(person.office.name.lower(),
                         "red")
        new_office2 = Dojo.create_room("office", ["orange"])[0]
        Dojo.reallocate_person(person.id, "Orange")
        self.assertEqual(len(new_office.room_members), 0)
        self.assertEqual(len(new_office2.room_members), 1)
        self.assertEqual(person.office.name.lower(),
                         "orange")
