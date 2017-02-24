import random
from os import sys, path

from app.room import Room
from app.fellow import Fellow
from app.utilities import Utilities
from app.errors import WrongFormatException

sys.path.append(path.dirname(path.dirname(
    path.dirname(path.abspath(__file__)))))


class LivingSpace(Room):
    """docstring for LivingSpace"""

    livingspace_list = {}

    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.type = "livingspace"
        self.maximum_capacity = 4

    def get_type(self):
        return self.type

    def set_type(self, new_type):
        self.type = new_type

    def get_maximum_capacity(self):
        return self.maximum_capacity

    def set_maximum_capacity(self, new_capacity):
        self.maximum_capacity = new_capacity

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
                print("' is not a valid office name format")

        return output

    @classmethod
    def add_to_livingspace_list(cls, livingspace):
        cls.livingspace_list[livingspace.name] = livingspace

    @classmethod
    def allocate_livingspace(cls, person):
        livingspace = cls.get_random_livingspace()
        if livingspace:
            person.set_assigned_livingspace(livingspace)
            livingspace.add_room_members(person)
            person.set_wants_accomodation = True
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
            if not livingspace.is_full:
                available_livingspaces.append(livingspace)
        return available_livingspaces

    @classmethod
    def get_livingspace_list(cls):
        return list(cls.livingspace_list.values())

    @classmethod
    def get_livingspace(cls, livingspace_name):
        return cls.livingspace_list[livingspace_name]

    @classmethod
    def reallocate_person(cls, person, livingspace_name):
        livingspace = cls.get_livingspace(livingspace_name)
        message = "{p.category} {p.surname} {p.firstname} has been " \
            + "successfully reallocated to {} {}"
        if person.get_wants_accomodation():
            if person.get_assigned_livingspace() is None:
                Fellow.remove_from_unallocated_fellow_list(
                    person, "livingspace")
            else:
                person.get_assigned_livingspace() \
                    .remove_member(person)
            person.set_assigned_livingspace(livingspace)
            livingspace.add_room_members(person)
            print(message
                  .format(livingspace_name, "livingspace", p=person))
        else:
            print(("Fellow {p.surname} "
                   + "{p.firstname} never "
                   + "registered for accomodation "
                   + "so can't be reallocated to a "
                   + "a livingspace")
                  .format(p=person))
