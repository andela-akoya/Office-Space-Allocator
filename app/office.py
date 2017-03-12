import random
from os import path, sys

from app.errors import MaximumCapacityException, WrongFormatException
from app.fellow import Fellow
from app.room import Room
from app.staff import Staff
from app.utilities import Utilities


class Office(Room):
    """This class holds the properties and methods of an office model"""
    list_of_offices = []

    def __init__(self, name):
        super(Office, self).__init__(name)
        self.__room_type = "office"
        self.__maximum_capacity = 6

    @property
    def room_type(self):
        """ returns the value of the room_type property """
        return self.__room_type

    @room_type.setter
    def room_type(self, new_type):
        """ this method sets the value of the room_type property """
        self.__room_type = new_type

    @property
    def maximum_capacity(self):
        """ this method returns the value of the maximum_capacity property """
        return self.__maximum_capacity

    @maximum_capacity.setter
    def maximum_capacity(self, new_capacity):
        """ sets the value of the maximum_capacity property """
        self.__maximum_capacity = new_capacity

    def check_availability(self):
        return len(self.room_members) != self.maximum_capacity

    @classmethod
    def create_office(cls, room_names):
        """ creates an office object """
        output = []
        for name in room_names:
            try:
                Utilities.check_format_validity([name])
                if not Room.exists(name):
                    new_office = Office(name)
                    cls.add_to_office_list(new_office)
                    Room.add_room(new_office)
                    output.append(new_office)
                    print("An Office called {} has been successfully created."
                          .format(name.capitalize()))
                else:
                    print("A Room with the name {} already exist"
                          .format(name.capitalize()))
            except WrongFormatException as e:
                print("{} is not a valid office name format".format(name))
        return output

    @classmethod
    def add_to_office_list(cls, office_instance):
        """ adds an office to the list of offices """
        cls.list_of_offices.append(office_instance)

    @classmethod
    def allocate_office(cls, person, office_name=None):
        """ Allocates a random office to a person """
        office = Office.get_office(office_name) \
            if office_name else cls.get_random_office()
        if office:
            person.office = office
            office.room_members = person
            return(("{p.surname} {p.firstname} has been allocated the office "
                    + " {o.name}\n").format(p=person, o=office))
        Staff.add_unallocated_staff(person) if isinstance(person, Staff) \
            else Fellow.add_unallocated_fellow(person, True)
        return("No available office, {p.surname} {p.firstname} has been "
               + "placed on the office waiting list.\n").format(p=person)

    @classmethod
    def get_random_office(cls):
        """ returns a random office from a list of available offices """
        available_offices = cls.get_available_offices()
        if available_offices:
            return random.choice(available_offices)

    @classmethod
    def get_available_offices(cls):
        """ returns a list of offices that haven't exceeded maximum capacity """
        available_offices = []
        for office in cls.get_office_list():
            if len(office.room_members) != office.maximum_capacity:
                available_offices.append(office)
        return available_offices

    @classmethod
    def get_office_list(cls):
        """ returns a list conttaining all offices """
        return cls.list_of_offices

    @classmethod
    def get_office(cls, office_name):
        """ returns a particular office from the list of offices
        based on the office_name passed as argument """
        for office in cls.list_of_offices:
            if office.name == office_name.capitalize():
                return office

    @classmethod
    def reallocate_person(cls, person, office):
        """ reallocates a person to another office specified by the
        office_name argument passed in """
        message = "{p.category} {p.surname} {p.firstname} has been " \
            + "successfully reallocated to {} {}"

        if not office.check_availability():
            raise MaximumCapacityException(office.name)

        if person.office is None:
            Staff.remove_from_unallocated_staff_list(person)
        else:
            person.office.remove_member(person)

        person.office = office
        office.room_members = person
        print(message.format(office.name, "office", p=person))

    @classmethod
    def reset(cls):
        """ Erases all the data in the office list """
        cls.list_of_offices = []
