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


class TestDojo(unittest.TestCase):

    def setUp(self):
        self.filepath = path.dirname(path.dirname(path.abspath(__file__))) \
            + "/data/documents/"

    def tearDown(self):
        Room.total_number_of_rooms = 0
        Room.list_of_rooms = []
        Office.list_of_offices = []
        LivingSpace.list_of_livingspace = []
        Staff.staff_list = []
        Fellow.fellow_list = []
        Fellow.unallocated_fellows = {"office": [], "livingspace": []}
        Staff.unallocated_staff = []

    def test_create_room(self):
        """ tests whether a room was created """
        initial_room_count = Room.get_total_number_of_rooms()
        new_room, = Dojo.create_room('Office', ['purple'])
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
        new_room1, = Dojo.create_room("Office", ["Orange"])
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

    def test_add_person_staff(self):
        """ test add_person_method if a staff is successfully
        added and allocated an office """
        new_office, = Dojo.create_room('Office', ['Orange'])
        self.assertTrue(new_office)
        Dojo.add_person("koya", "gabriel", "staff")
        self.assertEqual(len(new_office.room_members), 1)

    def test_add_person_fellow_no_accomodation(self):
        """ test  add_person method if a fellow
        that doesn't want accomodation is successfully
        added and allocated an office only  """
        new_office, = Dojo.create_room('Office', ['Orange'])
        new_livingspace, = Dojo.create_room('livingspace', ['kfc'])
        Dojo.add_person("koya", "gabriel", "fellow")
        self.assertEqual(len(new_office.room_members), 1)
        self.assertEqual(len(new_livingspace.room_members), 0)

    def test_add_person_fellow_with_accomodation(self):
        """ test add_person method if a fellow
        that wants accomodation is successfully
        added and allocated an office and a livingspace  """
        new_office, = Dojo.create_room('Office', ['Orange'])
        new_livingspace, = Dojo.create_room('livingspace', ['kfc'])
        Dojo.add_person("koya", "gabriel", "fellow", 'y')
        self.assertEqual(len(new_office.room_members), 1)
        self.assertEqual(len(new_livingspace.room_members), 1)

    def test_add_person_with_valid_category(self):
        """ test if only people with valid categorys are successfully
        added and allocated a space  """
        new_office, = Dojo.create_room('Office', ['Orange'])
        Dojo.add_person("koya", "gabriel", "staff")
        self.assertEqual(len(new_office.room_members), 1)
        Dojo.add_person("John", "Doe", "")
        self.assertEqual(len(new_office.room_members), 1)

    def test_add_person(self):
        """ test if a person instance was created"""
        new_office, = Dojo.create_room('Office', ['Orange'])
        Dojo.add_person("koya", "gabriel", "staff")
        person, = new_office.room_members
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

    def test_add_person_with_invalid_name_format(self):
        """ test if the add_person method returns appropriate
        error if an invalid name format is passed as argument """
        Dojo.add_person("'", "gabriel", "staff")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(
            output, "Firstname or Lastname is not a valid name format")

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
        new_office, = Dojo.create_room("office", ["orange"])
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

    def test_print_allocations_with_invalid_filename_format(self):
        """
        test the print_allocations whether it returns appropriate
        error message if an invalid filename format is passed as value
        """
        filename = "'"
        Dojo.print_allocations(filename)
        output = sys.stdout.getvalue().strip("\n")
        self.assertEqual(
            output, "{} is not a valid file name".format(filename))

    def test_print_allocations_without_filename(self):
        """ test the print_allocations method if it prints
        the appropriate message if no filename is passed
        as argument """
        office, = Dojo.create_room("office", ["Orange"])
        Dojo.add_person("Koya", "gabriel", "staff")
        expected_output = "Orange Room{}Koya Gabriel, "\
            .format(len(office.name + " Room") * "-")
        Dojo.print_allocations(None)
        output = "".join(sys.stdout.getvalue().split("\n")[4:7])
        self.assertEqual(output, expected_output)

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
        test the print_unallocated whether it successfully creates
        a new file if a non-existing filename is passed as value.
        """
        filename = "file4.txt"
        Dojo.print_allocations("file4")
        print(self.filepath + filename)
        self.assertTrue(path.isfile(self.filepath + filename))

    def test_print_unallocated_without_filename(self):
        """ test the print_unallocated method if it prints
        the appropriate message if no filename is passed
        as argument """
        Dojo.add_person("Koya", "gabriel", "staff")
        expected_output = "Unallocated List {}1. Staff Koya Gabriel"\
            .format(21 * "-")
        Dojo.print_unallocated(None)
        output = "".join(sys.stdout.getvalue().split("\n")[3:7])
        self.assertEqual(output, expected_output)

    def test_reallocate_person_to_office_instance(self):
        """
        tests the reallocate_person function if it successfully
        reallocates a person to a specified office
        """
        new_office, = Dojo.create_room("office", ["red"])
        self.assertEqual(len(new_office.room_members), 0)
        Dojo.add_person("koya", "gabriel", "staff")
        person, = Staff.get_staff_list()
        self.assertEqual(len(new_office.room_members), 1)
        self.assertEqual(person.office.name.lower(),
                         "red")
        new_office2, = Dojo.create_room("office", ["orange"])
        Dojo.reallocate_person(person.id, "Orange")
        self.assertEqual(len(new_office.room_members), 0)
        self.assertEqual(len(new_office2.room_members), 1)
        self.assertEqual(person.office.name.lower(),
                         "orange")

    def test_reallocate_person_to_livingspace_instance(self):
        """
        tests the reallocate_person function if it successfully
        reallocates a person to a specified livingspace
        """
        new_livingspace, = Dojo.create_room("livingspace", ["kfc"])
        self.assertEqual(len(new_livingspace.room_members), 0)
        Dojo.add_person("koya", "gabriel", "fellow", "y")
        person, = Fellow.get_fellow_list()
        self.assertEqual(len(new_livingspace.room_members), 1)
        self.assertEqual(person.livingspace.name.lower(), "kfc")
        new_livingspace2, = Dojo.create_room("livingspace", ["biggs"])
        Dojo.reallocate_person(person.id, "Biggs")
        self.assertEqual(len(new_livingspace.room_members), 0)
        self.assertEqual(len(new_livingspace2.room_members), 1)
        self.assertEqual(person.livingspace.name.lower(), "biggs")

    def test_reallocate_person_with_invalid_id_format(self):
        """
        tests the reallocate_person function if it returns appropriate error
        message if an id with invalid format is passed as argument
        """
        Dojo.reallocate_person("'", "Biggs")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Wrong id format. id must be a number")

    def test_reallocate_person_with_non_existing_person_id(self):
        """
        tests the reallocate_person function if it returns appropriate error
        message if a non existing person id is passed as argument
        """
        Dojo.reallocate_person(10, "Biggs")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Person with the id {} doesn't exist"
                         .format(10))

    def test_reallocate_person_with_non_existing_room_name(self):
        """
        tests the reallocate_person function if it returns appropriate error
        message if a non existing room name is passed as argument
        """
        Dojo.add_person("koya", "gabriel", "fellow", "y")
        person, = Fellow.get_fellow_list()
        Dojo.reallocate_person(person.id, "Biggs")
        output = sys.stdout.getvalue().split("\n")[-2]
        self.assertEqual(output, "Room Biggs doesn't exist")

    def test_reallocate_person_to_a_full_room(self):
        """
        tests the reallocate_person function if it returns appropriate error
        message if the name of a filled up room is passed as argument
        """
        new_livingspace, = Dojo.create_room("livingspace", ["kfc"])
        new_livingspace.room_members = Fellow(1, "koya", "gabriel")
        new_livingspace.room_members = Fellow(2, "Samuel", "ajayi")
        new_livingspace.room_members = Fellow(3, "Delores", "dei")
        new_livingspace.room_members = Fellow(4, "Alamu", "Yusuf")
        Dojo.add_person("orolu", "wumi", "fellow", "y")
        fellow, = Fellow.get_fellow_list()
        Dojo.reallocate_person(fellow.id, new_livingspace.name)
        output = sys.stdout.getvalue().strip().split("\n")[-1]
        self.assertEqual(output,
                         "Room {} is filled up, please input another room"
                         .format(new_livingspace.name))

    def test_reallocate_person_staff_to_livingspace(self):
        """
        tests the reallocate_person function if it returns appropriate error
        message if a staff is to be reallocated to a livingspace
        """
        new_livingspace, = Dojo.create_room("livingspace", ["kfc"])
        Dojo.add_person("orolu", "wumi", "staff")
        staff, = Staff.get_staff_list()
        Dojo.reallocate_person(staff.id, new_livingspace.name)
        output = sys.stdout.getvalue().split("\n")[-2]
        self.assertEqual(output,
                         ("Room {} is a livingspace and can't be assigned to "
                          + "a staff").format(new_livingspace.name))

    def test_reallocate_person_to_already_assigned_room(self):
        """
        tests the reallocate_person function if it returns appropriate error
        message if a staff is to be reallocated to a livingspace
        """
        new_office, = Dojo.create_room("office", ["orange"])
        Dojo.add_person("orolu", "wumi", "staff")
        staff, = Staff.get_staff_list()
        Dojo.reallocate_person(staff.id, new_office.name)
        output = sys.stdout.getvalue().split("\n")[-2]
        self.assertEqual(output,
                         ("{s.surname} {s.firstname} already belongs "
                          + "to room {}, therefore can't be "
                          + "reallocated to the same room")
                         .format(new_office.name, s=staff))

    def test_load_people_with_non_existing_filename(self):
        """
        test the load_people if it returns the appropriate error message
        when a non existing filename is passed as argument
        """
        Dojo.load_people("people")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "No such file: people.txt can't be found")

    def test_load_people_with_incomplete_file_content(self):
        """
        test the load_people method if it returns appropriate
        error message if the file being loaded contains lines with
        incomplete arguments
        """
        new_file = open(self.filepath + "test.txt", "w")
        new_file.write("koya gabriel\n")
        new_file.write("orolu wumi\n")
        new_file.close()
        expected_output = [
            "Errors\n---------",
            "The following people couldn't be loaded"
            + " because of incomplete information\n",
            "koya gabriel",
            "orolu wumi"
        ]
        Dojo.load_people("test")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "\n".join(expected_output))
