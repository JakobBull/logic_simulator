"""Test the names module."""
import pytest
from names import Names

@pytest.fixture
def new_names():
    """Return a new names instance."""
    return Names()

@pytest.fixture
def name_string_list():
    """Return a list of example names."""
    return ["Alice", "Bob", "Eve"]

@pytest.fixture
def used_names(name_string_list):
    """Return a names instance, after three names have been added."""
    return Names(name_string_list)
#TESTS FOR QUERY
#QUERY:
    #Return the corresponding name ID for name_string.
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

#TESTS FOR LOOKUP
#LOOKUP
    #Return a list of name IDs for each name string in name_string_list.
    #If the name string is not present in the names list, add it.
#test to see if lookup adds new names
def test_lookup_add_new_names(new_names,used_names,name_string_list):
    new_names.lookup(name_string_list) == new_names.names

#test to see if lookup will find list of name ids for name_string_list
def test_lookup_finds_stored_names(new_names,used_names,name_string_list):
        #tests that the right name_ids list is returned for the example name_string_list
        #all name_ids should be found when using the example name_string_list on the used_names instance
    	assert used_names.lookup(name_string_list) == [0,1,2]
    	#tests that no ids are found when new names are added to the new_names instance
    	assert new_names.lookup(["bob","mike","jill"]) == []
        #test that after being added, the ids of the new names are returned
        #assert new_names.lookup(["bob","mike","jill"]) == [0,1,2]
        #REVIEW WHY ABOVE GIVES TABS ERROR!

#GET_NAME_STRING TESTS FROM PRELIM EXERCISE
#GET_NAME_STRING
    #Return the corresponding name string for name_id.
    #If the name_id is not an index in the names list, return None.
def test_get_name_string_raises_exceptions(used_names):
    """Test if get_string raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_name_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_name_string("hello")
    with pytest.raises(ValueError):
        used_names.get_name_string(-1)

#expected results when using used_name instance of Names class
@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Alice"),
    (1, "Bob"),
    (2, "Eve"),
    (3, None)
])

def test_get_name_string_output(used_names, new_names, name_id, expected_string):
    """Test if get_string returns the expected string."""
    # Name is present
    assert used_names.get_name_string(name_id) == expected_string
    # Name is absent
    assert new_names.get_name_string(name_id) == expected_string
