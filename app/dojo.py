from os import sys, path

from app.office import Office
from app.livingspace import LivingSpace
from app.room import Room
from app.utilities import Utilities
from app.staff import Staff
from app.fellow import Fellow
from app.customfile import Customfile
from app.person import Person
from app.errors import WrongFormatException
from app.database import Database


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
    def get_total_rooms(cls):
        return Room.get_total_number_of_rooms()

    @classmethod
    def add_person(cls, surname, firstname, category, wants_accomodation=None, person_id=None):
        type_of_person = category.strip().lower()
        try:
            if type_of_person == "staff":
                new_staff = Staff(person_id, surname, firstname)
                if new_staff:
                    print(("Staff {ns.surname} {ns.firstname} has been"
                           + " successfully added").format(ns=new_staff))
                    Staff.add_to_staff_list(new_staff)
                    Person.add_to_map(new_staff)
                    cls.allocate_room(new_staff)

            elif type_of_person == "fellow":
                new_fellow = Fellow(person_id, surname, firstname, True) \
                    if wants_accomodation in ['y', 'Y'] \
                    else Fellow(person_id, surname, firstname)
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
                new_file = Customfile.create_file(filename)
                Customfile.write(new_file, allocations)
            except FileExistsError as e:
                print(e)
            except WrongFormatException as e:
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
                new_file = Customfile.create_file(filename)
                Customfile.write(new_file, unallocated)
            except FileExistsError as e:
                print(e)

    @classmethod
    def reallocate_person(cls, identifier, room_name):
        try:
            person_id = int(identifier)
            if Person.exist(person_id):
                person = Person.id_map[person_id]
                if Room.exists(room_name):
                    room = Room.get_room_list()[room_name]
                    if not room.is_full:
                        if not (person in room.room_members):
                            if isinstance(person, Staff):
                                if room.room_type == "office":
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
        error_messages = \
            [
                "Errors\n---------",
                "The following people couldn't be loaded"
                + " because of incomplete information\n"
            ]
        try:
            file_to_be_loaded = Customfile.open_file(filename)
            with file_to_be_loaded as data_file:
                for entry in data_file:
                    data = entry.strip().split(" ")
                    if len(data) > 2:
                        surname, firstname, category = data[0:3]
                        wants_accomodation = data[3] \
                            if len(data) > 3 else None
                        cls.add_person(surname, firstname,
                                       category, wants_accomodation)
                    else:
                        error_messages.append(" ".join(data))
                        print("\n".join(error_messages))
                data_file.close()

        except FileNotFoundError as e:
            print(e)

    @classmethod
    def load_rooms(cls, filename):
        error_messages = \
            [
                "Errors\n---------",
                "The following rooms couldn't be loaded"
                + " because of incomplete information\n"
            ]
        try:
            file_to_be_loaded = Customfile.open_file(filename)
            with file_to_be_loaded as data_file:
                for entry in data_file:
                    data = entry.strip().split(" ")
                    if len(data) > 1:
                        room_type = data[0]
                        room_names = data[1:]
                        cls.create_room(room_type, room_names)
                    else:
                        error_messages.append(" ".join(data))
                        print("\n".join(error_messages))
                data_file.close()

        except FileNotFoundError as e:
            print(e)

    @classmethod
    def save_state(cls, database_name):
        database_path = path.dirname(path.abspath(__file__)) \
            + "\\data\\database\\"
        if database_name:
            if not Customfile.exist(database_path, database_name + ".db"):
                new_database = Database(database_path + database_name + ".db")
                new_database.save(
                    Room.export_in_database_format(),
                    Person.export_in_database_format()
                )
            else:
                error = "Database with the name {} already exist. "\
                    + "You can either specify another name or override the " \
                    + "existing database.\n"\
                    + "To override specify the [override] command "
                print(error.format(database_name + ".db"))
        else:
            pass

    @classmethod
    def load_state(cls, database_name):
        database_path = path.dirname(path.abspath(__file__)) \
            + "\\data\\database\\"
        if database_name:
            if Customfile.exist(database_path, database_name + ".db"):
                new_database = Database(database_path + database_name + ".db")
                new_database.load()
                print()
            else:
                error = "Database with the name {} does not exist."\
                    .format(database_name + ".db")
                print(error)
