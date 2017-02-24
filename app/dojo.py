from os import sys, path

from app.office import Office
from app.livingspace import LivingSpace
from app.room import Room
from app.utilities import Utilities
from app.staff import Staff
from app.fellow import Fellow
from app.file import File
from app.person import Person
from app.errors import WrongFormatException

sys.path.append(path.dirname(path.dirname(
    path.dirname(path.abspath(__file__)))))


class Dojo(object):
    """docstring for Dojo"""

    @classmethod
    def create_room(cls, room_type, room_names):
        type_of_room = room_type.strip().lower()
        if type_of_room == "office":
            return Office.create_office(room_names)
        elif type_of_room == "livingspace":
            return LivingSpace.create_livingspace(room_names)
        else:
            print("Invalid type of room")

    @classmethod
    def add_person(cls, surname, firstname, category, wants_accomodation=None):
        type_of_person = category.strip().lower()
        try:
            if type_of_person == "staff":
                new_staff = Staff(surname, firstname)
                if new_staff:
                    print(("Staff {ns.surname} {ns.firstname} has been"
                           + " successfully added").format(ns=new_staff))
                    Staff.add_to_staff_list(new_staff)
                    Person.add_to_map(new_staff)
                    cls.allocate_room(new_staff)

            elif type_of_person == "fellow":
                new_fellow = Fellow(surname, firstname, True) \
                    if wants_accomodation in ['y', 'Y'] \
                    else Fellow(surname, firstname)
                if new_fellow:
                    print(("Fellow {nf.surname} {nf.firstname} has been"
                           + " successfully added").format(nf=new_fellow))
                    Fellow.add_to_fellow_list(new_fellow)
                    Person.add_to_map(new_fellow)
                    cls.allocate_room(new_fellow, wants_accomodation)
            else:
                print("Invalid type of person")

        except WrongFormatException as e:
            print(e)

    @classmethod
    def allocate_room(cls, person, wants_accomodation=None):
        if(not(wants_accomodation in ['y', 'Y'])):
            print(Office.allocate_office(person))
        else:
            print("{}{}".format(Office.allocate_office(person),
                                LivingSpace.allocate_livingspace(person)))

    @classmethod
    def print_room(cls, room_name):
        print("\n{}".format(Room.print_room_members(room_name)))

    @classmethod
    def print_allocations(cls, filename):
        allocations = Room.get_allocations()
        if filename is None:
            print(allocations)
        else:
            try:
                new_file = File.create_file(filename)
                File.write(new_file, allocations)
            except FileExistsError as e:
                print(e)

    @classmethod
    def print_unallocated(cls, filename):
        unallocated = Person \
            .get_unallocated(Staff.get_unallocated_staff(),
                             Fellow.get_unallocated_fellows())
        if filename is None:
            print(unallocated)
        else:
            try:
                new_file = File.create_file(filename)
                File.write(new_file, unallocated)
            except FileExistsError as e:
                print(e)

    @classmethod
    def reallocate_person(cls, identifier, room_name):
        person_id = None
        try:
            person_id = int(identifier)
            if Person.exist(person_id):
                person = Person.id_map[person_id]
                if Room.exists(room_name):
                    room = Room.get_room_list()[room_name]
                    if not room.is_full:
                        if not (person in room.get_room_members()):
                            if isinstance(person, Staff):
                                if room.get_type() == "office":
                                    Office.reallocate_person(person, room_name)
                                else:
                                    print(("Room {} is a livingspace and  "
                                           + "can't be assigned to a staff")
                                          .format(room_name))
                            else:
                                if room.get_type() == "office":
                                    Office.reallocate_person(person, room_name)
                                else:
                                    LivingSpace.reallocate_person(person,
                                                                  room_name)
                        else:
                            print(("{p.surname} {p.firstname} already belongs "
                                   + "to room {}, therefore can't be "
                                   + "reallocated to the same room")
                                  .format(room_name, p=person))
                    else:
                        print("Room {} is filled up, please input another room"
                              .format(room_name))
                else:
                    print("Room {} doesn't exist".format(room_name))

            else:
                print("Person with the id {} doesn't exist".format(person_id))
        except ValueError:
            print("Wrong id format. id must be a number")

    @classmethod
    def load_people(cls, filename):
        error_messages = []
        error_messages.append("Errors\n---------")
        error_messages.append("The following people couldn't be loaded "
                              + "because of incomplete information\n")
        try:
            file_to_be_loaded = File.open_file(filename)
            with file_to_be_loaded as data_file:
                for line in data_file:
                    data = line.strip().split(" ")
                    if len(data) > 2:
                        surname = data[0]
                        firstname = data[1]
                        category = data[2]
                        wants_accomodation = data[4] or None
                        cls.add_person(surname, firstname,
                                       staff, wants_accomodation)
                    else:
                        error_messages.append(" ".join(data))
                data_file.close()
                print("\n".join(error_messages))
        except FileNotFoundError as e:
            print(e)

    @classmethod
    def get_total_rooms(cls):
        return Room.get_total_number_of_rooms()
