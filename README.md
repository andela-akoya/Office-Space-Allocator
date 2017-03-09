# Office-Space-Allocator

The office space allocator is console application that manages the allocation of rooms by randomly allocating a newly added employee to a room.

## Installation

These are the basic steps to install and run the application locally on both a linux and windows system.

### Linux

```
1) Install the necessary packages
 $ sudo apt-get install python3-dev python-virtualenvwrapper git
2) sudo pip3 install virtualenvwrapper
3) mkvirtualenv --python=python3 cpenv
4) workon cpenv
```
### Windows
```
1) Download and Install python 3 using the link
	https://www.python.org/downloads/release/python-360/
2) pip3 install virtualenvwrapper
3) mkvirtualenv --python=python3 cpenv
4) workon cpenv
```


### Download the project by cloning the repository
From the terminal
```
1) git clone https://github.com/andela-akoya/Office-Space-Allocator.git
2) cd Office-Space-Allocator
3) pip install -r requirements.txt

virtualenv --python python3 venv-dojo
source venv-dojo/bin/activate

pip install -r requirements.txt
```

#### How should this be locally tested?

##### Usage:

```

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
```

##### To test the app:

```
- After cloning the repo, cd into the app/test directory and run nosetests dojo_tests.py.
```
### Contributing to the project
```Koya Adegboyega```

### Author
```Koya Adegboyega```

### License
```
MIT License
```
