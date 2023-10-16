from PropBank.ArgumentType import ArgumentType
from PropBank.FramesetArgument cimport FramesetArgument
from xml.etree.ElementTree import Element


cdef class Frameset(object):

    def __init__(self, framesetNode: Element = None):
        """
        Another constructor of Frameset class which takes filename as input and reads the frameset

        PARAMETERS
        ----------
        framesetNode : Element
            File name of the file to read frameset
        """
        if framesetNode is not None:
            self.__id = framesetNode.attrib["id"]
            self.__frameset_arguments = []
            for child in framesetNode:
                self.__frameset_arguments.append(FramesetArgument(child.attrib["name"], child.text,
                                                                  child.attrib["function"]))
        else:
            self.__id = ""
            self.__frameset_arguments = []

    cpdef bint containsArgument(self, object argumentType):
        """
        containsArgument method which checks if there is an Argument of the given argumentType.

        PARAMETERS
        ----------
        argumentType : ArgumentType
            ArgumentType of the searched Argument

        RETURNS
        -------
        bool
            true if the Argument with the given argumentType exists, false otherwise.
        """
        for frameset_argument in self.__frameset_arguments:
            if ArgumentType.getArguments(frameset_argument.getArgumentType()) == argumentType:
                return True
        return False

    cpdef addArgument(self,
                      str argumentType,
                      str definition,
                      str function = None):
        """
        The addArgument method takes a type and a definition of a FramesetArgument as input, then it creates a new
        FramesetArgument from these inputs and adds it to the framesetArguments list.

        PARAMETERS
        ----------
        argumentType : str
            Type of the new FramesetArgument
        definition : str
            Definition of the new FramesetArgument
        function: str
            Function of the new FramesetArgument
        """
        cdef FramesetArgument frameset_argument
        check = False
        for frameset_argument in self.__frameset_arguments:
            if frameset_argument.getArgumentType() == argumentType:
                frameset_argument.setDefinition(definition)
                check = True
                break
        if not check:
            arg = FramesetArgument(argumentType, definition, function)
            self.__frameset_arguments.append(arg)

    cpdef deleteArgument(self,
                         str argumentType,
                         str definition):
        """
        The deleteArgument method takes a type and a definition of a FramesetArgument as input, then it searches for the
        FramesetArgument with these type and definition, and if it finds removes it from the framesetArguments list.

        PARAMETERS
        ----------
        argumentType : str
            Type of the to be deleted FramesetArgument
        definition : str
            Definition of the to be deleted FramesetArgument
        """
        cdef FramesetArgument frameset_argument
        for frameset_argument in self.__frameset_arguments:
            if frameset_argument.getArgumentType() == argumentType and frameset_argument.getDefinition() == definition:
                self.__frameset_arguments.remove(frameset_argument)
                break

    cpdef list getFramesetArguments(self):
        """
        Accessor for framesetArguments.

        RETURNS
        -------
        list
            framesetArguments.
        """
        return self.__frameset_arguments

    cpdef str getId(self):
        """
        Accessor for id.

        RETURNS
        -------
        str
            id.
        """
        return self.__id

    cpdef setId(self, str _id):
        """
        Mutator for id.

        PARAMETERS
        ----------
        _id : str
            id to set.
        """
        self.__id = _id

    cpdef save(self, str fileName):
        """
        Saves current frameset with the given filename.

        PARAMETERS
        ----------
        fileName : str
            Name of the output file.
        """
        output_file = open(fileName, mode="w", encoding="utf-8")
        output_file.write("<FRAMESET id=\"" + self.__id + "\">\n")
        for framesetArgument in self.__frameset_arguments:
            output_file.write("\t<ARG name=\"" + framesetArgument.getArgumentType() + "\" function=\"" +
                             framesetArgument.getFunction() + "\">" + framesetArgument.getDefinition() + "</ARG>\n")
        output_file.write("</FRAMESET>\n")
        output_file.close()

    def __repr__(self):
        return f"{self.__id} {self.__frameset_arguments}"
