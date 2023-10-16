from PropBank.ArgumentType import ArgumentType


cdef class Frameset(object):

    cdef list __frameset_arguments
    cdef str __id

    cpdef bint containsArgument(self, object argumentType)
    cpdef addArgument(self, str argumentType, str definition, str function=*)
    cpdef deleteArgument(self, str argumentType, str definition)
    cpdef list getFramesetArguments(self)
    cpdef str getId(self)
    cpdef setId(self, str _id)
    cpdef save(self, str fileName)