# Office-Space-Allocator

#### How should this be manually tested?
1. To run the app itself:
- Install `docopt module` using `pip install docopt==0.6.2` for python 2 and `pip3 install docopt==0.6.2` for python 3.
- After cloning the repo,  run `python main.py`.
- To create a room run `create_room type_of_room(office/livingspace) room_name`
  - e.g  `create_room office Orange`
- To create multiple rooms at once run `create_room type_of_room(office/livingspace) room_name1 room_name2 room_name3`
  - e.g  `create_room livingspace Orange Red Green White`
- To add a person to a room run `add_person surname firstname person_type(staff/fellow) wants_accomodation(y/n)
  - e.g `add_person John Doe staff y`
- To print members of a room run `print_room room_name`
  - e.g `print_room Orange`
- To print allocations to command line run `print_allocations`
  - e.g `print_allocations`
- To print allocations to a text file run `print_allocations --o=filename`
  - e.g `print_allocations --o=data`
- To print unallocated to command line run `print_allocations`
  - e.g `print_unallocated`
- To print unallocated to a text file run `print_allocations --o=filename`
  - e.g `print_unallocated --o=data`

2. To test the app:
- Install `nosetest module` using using `pip install nose` for python 2 and `pip3 install nose` for python 3.
- After cloning the repo, cd into the `app/tests` directory and run `nosetests dojo_tests.py`.