import random

from app.errors import WrongFormatException


class Utilities():
	"""
	this class implements functionalities used for input validity check
	and unique number generation
	"""

	@classmethod
	def check_format_validity(cls, parameters):
		# checks the format validity of a string
		for param in parameters:
			if (param.strip()
					in ["\"\"", "\"", "'", "''", ".", "-", "?", "_", ","]):
				raise WrongFormatException("Invalid name format")

		return True

	@classmethod
	def generate_person_id(cls, id_list):
		# selects a unique number from a sequence of numbers
		return random.choice(list(set(range(1, 2000)).difference(id_list)))
