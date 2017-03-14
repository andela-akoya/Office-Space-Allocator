import random
from os import path, sys

from app.errors import *
from app.fellow import Fellow
from app.room import Room
from app.utilities import Utilities


class LivingSpace(Room):
    """
    This class implements livingspace specific functionalities and inherits
    from the Room class.
    """

    list_of_livingspace = []  # holds all the livingspace created

    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.__room_type = "livingspace"
        self.__maximum_capacity = 4

    @property
    def room_type(self):
        # This method returns the room type property value
        return self.__room_type

    @room_type.setter
    def room_type(self, new_type):
        # This method sets the room type property value
        self.__room_type = new_type

    @property
    def maximum_capacity(self):
        # This method returns the maximum capacity property value of a
        # livingspace.
        return self.__maximum_capacity

    @maximum_capacity.setter
    def maximum_capacity(self, new_capacity):
        # This method sets the maximum capacity property value of a
        # livingspace.
        self.__maximum_capacity = new_capacity

    def check_availability(self):
        return len(self.room_members) != self.maximum_capacity

    @classmethod
    def create_livingspace(cls, room_names):
        # This method creates a single or multiple livingspace
        # object based on argument  passed as room names.
        output = []
        for name in room_names:
            try:
                # checks the format validity of the room name argument
                Utilities.check_format_validity([name])
                if not Room.exists(name):
                    new_livingspace = LivingSpace(name)
                    cls.add_to_livingspace_list(new_livingspace)
                    Room.add_room(new_livingspace)
                    output.append(new_livingspace)
                    print(("A LivingSpace called {} has been "
                           + "successfully created.")\
                          .format(name.capitalize()))
                else:
                    print("A Room with the name {} already exist"
                          .format(name.capitalize()))
            except WrongFormatException as e:
                print("{} is not a valid livingspace name format"\
                      .format(name))

        return output

    @classmethod
    def add_to_livingspace_list(cls, livingspace):
        # This method adds a livingspace to the list of livingspace.
        cls.list_of_livingspace.append(livingspace)

    @classmethod
    def allocate_livingspace(cls, person, livingspace_name=None):
        # This method allocates an available livingspace to a person.
        livingspace = cls.get_livingspace(livingspace_name)\
            if livingspace_name else cls.get_random_livingspace()

        if livingspace:
            person.livingspace = livingspace
            livingspace.room_members = person
            person.wants_accomodation = True
            return("{p.surname} {p.firstname}has been allocated a "
                   + "livingspace {l.name}\n").format(p=person,l=livingspace)

        Fellow.add_unallocated_fellow(person, False, True)
        return("No available livingspace, {p.surname} {p.firstname} has been "
               + "placed on the livingspace waiting list\n").format(p=person)

    @classmethod
    def get_random_livingspace(cls):
        # this method returns a random livingspace from a list of
        # available livingspace.
        available_livingspaces = cls.get_available_livingspaces()
        if available_livingspaces:
            return random.choice(available_livingspaces)

    @classmethod
    def get_available_livingspaces(cls):
        # this method returns a list of all livingspace available for
        # allocation
        available_livingspaces = []
        for livingspace in cls.get_livingspace_list():
            if len(livingspace.room_members) != livingspace.maximum_capacity:
                available_livingspaces.append(livingspace)
        return available_livingspaces

    @classmethod
    def get_livingspace_list(cls):
        # this method returns a list of all the livingspace
        # that has been created.
        return cls.list_of_livingspace

    @classmethod
    def get_livingspace(cls, livingspace_name):
        # This method returns a particular livingspace based on the name
        # passed in as argument
        for livingspace in cls.list_of_livingspace:
            if livingspace.name == livingspace_name.capitalize():
                return livingspace

    @classmethod
    def reallocate_person(cls, person, livingspace):
        # this method reallocates a fellow to a new livingspace based on
        # the livingspace name passed in as argument.
        message = "{p.category} {p.surname} {p.firstname} has been " \
            + "successfully reallocated to {} {}"

        cls.check_eligiblity(person, livingspace)
        if not livingspace.check_availability():
            raise MaximumCapacityException(livingspace.name)

        if person in livingspace.room_members:
            raise ValueError(("{p.surname} {p.firstname} already belongs "
                          + "to room {}, therefore can't be "
                          + "reallocated to the same room")
                         .format(livingspace.name, p=person))

        if person.livingspace is None:
            Fellow.remove_from_unallocated_fellow_list(person, "livingspace")
        else:
            person.livingspace.remove_member(person)

        person.livingspace = livingspace
        livingspace.room_members = person
        print(message.format(livingspace.name, "livingspace", p=person))

    @classmethod
    def reset(cls):
        # Erases all the data in the office list.
        cls.list_of_livingspace = []

    @classmethod
    def check_eligiblity(cls, person, room):
        if (person.category == "staff"):
            raise EligibilityException(("Room {} is a livingspace and "
                                        + "can't be assigned to a staff")
                                       .format(room.name))
        elif not person.wants_accomodation:
            raise EligibilityException(("Fellow {p.surname} "
                                        + "{p.firstname} never "
                                        + "registered for accomodation "
                                        + "so can't be reallocated to a "
                                        + "a livingspace")
                                       .format(p=person))
