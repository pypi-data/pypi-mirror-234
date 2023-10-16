from PropBank.Frameset cimport Frameset


cdef class FramesetList(object):

    cdef list __frames

    cpdef dict readFromXml(self, str synSetId)
    cpdef bint frameExists(self, str synSetId)
    cpdef Frameset getFrameSet(self, synSetIdOrIndex)
    cpdef addFrameset(self, Frameset frameset)
    cpdef int size(self)
