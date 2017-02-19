from os import path

from app.utilities import Utilities
from app.errors import WrongFormatException


class File():
	"""docstring for File"""

	@classmethod
	def create_file(cls, filename):
		try:
			Utilities.check_format_validity(filename)
		except:
			raise WrongFormatException(
				"{} is not a valid file name".format(filename))

		filepath = path.dirname(path.abspath(__file__)) \
			+ "\\text documents\\"

		filename = "{}.txt".format(filename)
		if File.exist(filepath, filename):
			raise FileExistsError("{} already exist".format(filename))
		else:
			return open(filepath + filename, "w")

	@classmethod
	def write(cls, new_file, content):
		new_file.write(content)

	@classmethod
	def exist(cls, filepath, filename):
		if path.isfile(filepath + filename):
			return True

		return False
