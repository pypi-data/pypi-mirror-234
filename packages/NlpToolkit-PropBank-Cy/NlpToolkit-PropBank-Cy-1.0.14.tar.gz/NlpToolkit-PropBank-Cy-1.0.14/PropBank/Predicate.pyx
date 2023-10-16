from PropBank.RoleSet cimport RoleSet


cdef class Predicate(object):

    def __init__(self, lemma: str):
        """
        A constructor of Predicate class which takes lemma as input and initializes lemma with this input.
        The constructor also initializes the roleSets array.

        PARAMETERS
        ----------
        lemma : str
            Lemma of the predicate
        """
        self.__lemma = lemma
        self.__role_sets = []

    cpdef str getLemma(self):
        """
        Accessor for lemma.

        RETURNS
        -------
        str
            lemma.
        """
        return self.__lemma

    cpdef addRoleSet(self, RoleSet roleSet):
        """
        The addRoleSet method takes a RoleSet as input and adds it to the roleSets list.

        PARAMETERS
        ----------
        roleSet : RoleSet
            RoleSet to be added
        """
        self.__role_sets.append(roleSet)

    cpdef int size(self):
        """
        The size method returns the size of the roleSets list.

        RETURNS
        -------
        int
            the size of the roleSets list.
        """
        return len(self.__role_sets)

    cpdef RoleSet getRoleSet(self, int index):
        """
        The getRoleSet method returns the roleSet at the given index.

        PARAMETERS
        ----------
        index : int
            Index of the roleSet

        RETURNS
        -------
        RoleSet
            RoleSet at the given index.
        """
        return self.__role_sets[index]

    cpdef RoleSet getRoleSetWithId(self, str roleId):
        """
        Another getRoleSet method which returns the roleSet with the given roleSet id.

        PARAMETERS
        ----------
        roleId : str
            Id of the searched roleSet

        RETURNS
        -------
        RoleSet
            RoleSet which has the given id.
        """
        for role_set in self.__role_sets:
            if role_set.getId() == roleId:
                return role_set
        return None

    def __repr__(self):
        return f"{self.__lemma} {self.__role_sets}"
