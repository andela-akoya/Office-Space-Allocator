import unittest
from os import path, remove, sys

from app.customfile import Customfile
from app.database import Database
from app.dojo import Dojo
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
        self.database_path = path.dirname(path.dirname(path.abspath(__file__))) \
            + "/data/database/"

    def tearDown(self):
        Room.list_of_rooms = []
        Office.list_of_offices = []
        LivingSpace.list_of_livingspace = []
        Person.list_of_persons = []
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

    def test_create_room_with_invalid_office_name_format(self):
        """ tests the create_room method if it returns appropriate
        error message if an invalid office name format is passed in as
        argument """
        Dojo.create_room("office", ["'"])
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "' is not a valid office name format")

    def test_create_room_with_invalid_livingspace_name_format(self):
        """ tests the create_room method if it returns appropriate
        error message if an invalid livingspace name format is passed in as
        argument """
        Dojo.create_room("livingspace", ["'"])
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "' is not a valid livingspace name format")

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
        remove(self.filepath + "file1.txt")

    def test_print_allocations_with_new_filename(self):
        """
        test the print_allocations whether it successfully create
        a new file if a non-existing filename is passed as value.
        """
        filename = "file2.txt"
        Dojo.print_allocations("file2")
        self.assertTrue(path.isfile(self.filepath + filename))
        remove(self.filepath + "file2.txt")

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
        expected_output = "Orange Room ({}){}Koya Gabriel, "\
            .format("office", len(office.name + " Room " + "office") * "-")
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
        remove(self.filepath + "file3.txt")

    def test_print_unallocated_with_new_filename(self):
        """
        test the print_unallocated whether it successfully creates
        a new file if a non-existing filename is passed as value.
        """
        filename = "file4.txt"
        Dojo.print_allocations("file4")
        print(self.filepath + filename)
        self.assertTrue(path.isfile(self.filepath + filename))
        remove(self.filepath + "file4.txt")

    def test_print_unallocated_without_filename(self):
        """ test the print_unallocated method if it prints
        the appropriate message if no filename is passed
        as argument """
        Dojo.add_person("Koya", "gabriel", "staff")
        staff_id = Staff.staff_list[0].uniqueId
        Dojo.add_person("Orolu", "wumi", "fellow")
        fellow1_id = Fellow.fellow_list[0].uniqueId
        Dojo.add_person("Alamu", "Yusuf", "fellow", "y")
        fellow2_id = Fellow.fellow_list[1].uniqueId
        expected_output = ("Unallocated List {}1. Staff Koya Gabriel ({})"
                           + "2. Fellow Orolu Wumi ({}) (Office)"
                           + "3. Fellow Alamu Yusuf ({}) (Office $ Livingspace)")
        Dojo.print_unallocated(None)
        output = "".join(sys.stdout.getvalue().split("\n")[9:])
        self.assertEqual(output, expected_output
                         .format(21 * "-", staff_id, fellow1_id, fellow2_id))

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
        Dojo.reallocate_person(person.uniqueId, "Orange")
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
        Dojo.reallocate_person(person.uniqueId, "Biggs")
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
        self.assertEqual(output, "Reallocation operation failed."
                         + " Either the person or room doesn't exist")

    def test_reallocate_person_with_non_existing_room_name(self):
        """
        tests the reallocate_person function if it returns appropriate error
        message if a non existing room name is passed as argument
        """
        Dojo.add_person("koya", "gabriel", "fellow", "y")
        person, = Fellow.get_fellow_list()
        Dojo.reallocate_person(person.uniqueId, "Biggs")
        output = sys.stdout.getvalue().split("\n")[-2]
        self.assertEqual(output, "Reallocation operation failed."
                         + " Either the person or room doesn't exist")

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
        Dojo.reallocate_person(fellow.uniqueId, new_livingspace.name)
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
        Dojo.reallocate_person(staff.uniqueId, new_livingspace.name)
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
        Dojo.reallocate_person(staff.uniqueId, new_office.name)
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
        content = "koya gabriel\norolu wumi\n"
        Customfile.write(new_file, content)
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
        remove(self.filepath + "test.txt")

    def test_load_people_with_complete_file_content(self):
        """
        tests the load_people method if it suceessfully load_rooms
        data if a file with complete file content is passed as
        argument
        """
        new_file = open(self.filepath + "test.txt", "w")
        content = "koya gabriel staff\norolu wumi fellow\najayi tope fellow y\n"
        Customfile.write(new_file, content)
        new_file.close()
        self.assertFalse(Person.get_list_of_persons())
        Dojo.load_people("test")
        self.assertEqual(len(Person.get_list_of_persons()), 3)
        remove(self.filepath + "test.txt")

    def test_load_rooms_with_non_existing_filename(self):
        """
        test the load_rooms if it returns the appropriate error message
        when a non existing filename is passed as argument
        """
        Dojo.load_rooms("roomfile")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "No such file: roomfile.txt can't be found")

    def test_load_rooms_with_incomplete_file_content(self):
        """
        test the load_rooms method if it returns appropriate
        error message if the file being loaded contains lines with
        incomplete arguments
        """
        new_file = open(self.filepath + "test.txt", "w")
        content = "red\nlivingspace \n"
        Customfile.write(new_file, content)
        new_file.close()
        expected_output = [
            "Errors\n---------",
            "The following rooms couldn't be loaded"
            + " because of incomplete information\n",
            "red",
            "livingspace"
        ]
        Dojo.load_rooms("test")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "\n".join(expected_output))
        remove(self.filepath + "test.txt")

    def test_load_rooms_with_complete_file_content(self):
        """
        tests the load_rooms method if it suceessfully load_rooms
        data if a file with complete file content is passed as
        argument
        """
        new_file = open(self.filepath + "test.txt", "w")
        content = "office red green\nlivingspace kfc biggs\n"
        Customfile.write(new_file, content)
        new_file.close()
        self.assertFalse(Room.get_room_list())
        Dojo.load_rooms("test")
        self.assertEqual(len(Room.get_room_list()), 4)
        remove(self.filepath + "test.txt")

    def test_save_state_with_existing_database_name(self):
        """
        test the save_state method for a warning
        message if an already existing database name is
        inputed as value.
        """
        test_database = Database(self.database_path + "file.sqlite3")
        expected_output = "Database with the name {} already exist. "\
            + "You can either specify another name or override the " \
            + "existing database.\n"\
            + "To override specify the [override] command"
        new_database = Dojo.save_state("file")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_output.format("file.db"))
        remove(self.database_path + "file.db")

    def test_save_state_with_new_database_name(self):
        """
        test the save_state method whether it successfully create
        a new database if a non-existing database name is
        passed as value.
        """
        initial_database = Database(self.database_path + "file.sqlite3")
        initial_size = Customfile.get_status_info(
            self.database_path, "file.sqlite3").st_size
        remove(self.database_path + "file.db")
        Dojo.create_room("office", ["orange", "red"])
        Dojo.add_person("koya", "gabriel", "staff")
        Dojo.save_state("file")
        final_size = Customfile.get_status_info(
            self.database_path, "file.sqlite3").st_size
        self.assertNotEqual(initial_size, final_size)
        remove(self.database_path + "file.sqlite3")

    def test_load_state_with_non_existing_database_name(self):
        """ tests load_state method if it returns appropriate
        error message if a non existing filename is passed as
        argument """
        Dojo.load_state("test")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output,
                         "Database with the name test.db does not exist.")

    def test_load_state_with_existing_database_name(self):
        """ tests load_state method if it properly loads data
        if an existing filename is passed as argument """
        Dojo.create_room("office", ["orange", "red"])
        Dojo.add_person("koya", "gabriel", "staff")
        Dojo.create_room("livingspace", ["kfc", "biggs"])
        Dojo.add_person("Njirap", "Perci", "fellow")
        Dojo.save_state("file")
        Room.list_of_rooms = []
        Person.list_of_persons = []
        self.assertFalse(Room.get_room_list())
        self.assertFalse(Person.get_list_of_persons())
        Dojo.load_state("file")
        self.assertEqual(len(Room.get_room_list()), 4)
        self.assertEqual(len(Person.get_list_of_persons()), 2)

    def test_rename_room_with_non_existing_room(self):
        """ test the rename_room method if it returns
        appropriate error message if a non existing room
        is tried to rename """
        Dojo.rename_room("blue", "red")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output,
                         ("Room {} doesn't exist, therefore changes couldn't "
                          + "be made.").format("blue"))

    def test_rename_room_with_existing_room_name(self):
        """ test rename_room method if it returns appropriate
        error message when trying to use a name that already
        exist """
        Dojo.create_room("office", ["red"])
        Dojo.create_room("office", ["blue"])
        Dojo.rename_room("red", "blue")
        output = sys.stdout.getvalue().split("\n")[-2]
        self.assertEqual(output,
                         "Room {} already exist. Please choose another name"
                         .format("blue"))

    def test_rename_room(self):
        """ test rename_room method if it properly renames
        an existing room to a new name passed as arguments """
        Dojo.create_room("office", ["red"])
        self.assertTrue(Room.exists("red"))
        self.assertEqual(Room.get_room_list()[0].name, "Red")
        Dojo.rename_room("red", "blue")
        self.assertFalse(Room.exists("red"))
        self.assertTrue(Room.exists("blue"))
        self.assertEqual(Room.get_room_list()[0].name, "Blue")
