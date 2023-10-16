cdef class FramesetArgument(object):

    def __init__(self,
                 argumentType: str,
                 definition: str,
                 function: str = None):
        """
        A constructor of FramesetArgument class which takes argumentType and definition as input and initializes
        corresponding attributes

        PARAMETERS
        ----------
        argumentType : str
            ArgumentType of the frameset argument
        definition : str
            Definition of the frameset argument
        function : str
            Function of the frameset argument
        """
        self.__argument_type = argumentType
        self.__definition = definition
        self.__function = function

    cpdef str getArgumentType(self):
        """
        Accessor for argumentType.

        RETURNS
        -------
        str
            argumentType.
        """
        return self.__argument_type

    cpdef str getDefinition(self):
        """
        Accessor for definition.

        RETURNS
        -------
        str
            definition.
        """
        return self.__definition

    cpdef str getFunction(self):
        """
        Accessor for function.

        RETURNS
        -------
        str
            function.
        """
        return self.__function

    cpdef setDefinition(self, str definition):
        """
        Mutator for definition.

        PARAMETERS
        ----------
        definition : str
            definition to set.
        """
        self.__definition = definition

    cpdef setFunction(self, str function):
        """
        Mutator for definition.

        PARAMETERS
        ----------
        function : str
            function to set.
        """
        self.__function = function

    def __str__(self) -> str:
        """
        __str__ converts an FramesetArgument to a string. It returns argument string which is in the form of
        argumentType:definition

        RETURNS
        -------
        str
            string form of frameset argument
        """
        return self.__argument_type + ":" + self.__definition
