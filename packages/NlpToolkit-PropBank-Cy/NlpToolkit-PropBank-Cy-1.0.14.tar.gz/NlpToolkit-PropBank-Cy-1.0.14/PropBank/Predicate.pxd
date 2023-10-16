from PropBank.RoleSet cimport RoleSet


cdef class Predicate(object):

    cdef str __lemma
    cdef list __role_sets

    cpdef str getLemma(self)
    cpdef addRoleSet(self, RoleSet roleSet)
    cpdef int size(self)
    cpdef RoleSet getRoleSet(self, int index)
    cpdef RoleSet getRoleSetWithId(self, str roleId)