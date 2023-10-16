from PropBank.Role cimport Role


cdef class RoleSet(object):

    cdef str __id, __name
    cdef list __roles

    cpdef str getId(self)
    cpdef str getName(self)
    cpdef int size(self)
    cpdef addRole(self, Role role)
    cpdef Role getRole(self, int index)
    cpdef Role getRoleWithArgument(self, str n)
