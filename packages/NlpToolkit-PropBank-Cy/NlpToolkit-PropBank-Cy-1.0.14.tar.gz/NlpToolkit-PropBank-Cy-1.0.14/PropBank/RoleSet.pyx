cdef class RoleSet(object):

    def __init__(self, _id: str, name: str):
        """
        A constructor of RoleSet class which takes id and name as inputs and initializes corresponding attributes
        with these inputs.

        PARAMETERS
        ----------
        _id : str
            Id of the roleSet
        name : str
            Name of the roleSet
        """
        self.__id = _id
        self.__name = name
        self.__roles = []

    cpdef str getId(self):
        """
        Accessor for id.

        RETURNS
        -------
        str
            id.
        """
        return self.__id

    cpdef str getName(self):
        """
        Accessor for name.

        RETURNS
        -------
        str
            name.
        """
        return self.__name

    cpdef int size(self):
        """
        The size method returns the size of the roles list.

        RETURNS
        -------
        int
            the size of the roles list.
        """
        return len(self.__roles)

    cpdef addRole(self, Role role):
        """
        The addRole method takes a Role as input and adds it to the roles list.

        PARAMETERS
        ----------
        role : Role
            Role to be added
        """
        self.__roles.append(role)

    cpdef Role getRole(self, int index):
        """
        The getRole method returns the role at the given index.

        PARAMETERS
        ----------
        index : int
            Index of the role

        RETURNS
        -------
        Role
            Role at the given index.
        """
        return self.__roles[index]

    cpdef Role getRoleWithArgument(self, str n):
        """
        Finds and returns the role with the given argument number n. For example, if n == 0, the method returns
        the argument ARG0.

        PARAMETERS
        ----------
        n : str
            Argument number

        RETURNS
        -------
        Role
            The role with the given argument number n.
        """
        for role in self.__roles:
            if role.getN() == n:
                return role

    def __repr__(self):
        return f"{self.__id} {self.__name} {self.__roles}"
