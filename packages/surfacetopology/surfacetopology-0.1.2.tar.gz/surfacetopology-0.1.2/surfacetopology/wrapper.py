from dataclasses import dataclass, field
import numpy as np
from .topology import trisurftopology

__all__ = ['surface_topology', 'SurfaceTopology', 
           'renumber_vertices', 'disjoint_sum', 'connected_sum',
           'homeomorphic', 'small_mesh']

#-----------------------------------------------------------------------------
@dataclass
class SurfaceTopology:
    n_vertices: int
    n_edges: int
    n_triangles: int
    n_boundaries: int
    genus: int
    euler: int
    manifold: bool
    oriented: bool
    orientable: bool
    closed: bool
    vertices: np.ndarray = field(compare=False)
    triangles: np.ndarray  = field(compare=False)
    boundaries: list = field(compare=False)
    nonmanifold_vertices: np.ndarray = field(compare=False)
    nonmanifold_edges: np.ndarray = field(compare=False)
    collapsed_triangles: np.ndarray = field(compare=False)

    #-------------------------------------------------------------------------
    @property
    def sizes(self):
        return (self.n_vertices, self.n_edges, self.n_triangles, 
                self.n_boundaries)
    
    #-------------------------------------------------------------------------
    @property
    def invariants(self):
        return self.manifold, self.orientable, self.n_boundaries, self.genus
    
    #-------------------------------------------------------------------------
    def __repr__(self):
        s = __class__.__name__ + f'(n_vertices={self.n_vertices}'
        if self.n_vertices == 0:
            return s+')'
        if self.n_vertices <= 2:
            return s+f', vertices={self.vertices})'
        s += f', n_edges={self.n_edges}, n_triangles={self.n_triangles}' \
             + f', n_boundaries={self.n_boundaries}'
        
        if not self.manifold:
            s += f', manifold={self.manifold}'
            if self.nonmanifold_vertices.size:
                s += f', nonmanifold_vertices={self.nonmanifold_vertices}'
            if self.nonmanifold_edges.size:
                s += f', nonmanifold_edges={self.nonmanifold_edges}'
            if self.collapsed_triangles.size:
                s += f', collapsed_triangles={self.collapsed_triangles}'
            return s+')'
        
        s += f', euler={self.euler}, genus={self.genus}' \
           + f', manifold={self.manifold}, oriented={self.oriented}'
        if not self.oriented:
            s += f', orientable={self.orientable}'
        s += f', closed={self.closed}'
        return s+')'

#-----------------------------------------------------------------------------
def surface_topology(triangles) -> list[SurfaceTopology]:
    """Check the validity and determine the topology of a triangulated 
    surface (compact 2-manifold)

    Args:
        triangles (nt-by-3 int array): each row is a triangle described by the
            indices of its 3 vertices (indices start from 0); the number of 
            vertices is assumed to be triangles.max()+1
    
    Returns:
        list of SurfaceTopology: each element of the list is a connected 
        component (sorted from the largest to the smallest in terms of number 
        of vertices). The SurfaceTopology object contains the following 
        attributes:
        - n_vertices (int): number of vertices
        - n_edges (int): number of edges
        - n_triangles (int): number of triangles
        - n_boundaries (int): number of boundaries
        - genus (int): the genus is the number of handles (orientable surface)
          or cross-caps (non-orientable surface)
        - euler (int): Euler characteristic
        - manifold (bool): True if all the conditions for a manifold are 
          satisfied
        - oriented (bool): True if the triangles are consistently oriented
        - orientable (bool): True if the triangles can be consistently 
          oriented
        - closed (bool): True if there is no boundary
        - vertices (int array): indices of vertices in the connected comopnent
        - triangles (nt-by-3 int array): triangles in the connected component,
          with consistent orientation (if possible)
        - boundaries (list of int array): list of boundaries (arrays of vertex
          indices); if manifold=True, the vertices are ordered along the 
          boundary
        - nonmanifold_vertices (int array): vertex indices where the set of 
          adjacent triangles does not form a closed or open fan
        - nonmanifold_edges (n-by-2 int array): list of edges (identified by 
          the indices of their vertices) that have more than two adjacent 
          triangles
        - collapsed_triangles (int array): triangles in which 2 or 3 vertices
          are identical
    """
    triangles = np.ascontiguousarray(triangles, dtype=np.int32)
    if triangles.size == 0:
        triangles = np.empty((0, 3), dtype=np.int32)
    if triangles.ndim != 2 or triangles.shape[1] != 3:
        raise ValueError('the argument "triangles" must be nt-by-3 array')
    out = trisurftopology(triangles)
    components =[]

    B = np.split(out['bound_path'], out['bound_path_sep'][1:-1])
    B_comp = out['bound_path_comp']
    
    for c in range(out['nv'].size):
        boundaries = [B[k] for k in np.where(B_comp == c)[0]]
        chi = out['nv'][c] - out['ne'][c] + out['nt'][c]
        if out['orientable'][c]:
            # chi = nv - ne + nt = 2 - 2*g - nbound
            two_genus = 2 - chi - out['nbound'][c]
            if two_genus % 2 != 0 and out['manifold'][c] and out['nv'][c] > 1:
                raise ValueError('non-integer genus')
            genus = two_genus // 2
        else:
            # "demi-genus"
            # chi = nv - ne + nt = 2 - g - nbound
            genus = 2 - chi - out['nbound'][c]

        components.append(SurfaceTopology(
            n_vertices=out['nv'][c],
            n_edges=out['ne'][c],
            n_triangles=out['nt'][c],
            n_boundaries=out['nbound'][c],
            genus=genus,
            euler=chi,
            manifold=bool(out['manifold'][c]),
            oriented=bool(out['oriented'][c]),
            orientable=bool(out['orientable'][c]),
            closed=out['nbound'][c] == 0,
            vertices=np.where(out['comp'] == c)[0],
            triangles=out['repaired_orientation'][c].reshape((-1, 3)),
            boundaries=sorted(boundaries, key=lambda b: -b.size),
            collapsed_triangles=out['collapsed_triangles'][c],
            nonmanifold_vertices=out['nonmanifold_vertices'][c],
            nonmanifold_edges=out['nonmanifold_edges'][c].reshape((-1, 2)),
        ))
    
    return sorted(components, key=lambda C: -C.n_vertices)

