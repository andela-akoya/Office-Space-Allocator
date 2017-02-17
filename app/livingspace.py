from os import sys, path
from app.room import Room
from app.fellow import Fellow
from app.utilities import Utilities
sys.path.append(path.dirname(path.dirname(
	path.dirname(path.abspath(__file__)))))


class LivingSpace(Room):
	"""docstring for LivingSpace"""

	livingspace_list = {}

	def __init__(self, name):
		super(LivingSpace, self).__init__(name)
		self.type = "livingspace"
		self.maximum_capacity = 6

	def create_livingspace(room_names):
		output = []
		for name in room_names:
			try:
				if (Utilities.check_format_validity([name])
						and not Room.exists(name)):
					new_livingspace = LivingSpace(name)
					LivingSpace.add_to_livingspace_list(new_livingspace)
					Room.add_room(new_livingspace)
					output.append(new_livingspace)
					print("A LivingSpace called {} has been successfully created"
						  .format(name.capitalize()))
				else:
					print("A Room with the name {} already exist"
						  .format(name.capitalize()))
			except Exception as e:
				print(e)

		return output

	def add_to_livingspace_list(livingspace):
		LivingSpace.livingspace_list[livingspace.name] = livingspace

	def exist(livingspace_name):
		if livingspace_name.capitalize() in list(LivingSpace
												 .livingspace_list.keys()):
			raise Exception("A livingspace with the name {} already exist"
							.format(livingspace_name))

		return True

	def allocate_livingspace(person):
		livingspace = LivingSpace.get_random_livingspace()
		if livingspace:
			person.set_assigned_livingspace(livingspace)
			livingspace.add_room_members(person)
			person.set_wants_accomodation = True
			return("{p.surname} has been allocated a livingspace {l.name}\n"
				   .format(p=person, l=livingspace))
		Fellow.add_unallocated_fellow(person, False, True)
		return(("No available livingspace, {p.surname} has been placed on the"
				+ " livingspace waiting list\n").format(p=person))

	def get_random_livingspace():
		available_livingspaces = LivingSpace.get_available_livingspaces()
		if available_livingspaces:
			return random.choice(available_livingspaces)
		return False

	def get_available_livingspaces():
		available_livingspaces = []
		for livingspace in LivingSpace.get_livingspace_list():
			if not livingspace.is_full:
				available_livingspaces.append(livingspace)
		return available_livingspaces

	def get_livingspace_list():
		return list(LivingSpace.livingspace_list.values())
