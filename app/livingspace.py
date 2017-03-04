import random
from os import path, sys

from app.errors import WrongFormatException
from app.fellow import Fellow
from app.room import Room
from app.utilities import Utilities


class LivingSpace(Room):
    """docstring for LivingSpace"""

    list_of_livingspace = []

    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.__room_type = "livingspace"
        self.__maximum_capacity = 4

    @property
    def room_type(self):
        return self.__room_type

    @room_type.setter
    def room_type(self, new_type):
        self.__room_type = new_type

    @property
    def maximum_capacity(self):
        return self.__maximum_capacity

    @maximum_capacity.setter
    def maximum_capacity(self, new_capacity):
        self.__maximum_capacity = new_capacity

    @classmethod
    def create_livingspace(cls, room_names):
        output = []
        for name in room_names:
            try:
                Utilities.check_format_validity([name])
                if not Room.exists(name):
                    new_livingspace = LivingSpace(name)
                    cls.add_to_livingspace_list(new_livingspace)
                    Room.add_room(new_livingspace)
                    output.append(new_livingspace)
                    print("A LivingSpace called {} has been successfully created"
                          .format(name.capitalize()))
                else:
                    print("A Room with the name {} already exist"
                          .format(name.capitalize()))
            except WrongFormatException as e:
                print("{} is not a valid office name format".format(name))

        return output

    @classmethod
    def add_to_livingspace_list(cls, livingspace):
        cls.list_of_livingspace.append(livingspace)

    @classmethod
    def allocate_livingspace(cls, person, livingspace_name=None):
        livingspace = cls.get_livingspace(livingspace_name) \
            if livingspace_name else cls.get_random_livingspace()
        if livingspace:
            person.livingspace = livingspace
            livingspace.room_members = person
            person.wants_accomodation = True
            return("{p.surname} has been allocated a livingspace {l.name}\n"
                   .format(p=person, l=livingspace))
        Fellow.add_unallocated_fellow(person, False, True)
        return(("No available livingspace, {p.surname} has been placed on the"
                + " livingspace waiting list\n").format(p=person))

    @classmethod
    def get_random_livingspace(cls):
        available_livingspaces = cls.get_available_livingspaces()
        if available_livingspaces:
            return random.choice(available_livingspaces)
        return False

    @classmethod
    def get_available_livingspaces(cls):
        available_livingspaces = []
        for livingspace in cls.get_livingspace_list():
            if len(livingspace.room_members) != livingspace.maximum_capacity:
                available_livingspaces.append(livingspace)
        return available_livingspaces

    @classmethod
    def get_livingspace_list(cls):
        return cls.list_of_livingspace

    @classmethod
    def get_livingspace(cls, livingspace_name):
        return [livingspace for livingspace in cls.list_of_livingspace
                if livingspace.name == livingspace_name][0]

    @classmethod
    def reallocate_person(cls, person, livingspace_name):
        livingspace = cls.get_livingspace(livingspace_name)
        message = "{p.category} {p.surname} {p.firstname} has been " \
            + "successfully reallocated to {} {}"
        if person.wants_accomodation:
            if person.livingspace is None:
                Fellow.remove_from_unallocated_fellow_list(
                    person, "livingspace")
            else:
                person.livingspace.remove_member(person)
            person.livingspace = livingspace
            livingspace.room_members = person
            print(message
                  .format(livingspace_name, "livingspace", p=person))
        else:
            print(("Fellow {p.surname} "
                   + "{p.firstname} never "
                   + "registered for accomodation "
                   + "so can't be reallocated to a "
                   + "a livingspace")
                  .format(p=person))
