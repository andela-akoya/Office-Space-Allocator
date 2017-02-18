from os import sys, path

from app.utilities import Utilities

sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))


class Person():
	"""docstring for Person"""

	id_map = {}

	def __init__(self, lname, fname):

		if Utilities.check_format_validity([lname, fname]):
			self.id = Utilities.generate_person_id(Person.get_id_list())
			self.surname = lname.capitalize()
			self.firstname = fname.capitalize()
			self.office = None

		else:
			raise Exception

	def set_assigned_office(self, office):
		self.office = office

	def get_assigned_office(self):
		return self.office

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
	def add_to_map(cls, person):
		cls.id_map[person.id] = person

	@classmethod
	def get_id_list(cls):
		return list(cls.id_map.keys())

	@classmethod
	def exist(cls, person_identifier):
		if not person_identifier in cls.get_id_list():
			raise Exception("Person doesn't exist")
		return True