#-----------------------------------------------------------------------------
def renumber_vertices(triangles):
    """Eliminate isolated vertices

    Args:
        triangles (nt-by-3 int array): each row is a triangle described by the
            indices of its 3 vertices 
    
    Returns:
        nt-by-3 int array: triangles with renumbered vertices
    """
    z = np.zeros(triangles.max()+1, np.int32)
    z[triangles.ravel()] = 1
    p = np.cumsum(z) - 1
    return p[triangles]

#-----------------------------------------------------------------------------
def disjoint_sum(*triangles):
    """Create a surface with multiple connected components

    Args:
        triangles1 (nt-by-3 int array): each row is a triangle described by 
            the indices of its 3 vertices 
        triangles2 (nt-by-3 int array): idem 
        etc. (variable number of arguments)
    
    Returns:
        nt-by-3 int array: new surface combining all the input surfaces
    """
    shift = np.cumsum([0] + [tri.max()+1 for tri in triangles])
    return np.vstack([tri+shift[i] for i, tri in enumerate(triangles)])

#-----------------------------------------------------------------------------
def _pick_nonboundary_vertex(triangles):
    T = surface_topology(triangles)
    if len(T) != 1:
        return -1
    if T[0].n_boundaries == 0:
        return 0
    B = np.concatenate(T[0].boundaries)
    interior = np.ones(triangles.max()+1, dtype=np.uint8)
    interior[B] = 0
    I, = np.where(np.all(interior[triangles], axis=1))
    if I.size == 0:
        return -1
    return I[0]

#-----------------------------------------------------------------------------
def connected_sum(*triangles):
    """Create a surface as a connected sum of multiple surfaces

    Args:
        triangles1 (nt-by-3 int array): each row is a triangle described by 
            the indices of its 3 vertices 
        triangles2 (nt-by-3 int array): idem 
        etc. (variable number of arguments)
    
    Returns:
        nt-by-3 int array: new surface combining all the input surfaces in a 
        single connected cmponent
    """
    if len(triangles) > 2:
        return connected_sum(triangles[0], connected_sum(*triangles[1:]))
    if len(triangles) < 2:
        return triangles
    triangles1, triangles2 = triangles
    idx1 = _pick_nonboundary_vertex(triangles1)
    idx2 = _pick_nonboundary_vertex(triangles2)
    if idx1 < 0 or idx2 < 0:
        raise ValueError("The surfaces must be connected and have at least "
                         + "one triangle not touching a boundary")
    shift = triangles1.max()+1
    tri1, tri2 = triangles1[idx1], triangles2[idx2] + shift
    tri = np.vstack((np.delete(triangles1, idx1, 0), 
                           np.delete(triangles2, idx2, 0) + shift))
    for k in range(3):
        tri[tri == tri2[k]] = tri1[2-k]
    return renumber_vertices(tri)

