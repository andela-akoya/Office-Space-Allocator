from os import sys, path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
import random
from app.fellow import Fellow
from app.staff import Staff
from app.person import Person

class Room():
	
	total_number_of_rooms = 0
	room_list = {}

	def __init__(self, name):
		self.name = name
		self.is_full = False
		self.room_members = []
		Room.total_number_of_rooms += 1

	def add_room(room):
		Room.room_list[room.name] = room

	def allocate_room(person, office_list, livingspace_list = None ):
		output = []
		random_office = Room.get_random_room(office_list)

		if livingspace_list != None:
			output.append("Fellow {p.surname} {p.firstname} " \
							+ "has been successfully added." \
							.format(p=person))

			random_livingspace = Room.get_random_room(livingspace_list)

			if random_office and random_livingspace:
				person.set_assigned_office(random_office)
				person.set_assigned_livingspace(random_livingspace)
				random_office.add_room_members(person)
				random_livingspace.add_room_members(person)
				output.append(("{p.surname} has been allocated "  \
								+ "the office {o.name}"  \
								+ "\n{p.surname} has been allocated " \
								+ "the livingspace {l.name}") \
								.format(p=person, o=random_office, \
										l=random_livingspace))
			elif random_office:
				person.set_assigned_office(random_office)
				random_office.add_room_members(person)
				Fellow.add_unallocated_fellow(person, False, True)
				output.append(("{p.surname} has been allocated " \
								+"the office {o.name}" \
								+ "\nNo available livingspace, " \
								+"{p.surname} has been placed on the" \
								+ " livingspace waiting list") \
								.format(p=person, o=random_office))

			elif random_livingspace:
				person.set_assigned_livingspace(random_livingspace)
				random_livingspace.add_room_members(person)
				Fellow.add_unallocated_fellow(person, True, False)
				output.append(("{p.surname} has been allocated " \
								+"the livingspace {l.name}" \
								+ "\nNo available office, " \
								+ "{p.surname} has been placed on the" \
								+ " office waiting list")
								.format(p=person, l=random_livingspace))

			else:
				Fellow.add_unallocated_fellow(person, True, True)
				output.append(("No available room. " \
								+"All the rooms are occupied " \
								+ "\n{p.surname} has been placed " \
								+"on the waiting list") \
								.format(p=person))
		else:
			output.append("{0} {p.surname} {p.firstname} has been " \ 
							+" successfully added."\
							.format(person.category.capitalize(), p=person))

			if random_office:
				person.set_assigned_office(random_office)
				random_office.add_room_members([person])
				output.append("{p.surname} has been allocated" \
								+" the office {o.name}" \
								.format(p=person, o=random_office) )
			else:
				Staff.add_unallocated_staff(person) \
				if isinstance(person, Staff)  \
				else Fellow.add_unallocated_fellow(person, True, False)

				output.append(("No available room. " \ 
								+"All the rooms are occupied " \
								+ "\n{p.surname} has been placed on " \ 
								+"the office waiting list") \
								.format(p=person))

		return("\n".join(output))

	def get_random_room(room_list):
		available_rooms = Room.get_available_rooms(room_list)
		if available_rooms:
			return random.choice(available_rooms)
		
		return False

	def get_available_rooms(room_list):
		available_rooms = []
		for room in room_list:
			if not room.is_full:
				available_rooms.append(room)

		return available_rooms

	def print_room_members(room_name):
		output = []
		if room_name in list(Room.room_list.keys()):
			output.append("{:15} {}".format("Surname", "Firstname"))
			for member in Room.room_list[room_name].room_members:
				output.append("{:15} {} " \
								.format(member.surname, member.firstname))

			return "\n".join(output)

		else:
			raise Exception("The room with the name {} does not exist" \
							.format(room_name))
