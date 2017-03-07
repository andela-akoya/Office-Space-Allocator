from os import path, stat

from app.errors import WrongFormatException
from app.utilities import Utilities


class Customfile():
	"""This class holds the properties and methods of a customfile
	model """

	@classmethod
	def create_file(cls, filename):
		""" this method creates a new file using the filename
		passed as argument """
		try:
			Utilities.check_format_validity(filename)
		except:
			raise WrongFormatException(
				"{} is not a valid file name".format(filename))

		filepath = path.dirname(path.abspath(__file__)) + "/data/documents/"

		filename = "{}.txt".format(filename)
		if cls.exist(filepath, filename):
			raise FileExistsError("{} already exist".format(filename))
		else:
			return open(filepath + filename, "w")

	@classmethod
	def open_file(cls, filename):
		""" This method opens a file for editing """
		filepath = path.dirname(path.abspath(__file__)) + "/data/documents/"
		filename = "{}.txt".format(filename)
		if not cls.exist(filepath, filename):
			raise FileNotFoundError(
				"No such file: {} can't be found".format(filename))
		else:
			return open(filepath + filename, "r")

	@classmethod
	def write(cls, new_file, content):
		""" This method writes the content passed as argument to a file """
		new_file.write(content)

	@classmethod
	def exist(cls, filepath, filename):
		""" This method checks if a file exists """
		return path.isfile(filepath + filename)

	@classmethod
	def get_status_info(cls, filepath, filename):
		""" This method returns status information of a file """
		return stat(filepath + filename)
