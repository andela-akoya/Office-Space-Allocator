from os import sys, path

from app.utilities import Utilities
from app.errors import WrongFormatException


class Person():
    """docstring for Person"""

    id_map = {}

    def __init__(self, person_id, lname, fname):
        try:
            Utilities.check_format_validity([lname, fname])
        except WrongFormatException:
            raise WrongFormatException(
                "Firstname or Lastname is not a valid name format")

        self.id = person_id or Utilities.generate_person_id(
            Person.get_id_list())
        self.surname = lname.capitalize()
        self.firstname = fname.capitalize()
        self.office = None

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id

    def get_surname(self):
        return self.surname

    def set_surname(self, new_surname):
        self.surname = new_surname.capitalize()

    def get_firstname(self):
        return self.firstname

    def set_firstname(self, new_firstname):
        self.firstname = new_firstname.capitalize()

    def set_assigned_office(self, office):
        self.office = office

    def get_assigned_office(self):
        return self.office

    def get_assigned_livingspace(self):
        return None

    def get_wants_accomodation(self):
        return False

    @classmethod
    def get_unallocated(cls, unallocated_staff_list, unallocated_fellow_list):
        output = []
        output.append("Unallocated List \n---------------------\n")
        serial_no = 0
        for staff in unallocated_staff_list:
            serial_no += 1
            output.append(("{}. Staff {s.surname} {s.firstname}\n")
                          .format(serial_no, s=staff))

        for fellow in unallocated_fellow_list["office"]:
            serial_no += 1
            if fellow in unallocated_fellow_list["livingspace"]:
                output.append(("{}. Fellow {f.surname} {f.firstname}"
                               + " (Office $ Livingspace)\n")
                              .format(serial_no, f=fellow))
            else:
                output.append(("{}. Fellow {f.surname} {f.firstname} "
                               + "(Office)\n").format(serial_no, f=fellow))

        for fellow in unallocated_fellow_list["livingspace"]:

            if not fellow in unallocated_fellow_list["office"]:
                serial_no += 1
                output.append(("{}. Fellow {f.surname} {f.firstname} "
                               + "(Livingspace)\n").format(serial_no, f=fellow))

        return "\n".join(output)

    @classmethod
    def add_to_map(cls, person):
        cls.id_map[person.id] = person

    @classmethod
    def get_id_list(cls):
        return list(cls.id_map.keys())

    @classmethod
    def exist(cls, person_identifier):
        if not person_identifier in cls.get_id_list():
            return False
        return True

    @classmethod
    def export_in_database_format(cls):
        output = []
        for person in cls.id_map.values():
            office = "None" \
                if not person.get_assigned_office() \
                else person.get_assigned_office().get_room_name()
            livingspace = "None" \
                if not person.get_assigned_livingspace() \
                else person.get_assigned_livingspace().get_room_name()
            output.append(
                (person.get_id(), person.get_surname(), person.get_firstname(),
                 person.get_category(), office, livingspace,
                 person.get_wants_accomodation())
            )

        return output
