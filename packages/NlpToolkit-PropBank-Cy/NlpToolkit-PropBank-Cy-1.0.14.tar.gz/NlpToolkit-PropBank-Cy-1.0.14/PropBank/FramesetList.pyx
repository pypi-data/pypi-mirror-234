import pkg_resources
import xml
import xml.etree.ElementTree

from PropBank.FramesetArgument cimport FramesetArgument

cdef class FramesetList(object):

    def __init__(self, fileName = pkg_resources.resource_filename(__name__, 'data/turkish-propbank.xml')):
        """
        A constructor of FramesetList class which reads all frameset files inside the Predicates folder. For each
        file inside that folder, the constructor creates a Frameset and puts in inside the frames list.
        """
        self.__frames = []
        root = xml.etree.ElementTree.parse(fileName).getroot()
        for frameset_node in root:
            frameset = Frameset(frameset_node)
            self.__frames.append(frameset)

    cpdef dict readFromXml(self, str synSetId):
        """
        readFromXmL method searches the Frameset with a given synSetId if there is a Frameset with the given synSet id,
        returns the arguments of that Frameset as a dictionary.

        PARAMETERS
        ----------
        synSetId : str
            Id of the searched Frameset

        RETURNS
        -------
        dict
            a dict containing the arguments of the searched Frameset
        """
        cdef Frameset f
        cdef int i
        cdef FramesetArgument frameset_argument
        frameset = {}
        for f in self.__frames:
            if f.getId() == synSetId:
                for i in range(len(f.getFramesetArguments())):
                    frameset_argument = f.getFramesetArguments()[i]
                    frameset[frameset_argument.getArgumentType()] = frameset_argument.getDefinition()
        return frameset

    cpdef bint frameExists(self, str synSetId):
        """
        frameExists method checks if there is a Frameset with the given synSet id.

        PARAMETERS
        ----------
        synSetId : str
            Id of the searched Frameset

        RETURNS
        -------
        bool
            true if the Frameset with the given id exists, false otherwise.
        """
        cdef Frameset f
        for f in self.__frames:
            if f.getId() == synSetId:
                return True
        return False

    cpdef Frameset getFrameSet(self, synSetIdOrIndex):
        """
        getFrameSet method returns the Frameset with the given synSet id or index

        PARAMETERS
        ----------
        synSetIdOrIndex
            Id of the searched Frameset

        RETURNS
        -------
        Frameset
            Frameset which has the given id.
        """
        cdef Frameset f
        if isinstance(synSetIdOrIndex, str):
            for f in self.__frames:
                if f.getId() == synSetIdOrIndex:
                   return f
        elif isinstance(synSetIdOrIndex, int):
            return self.__frames[synSetIdOrIndex]
        return None

    cpdef addFrameset(self, Frameset frameset):
        """
        The addFrameset method takes a Frameset as input and adds it to the frames list.

        PARAMETERS
        ----------
        frameset : Frameset
            Frameset to be added
        """
        self.__frames.append(frameset)

    cpdef int size(self):
        """
        The size method returns the size of the frames list.

        RETURNS
        -------
        int
            the size of the frames list.
        """
        return len(self.__frames)
