from app.utilities import Utilities
from os import path

class File():
	"""docstring for File"""
	def create_file(filename):
		try:
			Utilities.check_format_validity(filename)
		except:
			raise Exception("{} is not a valid file name".format(filename))

		filepath = path.dirname(path.abspath(__file__)) + "\\text documents\\"
		filename = "{}.txt".format(filename)
		
		if File.exist(filepath, filename):
			raise Exception("{} already exist".format(filename))
		else:
			return open(filepath + filename, "w")

	def write(file, content):
		file.write(content)


	def exist(filepath, filename):
		if path.isfile(filepath + filename):
			return True

		return False
