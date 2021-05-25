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
    name = Names()
    for name in name_string_list:
        name.lookup(name)
    return name

#GET_NAME_STRING TESTS FROM PRELIM EXERCISE
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
    assert new_names.get_name_string(name_id) is None

#TESTS FOR QUERY
#tests if query raises the right exceptions for unexpected inputs
def test_query_raises_exceptions(used_names):
	#query only accepts a name_string
	with pytest.raises(TypeError):
		used_names.query(10)
	with pytest.raises(TypeError):
		used_names.query(2.2)
	with pytest.raises(TypeError):
		used_names.query('a')
	with pytest.raises(TypeError):
		used_names.query(["hello", "bye"])

#tests if query returns correct name ID for a name sting
def test_query_output(new_names,used_names, name_string_list):
	#tests that the right name_id returned if name string is present
	assert used_names.query(expected_string) == name_id
	#tests that the "None" is returned if name string isn't present
	assert new_names.query(expected_string) is None

#TESTS FOR LOOKUP
#test to see if lookup adds new names
def test_lookup_add_new_names(new_names,used_names,name_string_list):
    """Return a names instance, after three names have been added."""
    for name in name_string_list:
        new_names.lookup(name)
    assert new_names.names == used_names.names

#test to see if lookup will find names that are already stored
def test_lookup_finds_stored_names(used_names,name_string_list):
    """Return a names instance, after three names have been added."""
    for name in name_string_list:
        assert used_names.lookup(name) is not None
