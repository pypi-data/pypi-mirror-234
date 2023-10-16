# README #

This library contains helper code for working with Cosmic Frog Anura supply chain models

# What is this repository for?

Include this library in your code to simplify interactions with Cosmic Frog models when integrating with external systems

# How do I get set up? #

include cosmic_frog
see examples folder for example code for common operations
see tests folder for tests and example files

## running the tests with pytest
The tests and associated files are located in the ./cosmicfrog/cosmicfrog/tests directory. In order to run these tests with pytest you will need to run them from the ./cosmicfrog directory. This is necessary so the project can be properly imported without having to do a full build of the component.  
```
/mnt/c/code/cosmicfrog/cosmicfrog-cosmicfrog/cosmicfrog (feature/excel-sheet1)$ python -m pytest cosmicfrog/tests/unit_test.py -v
```
In order to have the component be able to import from the local source code and find all the directories, depencies, files, etc. you will need to run the command as shown above. It needs to be in the project directory (/mnt/c/code/cosmicfrog/cosmicfrog-cosmicfrog or below) in order to be able to import the directory in the python path when the tests start

Also note the use of the `Path(__file__).with_name('customers.csv')` pattern in unit_test.py. This ensures that dependent files in the tests that are in the same directory as the tests will be open.

# Who do I talk to? #

* cosmicfrog.com
* support@optilogic.com
