class WrongFormatException(Exception):

	def __init__(self, arg):
		self.error = arg

	def __str__(self):
		return self.error