#-----------------------------------------------------------------------------
def homeomorphic(surface1, surface2):
    """Test if two manifolds are homeomorphic based on the classification of
    compact manifolds of dimension two

    Args:
        surface1 (nt-by-3 int array or SurfaceTopology): first surface
        surface2 (nt-by-3 int array or SurfaceTopology): second surface
    
    Returns:
        bool: True if both surfaces have the same topological invariants for 
        each connected component (returns False if any of them is not a 
        manifold)
    """
    name = ''
    T1, T2 = surface1, surface2
    if not isinstance(surface1, SurfaceTopology):
        T1 = surface_topology(surface1)
    if not isinstance(surface2, SurfaceTopology):
        if isinstance(surface2, str):
            name = surface2.lower()
            invariants = {'sphere': (True, True, 0, 0),
                          'torus': (True, True, 0, 1)}
            T2 = [invariants[name]]
        else:
            T2 = surface_topology(surface1)
    
    if len(T1) != len(T2):
        return False
    invariants1 = sorted([C.invariants for C in T1])
    if name:
        invariants2 = T2
    else:
        invariants2 = sorted([C.invariants for C in T2])
    
    for inv1, inv2 in zip(invariants1, invariants2):
        if not inv1[0] or not inv2[0]: # non-manifold
            return False
        if inv1 != inv2:
            return False
    return True

#-----------------------------------------------------------------------------
def small_mesh(name):
    """Create small examples of triangulated surfaces used for testing

    Args:
        name (str): name of the mesh ('sphere', 'tetrahedron'), 'cylinder',
            'moebius', 'torus', 'projplane', 'kleinbottle', 'hemiicosahedron'
    
    Returns:
        nt-by-3 int array: list of the triangles of the surface
    """
    name = name.lower()
    if name == 'sphere':
        return np.array([[0, 1, 2], [2, 1, 0]])
    if name == 'tetrahedron':
        return np.array([[0, 1, 2], [0, 2, 3], [1, 0, 3], [2, 1, 3]])
    if name == 'cylinder':
        return np.array([
            [0, 1, 2], [2, 1, 4], [2, 4, 3], [3, 4, 5], [3, 5, 0], [0, 5, 1]
        ])
    if name == 'moebius':
        return np.array([
            [0, 1, 2], [2, 1, 4], [2, 4, 3], [3, 4, 5], [3, 5, 1], [1, 5, 0]
        ])
    if name == 'torus':
        # triangulation provided by J. M. Boardman
        A, B, C, D, E, F, G = range(7)
        return np.array([
            [A, F, B], [F, G, B], [B, G, C], [G, A, C],
            [F, D, G], [D, E, G], [G, E, A], [A, E, F],
            [A, B, D], [D, B, E], [E, B, C], [E, C, F], [F, C, D],
            [C, A, D]
        ])
    if name == 'projplane':
        # triangulation provided by A. Aanjaneya & M. Teillaud
        return np.array([
            [3, 4, 1], [1, 4, 5], [1, 5, 2],
            [2, 4, 3], [2, 6, 4], [6, 5, 4], [6, 3, 5], [3, 2, 5],
            [2, 1, 6], [6, 1, 3]
        ]) - 1
    if name == 'kleinbottle':
        # triangulation provided by D. P. Cervone
        A, B, C, D, E, F, G, H, I = range(9)
        return np.array([
            [E, C, F], [F, C, B], [B, C, H], [C, D, H], [H, D, F],
            [E, D, A], [E, A, C], [C, A, G], [C, G, D], [G, E, D],
            [D, F, B], [D, B, A], 
                [A, B, I], [A, I, G], [B, H, I], [I, H, G], 
                                            [G, H, E], [H, F, E]
        ])
    if name == 'hemiicosahedron':
        # https://polytope.miraheze.org/wiki/Hemiicosahedron
        a, b, c, d, e, f = range(6)
        return np.array([
            [a, b, c], 
            [a, c, d], [c, e, d], 
            [c, f, e],
            [b, f, c], [b, d, f],
            [b, d, e],
            [a, b, e], [a, e, f],
            [a, d, f]
        ])
    raise ValueError("mesh '"+name+"' not known.")