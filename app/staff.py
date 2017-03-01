from os import sys, path

from app.person import Person


class Staff(Person):
    """docstring for Staff"""
    staff_list = []
    unallocated_staff = []

    def __init__(self, staff_id,  lname, fname):
        super(Staff, self).__init__(staff_id, lname, fname)
        self.__category = "staff"

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, new_category):
        self.__category = new_category.lower()

    @classmethod
    def add_to_staff_list(cls, staff):
        cls.staff_list.append(staff)

    @classmethod
    def get_staff_list(cls):
        return cls.staff_list

    @classmethod
    def add_unallocated_staff(cls, staff):
        cls.unallocated_staff.append(staff)

    @classmethod
    def get_unallocated_staff(cls):
        return cls.unallocated_staff

    @classmethod
    def remove_from_unallocated_staff_list(cls, staff):
        cls.unallocated_staff.remove(staff)
