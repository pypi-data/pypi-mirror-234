
#include <unordered_map>
#include <array>
#include <vector>
#include "unionfind.h"
#include "halfedges.h"

typedef std::unordered_map<long, int> EdgeMap;

/*
The conditions of a simplicial 2-complex being a manifold triangle mesh are:
- Every edge is adjacent to one or two triangles
- The set of triangles adjacent to every vertex form a closed or open fan.

A fan is a collection of triangles sharing a common vertex and chained 
together by a sequence of shared edges 
*/

//-----------------------------------------------------------------------------
class TriSurfTopology {
public:
    // inputs
    int nv_tot; // number of vertices
    int nt_tot; // number of triangles
    int* tri; // triangle indices (size = 3*nt_tot; max value < nv_tot)

    // outputs
    int ne_tot; // number of edges
    int ncomp; // number of connected components
    int* nv; // number of vertices in each connected component
    int* nt; // number of triangles in each connected component
    int* ne; // number of edges in each connected component
    int nbound_tot; // nomber of boundaries
    int* nbound; // number of boundaries in each connected component
    std::vector<int> bound_edges; // boundary edges (pairs of vertices)
    int* bound_path;
    int* bound_path_sep;
    int* bound_path_comp;
    int* oriented; // = 1 if orientation is consistent, = 0 if not
    int* orientable; // = 1 if orientation can be made consistent, = 0 if not
    int* manifold; // = 1 if the component is a 2-manifold, = 0 if not
    int** repaired_orientation;
    std::vector<int> *collapsed_triangles;
    std::vector<int> *nonmanifold_vertices;
    std::vector<int> *nonmanifold_edges;
    TriSurfTopology();
    void initialize(int nt_, int* tri_);
    TriSurfTopology(int nt_, int* tri_);
    ~TriSurfTopology();

    // processing methods
    void determine_topology(); // run all
    int count_vertices(); //> nv_tot
    void identify_connected_components(); //> ncomp, comp, nv (+ allocate)
    void count_triangles(); //> nt, collapsed_triangles, adjtri(1)
    int count_edges(); //> ne, edgemap, oriented, adjtri(2)
    void check_max_two_adjacent_triangles(); //> manifold(1), nonmanifold_edges
    void identify_triangles_incident_to_vertex(); //> edge_loop
    void check_triangle_fan(); // manifold(2), nonmanifold_vertices
    void find_boundary_edges(); //> bound_edges
    void count_boundaries(); //> nbound_tot, nbound, bound_uf
    void follow_boundary_paths(); //> bound_path, bound_path_sep
    void identify_boundary_components(); //> bound_path, bound_path_sep
    void associate_boundary_with_component(); //> bound_path_comp
    void check_orientability();

    // output functions
    int* get_array_ptr(int array_type, int index);
    int get_array_size(int array_type, int index);

//private:
    UnionFind comp;
    EdgeMap edgemap;
    HalfEdgeMap hedgemap;
    std::vector<int> *edge_loop;
    UnionFind bound_uf;
    int* adjtri;
    int insert_edge(int a, int b, int idtri);
    bool all_manifold();
    void depth_first_search(int c, int i, int sign, signed char* visited);
    int count_tri;
};