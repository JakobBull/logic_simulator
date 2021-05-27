"""Map variable names and string names to unique integers.

Used in the Logic Simulator project. Most of the modules in the project
use this module either directly or indirectly.

Classes
-------
Names - maps variable names and string names to unique integers.
"""


class Names:
    """Map variable names and string names to unique integers.
    This class deals with storing grammatical keywords and user-defined words,
    and their corresponding name IDs, which are internal indexing integers. It
    provides functions for looking up either the name ID or the name string.
    It also keeps track of the number of error codes defined by other classes,
    and allocates new, unique error codes on demand.

    Parameters
    ----------
    No parameters.

    Public methods
    -------------
    unique_error_codes(self, num_error_codes): Returns a list of unique integer
    query(self, name_string): Returns the corresponding name ID for the
                        name string. Returns None if the string is not present.

    lookup(self, name_string_list): Returns a list of name IDs for each
                        name string. Adds a name if not already present.

    get_name_string(self, name_id): Returns the corresponding name string for
                        the name ID. Returns None if the ID is not present.
    """

    def __init__(self):
        """Initialise names list."""
        self.error_code_count = 0  # how many error codes have been declared
        self.names = []

    def unique_error_codes(self, num_error_codes):
        """Return a list of unique integer error codes."""
        if not isinstance(num_error_codes, int):
            raise TypeError("Expected num_error_codes to be an integer.")
        self.error_code_count += num_error_codes
        return range(self.error_code_count - num_error_codes,
                     self.error_code_count)

    def query(self, name_string):
        """Return the corresponding name ID for name_string.
        If the name string is not present in the names list, return None.
        """
        # raise TypeError if name_string isn't a string
        if not isinstance(name_string, str):
            raise TypeError("Only strings are allowed as inputs to query")
        # iterate through all indeces of names list
        for i in range(len(self.names)):
            # return index whose name == name_stirng
            if self.names[i] == name_string:
                return i
        # return none if return hasn't been called in for loop
        return None

    def lookup(self, name_string_list):
        """Return a list of name IDs for each name string in name_string_list.
        If the name string is not present in the names list, add it.
        """
        name_ids = []
        # boolean to determine whether a name in name_string_list
        # is in names of instance
        for n in name_string_list:
            present = False
            for i in range(len(self.names)):
                if self.names[i] == n:
                    name_ids.append(i)
                    present = True
                    # if a name in name_string_list is found,
                    # change present to true and break loop
                    break
            if(present is False):
                # if a name in name_string_list isn't found,
                # add to names list of instance
                # and add its name_id to the name_ids list
                # add length of names to name_ids before adding new name,
                # since length of old names list will be the index of the
                # new name
                name_ids.append(len(self.names))
                self.names.append(n)
        return name_ids

    def get_name_string(self, name_id):
        """Return the corresponding name string for name_id.
        If the name_id is not an index in the names list, return None.
        """
        # from prelim exercise
        if not type(name_id) is int:
            raise TypeError(
                "Only +ve integers are allowed as inputs to get_name_string")
        if name_id < 0:
            raise ValueError(
                "only +ve integers allowed as inputs to get_name_string")
        if name_id <= len(self.names)-1:
            return self.names[name_id]
