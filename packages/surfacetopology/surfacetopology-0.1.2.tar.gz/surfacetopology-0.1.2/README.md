### Triangulated compact manifolds

The connectivity of a triangulated surface composed of $n_v$ vertices and $n_t$ triangles can be specified by a 3-by-$n_t$ matrix of vertex indices ranging from 0 to $n_v-1$. Each row contains the index of the three vertices of a triangle. This representation is less general than a simplicial complex, but is more convenient and widespread for large meshes. Note that the vertex positions are not needed since only topological properties are considered.

This triangulation describes a compact manifold surface if and only if:
1. every triangle has 3 distinct vertices;
2. every edge is adjacent to 1 or 2 triangles;
3. the set of triangles adjacent to any vertex forms a closed or open fan.

A fan is a collection of triangles sharing a common vertex and chained 
together by a sequence of shared edges.

### Objective

The purpose of this package is to check if a triangulation satisfies the above conditions and to calculate the basic topological properties such as connectedness, orientability, genus and boundaries that are used for the classification of compact 2-manifolds.

### Examples

The function `surface_topology` separates the connected components and provides for each one some information about the mesh. The attribute ``manifold`` indicates if the conditions are satisfied. The attribute ``genus`` is calculated from the Euler characteristic (``euler``).

```python
>>> import surfacetopology as topo
>>> S1 = topo.small_mesh('tetrahedron')
>>> S1
[[0 1 2]
 [0 2 3]
 [1 0 3]
 [2 1 3]]
>>> topo.surface_topology(S1)
[SurfaceTopology(n_vertices=4, n_edges=6, n_triangles=4, n_boundaries=0,
euler=2, genus=0, manifold=True, oriented=True, closed=True)]
```

If a surface has multiple connected components (here artificially generated using ``disjoint_sum``), a list of ``SurfaceTopology`` objects are returned. When there are isolated vertices, a large number of connected components of size 1 may be generated. In that case, it is useful to call the function ``renumber_vertices`` first.

```python
>>> S2 = topo.small_mesh('torus')
>>> S = topo.disjoint_sum(S1, S2, 10+S1)
>>> len(topo.surface_topology(S))
13
>>> S = topo.renumber_vertices(S)
>>> len(topo.surface_topology(S))
3
```

If a surface is not oriented, the orientability will be checked by attempting to fix the orientation (stored in the attribute ``triangles`` if the surface turns out to be orientable). Here, the Moebius strip is not orientable and has genus 1.

```python
>>> S3 = topo.small_mesh('moebius')
>>> topo.surface_topology(S3)
[SurfaceTopology(n_vertices=6, n_edges=12, n_triangles=6, n_boundaries=1,
euler=0, genus=1, manifold=True, oriented=False, orientable=False, closed=False)]
```

Surfaces with higher genus can be generated using ``connected_sum``

```python
>>> S = topo.connected_sum(S2, S2, S2)
>>> topo.surface_topology(S)
[SurfaceTopology(n_vertices=15, n_edges=57, n_triangles=38, n_boundaries=0,
euler=-4, genus=3, manifold=True, oriented=True, closed=True)]
```

In case ``manifold`` is false, the ``SurfaceTopology`` object contains attributes for trouble-shooting (``nonmanifold_vertices``, ``nonmanifold_edges``, ``collapsed_triangles``).

### Implementation

The code is implemented in C++, interfaced and compiled using ``cython``, and with a wrapper for python (``surfacetopology/wrapper.py``). It was designed for meshes with 100k vertices, but should be appropriate for 1M vertices.

### Installation

Can be installed using the command ``pip install surfacetopology`` (on Windows, a compiler such as Microsoft Visual C++ is required).

Tested using Anaconda 2023.09 (python 3.11) on Linux and Windows.
