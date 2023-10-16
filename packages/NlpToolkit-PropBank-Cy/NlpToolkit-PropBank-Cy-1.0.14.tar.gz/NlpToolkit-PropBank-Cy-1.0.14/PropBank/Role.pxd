from PropBank.ArgumentType import ArgumentType


cdef class Role(object):

    cdef str __description, __f, __n

    cpdef str getDescription(self)
    cpdef str getF(self)
    cpdef str getN(self)
    cpdef object getArgumentType(self)