from os import path, sys

from app.errors import WrongFormatException
from app.utilities import Utilities


class Person():
    """docstring for Person"""

    list_of_persons = []

    def __init__(self, person_id, lname, fname):
        try:
            Utilities.check_format_validity([lname, fname])
        except WrongFormatException:
            raise WrongFormatException(
                "Firstname or Lastname is not a valid name format")

        self.__id = person_id or Utilities.generate_person_id(
            Person.get_id_list())
        self.__surname = lname.capitalize()
        self.__firstname = fname.capitalize()
        self.__office = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        self.__id = new_id

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, new_surname):
        self.__surname = new_surname.capitalize()

    @property
    def firstname(self):
        return self.__firstname

    @firstname.setter
    def firstname(self, new_firstname):
        self.__firstname = new_firstname.capitalize()

    @property
    def office(self):
        return self.__office

    @office.setter
    def office(self, office):
        self.__office = office

    @property
    def livingspace(self):
        return None

    @property
    def wants_accomodation(self):
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
    def add_to_person_list(cls, person):
        cls.list_of_persons.append(person)

    @classmethod
    def get_id_list(cls):
        return [person.id for person in cls.list_of_persons]

    @classmethod
    def get_list_of_persons(cls):
        return cls.list_of_persons

    @classmethod
    def exist(cls, person_identifier):
        return person_identifier in [person.id for person in cls.list_of_persons]

    @classmethod
    def export_in_database_format(cls):
        output = []
        for person in cls.list_of_persons:
            office = "None" \
                if not person.office \
                else person.office.name
            livingspace = "None" \
                if not person.livingspace \
                else person.livingspace.name
            output.append(
                (person.id, person.surname, person.firstname,
                 person.category, office, livingspace,
                 person.wants_accomodation)
            )

        return output
