import unittest

from app.dojo import Dojo
from app.fellow import Fellow
from app.person import Person
from app.staff import Staff


class TestPerson(unittest.TestCase):

    def tearDown(self):
        Person.list_of_persons = []
        Staff.staff_list = []
        Fellow.fellow_list = []
        Fellow.unallocated_fellows = {"office": [], "livingspace": []}
        Staff.unallocated_staff = []

    def test_the_id_property_setter(self):
        """  tests the id property setter method if it properly sets
        the id to any new id provided. """

        Dojo.add_person("Koya", "Gabriel", "Fellow")
        person, = Person.get_list_of_persons()
        initial_id = (person.uniqueId)
        person.uniqueId = 3000
        self.assertEqual(person.uniqueId, 3000)
        self.assertNotEqual(initial_id, person.uniqueId)

    def test_the_id_property_setter_with_invalid_format(self):
        """  tests the id property setter method if it returns appropriate
        error messages if an invalid id format is passed as
        argument """

        Dojo.add_person("Koya", "Gabriel", "Fellow")
        person, = Person.get_list_of_persons()
        with self.assertRaises(ValueError) as context:
            person.uniqueId = "hello"
            self.assertEqual("Only integers are acceptable format",
                             context.exception.message)
