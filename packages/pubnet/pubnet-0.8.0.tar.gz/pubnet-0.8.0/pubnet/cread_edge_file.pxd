cdef extern from "src/read_edge_file.h":
    int* read_edge_file(char* file_name)
