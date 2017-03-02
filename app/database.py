import sqlite3
from os import sys, path

from app.office import Office
from app.livingspace import LivingSpace
from app.person import Person
from app.staff import Staff
from app.fellow import Fellow


class Database():

    def __init__(self, database_name):
        self.db_name = database_name
        self.db_conn = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_conn.cursor()

    def save(self, rooms, persons):
        self.create_tables()
        self.save_room(rooms)
        self.save_person(persons)

    def load(self):
        self.load_rooms()
        self.load_people()

    def create_tables(self):
        # creates the room table
        create_room_table_query = \
            """
        CREATE TABLE IF NOT EXISTS rooms
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name VARCHAR(30),
         type VARCHAR(10)
        )
        """
        create_person_table_query = \
            """
        CREATE TABLE IF NOT EXISTS person
        (id INTEGER PRIMARY KEY,
         surname VARCHAR(30),
         firstname VARCHAR(30),
         category VARCHAR(10),
         office VARCHAR(20),
         livingspace VARCHAR(20),
         accomodation BOOLEAN DEFAULT false
        )
        """
        self.db_cursor.execute(create_room_table_query)
        self.db_cursor.execute(create_person_table_query)
        self.db_conn.commit()

    def save_room(self, rooms):
        room_query = "INSERT INTO rooms (name, type) VALUES (?,?)"
        self.db_cursor.executemany(room_query, rooms)
        self.db_conn.commit()

    def save_person(self, persons):
        person_query = "INSERT INTO person VALUES (?,?,?,?,?,?,?)"
        self.db_cursor.executemany(person_query, persons)
        self.db_conn.commit()

    def load_rooms(self):
        for row in self.db_cursor.execute("SELECT * FROM rooms"):
            if row[2] == "office":
                Office.create_office([row[1]])
            else:
                LivingSpace.create_livingspace([row[1]])

    def load_people(self):
        for row in self.db_cursor.execute("SELECT * FROM person"):
            person_id, surname, firstname, category, office, livingspace, \
                accomodation = row
            if category.lower() == "staff":
                new_staff = Staff(person_id, surname, firstname)
                Staff.add_to_staff_list(new_staff)
                Person.add_to_person_list(new_staff)
                Office.allocate_office(new_staff, office) \
                    if not office == "None" \
                    else Staff.add_unallocated_staff(new_staff)
            else:
                new_fellow = Fellow(person_id, surname, firstname)
                Fellow.add_to_fellow_list(new_fellow)
                Person.add_to_person_list(new_fellow)
                Office.allocate_office(new_fellow, office) \
                    if not office == "None" \
                    else Fellow.add_unallocated_fellow(new_fellow, True)
                if accomodation == 1:
                    LivingSpace.allocate_livingspace(new_fellow, livingspace)\
                        if livingspace \
                        else Fellow.add_unallocated_fellow(new_fellow, False,
                                                           True)
