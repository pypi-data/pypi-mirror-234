cdef class Role(object):

    def __init__(self,
                 description: str,
                 f: str,
                 n: str):
        """
        A constructor of Role class which takes description, f, and n as inputs and initializes corresponding with
        these inputs.

        PARAMETERS
        ----------
        description : str
            Description of the role
        f : str
            Argument Type of the role
        n : str
            Number of the role
        """
        self.__description = description
        self.__f = f
        self.__n = n

    cpdef str getDescription(self):
        """
        Accessor for description.

        RETURNS
        -------
        str
            description.
        """
        return self.__description

    cpdef str getF(self):
        """
        Accessor for f.

        RETURNS
        -------
        str
            f.
        """
        return self.__f

    cpdef str getN(self):
        """
        Accessor for n.

        RETURNS
        -------
        str
            n.
        """
        return self.__n

    cpdef object getArgumentType(self):
        """
        Constructs and returns the argument type for this role.

        RETURNS
        -------
        ArgumentType
            Argument type for this role.
        """
        return ArgumentType.getArguments("ARG" + self.__f.upper())

    def __repr__(self):
        return f"{self.__f} {self.__n} {self.__description}"
