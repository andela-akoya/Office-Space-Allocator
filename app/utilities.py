import random

class Utilities():
	"""docstring for Utilities"""
	def __init__(self, arg):
		pass

	def check_format_validity(parameters):
		for param in parameters:
			if (param.strip() \
					in ["\"\"", "\"", "'", "''", ".", "-","?", "_", ","]):
				raise ValueError("Invalid name format")

		return True

	def generate_person_id(id_list): 
		return random.choice(list(set(range(1, 2)).difference(id_list)))
