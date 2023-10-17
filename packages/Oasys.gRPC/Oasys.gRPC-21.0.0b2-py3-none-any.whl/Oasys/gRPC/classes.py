# Class to represent an item in Oasys software.
# For each item we store a type and a handle to uniquely identify it.
class OasysItem:

    def __init__(self, objtype, handle):
        self._objtype = objtype
        self._handle  = handle

# Class to represent an argument for a function call in Oasys software.
class OasysArg:

    def __init__(self):
        pass

# An instance of OasysArg to represent a default argument passed to a function
defaultArg = OasysArg()
