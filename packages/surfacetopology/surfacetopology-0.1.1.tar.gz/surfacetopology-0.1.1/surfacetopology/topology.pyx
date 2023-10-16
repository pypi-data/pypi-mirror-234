import numpy as np

#-----------------------------------------------------------------------------
cdef extern from "trisurftopology.h":
    cdef cppclass TriSurfTopology:
        TriSurfTopology()
        void initialize(int nt_, int* tri_)
        void determine_topology()
        int* get_array_ptr(int array_type, int index)
        int get_array_size(int array_type, int index)
        int nv_tot
        int nt_tot
        int ne_tot
        int nbound_tot
        int ncomp
        int* nv
        int* nt
        int* ne
        int* oriented
        int* orientable
        int* manifold
        int* nbound
        int* bound_path
        int* bound_path_sep
        int* bound_path_comp

#-----------------------------------------------------------------------------
cdef to_ndarray(int size, int* array):
    cdef int i
    pyarray = np.empty(size, dtype=np.int32)
    for i in range(size):
        pyarray[i] = array[i]
    return pyarray

#-----------------------------------------------------------------------------
cdef to_list_of_ndarrrays(TriSurfTopology *topo, int array_type):
    cdef:
        int c
        list L = []
    for c in range(topo.ncomp):
        L.append(to_ndarray(topo.get_array_size(array_type, c), 
                            topo.get_array_ptr(array_type, c)))
    return L

#-----------------------------------------------------------------------------
def trisurftopology(int[:, ::1] triangles):
    cdef:
        TriSurfTopology topo
        int[:, ::1] triangles_ptr
        int nc

    triangles_ptr = triangles
    if triangles.size == 0:
        topo.initialize(triangles.shape[0], NULL)
    else:
        topo.initialize(triangles.shape[0], &triangles_ptr[0, 0])
    topo.determine_topology()
    nc = topo.ncomp

    return {
        'comp': to_ndarray(topo.get_array_size(0, 0), 
                           topo.get_array_ptr(0, 0)),
        'nv': to_ndarray(nc, topo.nv),
        'nt': to_ndarray(nc, topo.nt),
        'ne': to_ndarray(nc, topo.ne),
        'nbound': to_ndarray(nc, topo.nbound),
        'oriented': to_ndarray(nc, topo.oriented),
        'orientable': to_ndarray(nc, topo.orientable),
        'manifold': to_ndarray(nc, topo.manifold),
        'bound_path': to_ndarray(topo.bound_path_sep[topo.nbound_tot], 
                                 topo.bound_path),
        'bound_path_sep': to_ndarray(topo.nbound_tot+1, topo.bound_path_sep),
        'bound_path_comp': to_ndarray(topo.nbound_tot, topo.bound_path_comp),
        'collapsed_triangles': to_list_of_ndarrrays(&topo, 1),
        'nonmanifold_vertices': to_list_of_ndarrrays(&topo, 2),
        'nonmanifold_edges': to_list_of_ndarrrays(&topo, 3),
        'repaired_orientation': to_list_of_ndarrrays(&topo, 4),
    }
    