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
  create_room (<room_names> <room_types>)...
  add_person <first_name> <last_name> <STAFF/FELLOW> [<wants_accommodation>]
  reallocate_person <person_identifier> <new_room_name>
  load_people <filename>
  load_rooms <filename>
  rename_room <old_room_name> <new_room_name>
  print_room <room_name>
  print_allocations [(--o=<filename> [override|append])]
  print_unallocated [(--o=<filename> [override|append])]
  save_state [--db=sqlite_database]
  load_state [--db=sqlite_database]
  clear
  help
```

##### Usage Example:

- To create a room
   ```
	   create_room office Orange
   ```

- To create multiple rooms at once
 ```
	 create_room livingspace Orange Red Green White
 ```
- To add a person to a room
```
	add_person John Doe staff y
```
- To print members of a room
  ```
	  print_room Orange
  ```
- To print allocations to command line
```
	print_allocations
```
- To print allocations to a text file
```
	print_allocations --o=data
```
- To print unallocated
 ```
	 print_unallocated
 ```
- To print unallocated to a text file 
```
print_unallocated --o=data
```


##### To test the app:

```
- After cloning the repo,
 cd into the app/test directory
  run nosetests dojo_tests.py.
```
### Contributing to the project
```Koya Adegboyega```

### Author
```Koya Adegboyega```

### License
```
MIT License
```
