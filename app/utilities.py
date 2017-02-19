import random

from app.errors import WrongFormatException


class Utilities():
	"""docstring for Utilities"""

	@classmethod
	def check_format_validity(cls, parameters):
		for param in parameters:
			if (param.strip()
					in ["\"\"", "\"", "'", "''", ".", "-", "?", "_", ","]):
				raise WrongFormatException("Invalid name format")

		return True

	@classmethod
	def generate_person_id(cls, id_list):
		return random.choice(list(set(range(1, 4)).difference(id_list)))
