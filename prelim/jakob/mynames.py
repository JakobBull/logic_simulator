"""Implements a name table for lexical analysis.

Classes
-------
MyNames - implements a name table for lexical analysis.
"""


class MyNames:

    """Implements a name table for lexical analysis.

    Parameters
    ----------
    No parameters.

    Public methods
    -------------
    lookup(self, name_string): Returns the corresponding name ID for the
                 given name string. Adds the name if not already present.

    get_string(self, name_id): Returns the corresponding name string for the
                 given name ID. Returns None if the ID is not a valid index.
    """

    def __init__(self):
        self.names = []

    def lookup(self, name_string):
        if name_string in self.names:
            return self.names.index(name_string)
        else:
            self.names.append(name_string)
            return self.names.index(name_string)

    def get_string(self, name_id):
        try:
            return self.names[name_id]
        except IndexError:
            return None
