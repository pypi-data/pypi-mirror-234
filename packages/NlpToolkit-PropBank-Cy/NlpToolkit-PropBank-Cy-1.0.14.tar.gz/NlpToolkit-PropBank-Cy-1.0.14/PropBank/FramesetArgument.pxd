cdef class FramesetArgument(object):

    cdef str __argument_type,__definition, __function

    cpdef str getArgumentType(self)
    cpdef str getDefinition(self)
    cpdef str getFunction(self)
    cpdef setDefinition(self, str definition)
    cpdef setFunction(self, str function)