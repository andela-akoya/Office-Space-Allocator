from os import path, sys

from app.person import Person


class Fellow(Person):
    """docstring for Fellow"""

    fellow_list = []
    unallocated_fellows = {"office": [], "livingspace": []}

    def __init__(self, fellow_id, lname, fname, wants_accomodation=False):
        super(Fellow, self).__init__(fellow_id, lname, fname)
        self.__category = "fellow"
        self.__livingspace = None
        self.__wants_accomodation = wants_accomodation

    @property
    def livingspace(self):
        return self.__livingspace

    @livingspace.setter
    def livingspace(self, livingspace):
        self.__livingspace = livingspace

    @property
    def wants_accomodation(self):
        return self.__wants_accomodation

    @wants_accomodation.setter
    def wants_accomodation(self, param):
        self.__wants_accomodation = param

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, new_category):
        self.__category = new_category.lower()

    @classmethod
    def add_to_fellow_list(cls, fellow):
        cls.fellow_list.append(fellow)

    @classmethod
    def get_fellow_list(cls):
        return cls.fellow_list

    @classmethod
    def add_unallocated_fellow(cls, fellow, office=False, livingspace=False):
        if office and livingspace:
            cls.unallocated_fellows["office"].append(fellow)
            cls.unallocated_fellows["livingspace"].append(fellow)
        elif office:
            cls.unallocated_fellows["office"].append(fellow)
        else:
            cls.unallocated_fellows["livingspace"].append(fellow)

    @classmethod
    def get_unallocated_fellows(cls):
        return cls.unallocated_fellows

    @classmethod
    def remove_from_unallocated_fellow_list(cls, fellow, room_type):
        cls.unallocated_fellows[room_type].remove(fellow)
