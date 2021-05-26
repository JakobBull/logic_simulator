"""Test the names module."""
import pytest
from names import Names

#Return a new names instance
@pytest.fixture
def new_names():
    return Names()

#Return a list of example names
@pytest.fixture
def name_string_list():
    return ["Alice", "Bob", "Eve"]

#Return a names instance, after three names have been added
@pytest.fixture
def used_names(name_string_list):
    name = Names()
    name.lookup(name_string_list)
    return name

"""TESTS FOR QUERY"""
#QUERY:
    #Returns the corresponding name ID for name_string.
    #If the name string is not present in the names list, return None.

#tests if query raises the right exceptions for unexpected inputs
def test_query_raises_exceptions(used_names):
	#query only accepts a name_string
	with pytest.raises(TypeError):
		used_names.query(10)
	with pytest.raises(TypeError):
		used_names.query(2.2)
	with pytest.raises(TypeError):
		used_names.query(["hello", "bye"])
    #Python does not have a character data type,
    #a single character is simply a string with a length of 1

@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Alice"),
    (1, "Bob"),
    (2, "Eve"),
])
#tests if query returns correct name ID for a name sting
def test_query_output(used_names, new_names, name_id, expected_string, name_string_list):
	#tests that the right name_id returned if name string is present
	assert used_names.query(expected_string) == name_id
	#tests that the "None" is returned if name string isn't present
	assert new_names.query(expected_string) is None

"""TESTS FOR LOOKUP"""
#LOOKUP
    #Returns a list of name IDs for each name string in name_string_list.
    #If the name string is not present in the names list, add it.
#test to see if lookup adds new names
def test_lookup_add_new_names(new_names,used_names,name_string_list):
    #tests to see that lookup returns no name_ids when using lookup
    #function on the new_names instance, since the new_names instance
    #has no stored names
    assert new_names.lookup(name_string_list) == []
    #tests to see that after the first attempt to lookup name_string_list
    #the names of name_string_list are stores in the new_names instance
    assert new_names.lookup(name_string_list) == [0,1,2]
#test to see if lookup will find list of name ids for name_string_list
def test_lookup_finds_stored_names(new_names,used_names,name_string_list):
    #tests that the right name_ids list is returned for the example name_string_list
    #all name_ids should be found when using the example name_string_list on the used_names instance
    assert used_names.lookup(name_string_list) == [0,1,2]
    #tests that no ids are found when list of names that haven't been used before
    #are used as parameter to lookup function for both new_names and used_names instances
    assert used_names.lookup(["bob","mike","jill"]) == []
    assert new_names.lookup(["bob","mike","jill"]) == []

"""TESTS FOR GET_NAME_STRING"""
#GET_NAME_STRING
    #Return the corresponding name string for name_id.
    #If the name_id is not an index in the names list, return None.

#tests if get_name_string raises the right error for wrong inputs
def test_get_name_string_raises_exceptions(used_names):
    """Test if get_string raises expected exceptions."""
    with pytest.raises(TypeError):      #only accepts integers, not doubles
        used_names.get_name_string(1.4)
    with pytest.raises(TypeError):      #only accepts integers, not strings
        used_names.get_name_string("hello")
    with pytest.raises(ValueError):     #only accepts +ve integers
        used_names.get_name_string(-1)  #can't have a -ve index to the names list

#expected results when using used_name instance of Names class
@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Alice"),
    (1, "Bob"),
    (2, "Eve"),
    (3, None)
])
#Test if get_name_string returns the expected string
def test_get_name_string_output(used_names, new_names, name_id, expected_string):
    #tests that get_name_string returns the right name when given the corresponding name_id
    #for instance of name, used_names, that has seen all of these names to be tested
    assert used_names.get_name_string(name_id) == expected_string
    #tests that None is returned if the name hasn't been seen
    #just running the same test on the instance of names
    #that hasn't seen any of the tested names - new_names
    assert new_names.get_name_string(name_id) == None
