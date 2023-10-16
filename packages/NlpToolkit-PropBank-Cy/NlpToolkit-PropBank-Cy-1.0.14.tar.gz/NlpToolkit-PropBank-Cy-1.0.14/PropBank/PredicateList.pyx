import xml.etree.ElementTree
from collections import KeysView

import pkg_resources
from PropBank.Predicate cimport Predicate
from PropBank.RoleSet cimport RoleSet
from PropBank.Role cimport Role


cdef class PredicateList(object):

    cdef dict __list

    def __init__(self, fileName = pkg_resources.resource_filename(__name__, 'data/english-propbank.xml')):
        """
        A constructor of PredicateList class which reads all predicate files inside the 'Frames' folder. For each
        file inside that folder, the constructor creates a Predicate and puts in inside the list dictionary.
        """
        self.__list = {}
        root = xml.etree.ElementTree.parse(fileName).getroot()
        for frame_set in root:
            for predicate in frame_set:
                lemma = predicate.attrib["lemma"]
                new_predicate = Predicate(lemma)
                for role_set in predicate:
                    _id = role_set.attrib["id"]
                    name = role_set.attrib["name"]
                    new_role_set = RoleSet(_id, name)
                    for roles in role_set:
                        for role in roles:
                            if "descr" in role.attrib:
                                descr = role.attrib["descr"]
                            else:
                                descr = ""
                            if "f" in role.attrib:
                                f = role.attrib["f"]
                            else:
                                f = ""
                            if "n" in role.attrib:
                                n = role.attrib["n"]
                            else:
                                n = ""
                            newRole = Role(descr, f, n)
                            new_role_set.addRole(newRole)
                    new_predicate.addRoleSet(new_role_set)
                self.__list[lemma] = new_predicate

    cpdef size(self):
        """
        The size method returns the number of predicates inside the list.

        RETURNS
        -------
        int
            the size of the list dict.
        """
        return len(self.__list)

    cpdef Predicate getPredicate(self, str lemma):
        """
        getPredicate method returns the Predicate with the given lemma.

        PARAMETERS
        ----------
        lemma : str
            Lemma of the searched predicate

        RETURNS
        -------
        Predicate
            Predicate which has the given lemma.
        """
        return self.__list[lemma]

    def getLemmaList(self) ->KeysView:
        """
        The method returns all lemma in the predicate list.

        RETURNS
        -------
        dict
            All lemma in the predicate list.
        """
        return self.__list.keys()
