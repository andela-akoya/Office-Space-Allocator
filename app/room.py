import random
from os import path, sys

from app.fellow import Fellow
from app.person import Person
from app.staff import Staff


class Room():

    list_of_rooms = []

    def __init__(self, room_name):
        self.__name = room_name.capitalize()
        self.__room_members = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_room_name):
        if new_room_name and isinstance(new_room_name, str):
            self.__name = new_room_name.capitalize()
        else:
            raise ValueError("Room name must be a string and can't be empty")

    @property
    def room_members(self):
        return self.__room_members

    @room_members.setter
    def room_members(self, person):
        if not isinstance(person, Person):
            raise ValueError(
                "Only a person, staff, or fellow instance can be added")
            return False
        self.__room_members.append(person)

    def remove_member(self, person):
        if not isinstance(person, Person):
            raise ValueError(
                "Only a person, staff, or fellow instance can be removed")
        self.__room_members.remove(person)

    @classmethod
    def add_room(cls, room):
        if not isinstance(room, Room):
            raise ValueError(
                "Only a room, office, or livingspace instance can be added")
        cls.list_of_rooms.append(room)

    @classmethod
    def get_random_room(cls, room_list):
        available_rooms = cls.get_available_rooms(room_list)
        return random.choice(available_rooms) if available_rooms else False

    @classmethod
    def get_available_rooms(cls, room_list):
        return [room for room in room_list
                if len(room.room_members) != room.maximum_capacity] \
            if room_list else []

    @classmethod
    def print_room_members(cls, room_name):
        name = room_name.capitalize()
        output = (["{:15} {}".format("Surname", "Firstname")] +
                  [("{:15} {} ".format(member.surname, member.firstname))
                   for member in [room.room_members for room in cls.list_of_rooms
                                  if room.name == name][0]]) \
            if name in [room.name for room in cls.list_of_rooms] \
            else "The room with the name {} does not exist".format(room_name)
        return "\n".join(output) if isinstance(output, list) else output

    @classmethod
    def get_total_number_of_rooms(cls):
        return len(cls.list_of_rooms)

    @classmethod
    def exists(cls, room_name):
        return room_name.capitalize() in [room.name for room in cls.list_of_rooms]

    @classmethod
    def get_room_list(cls):
        return cls.list_of_rooms

    @classmethod
    def get_allocations(cls):
        output = ""
        for room in cls.list_of_rooms:
            output += "{} Room\n".format(room.name)
            output += (len(room.name + " Room") * "-") + "\n"
            for member in room.room_members:
                output += "{m.surname} {m.firstname}, ".format(m=member)
            output += "\n"

        return output

    @classmethod
    def export_in_database_format(cls):
        return [(room.name, room.room_type) for room in cls.list_of_rooms]

    @classmethod
    def get_a_particular_room(cls, room_name):
        output = [room for room in cls.list_of_rooms if room.name ==
                  room_name.capitalize()]
        return output[0] if output \
            else "Room {} doesn't exist".format(room_name)
