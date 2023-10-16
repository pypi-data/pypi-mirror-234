#include <math.h>
#include <cassert>

#include "trisurftopology.h"
#include "unionfind.cpp"
#include "halfedges.cpp"

#ifdef BENCH
    #include <stdio.h>
    #include <time.h>
    clock_t start_time;
    void tic()
    {
        start_time = clock();
    }
    void toc(const char* name)
    {
        clock_t end_time = clock();
        printf("%30s [%.3f s]\n", name, 
               (double)((end_time - start_time))/CLOCKS_PER_SEC);
        tic();
    }
#else
    #define tic() {}
    #define toc(name) {}
#endif

//-----------------------------------------------------------------------------
TriSurfTopology::TriSurfTopology()
{
    nv_tot = 0;
    nt_tot = 0;
    tri = NULL;
}

//-----------------------------------------------------------------------------
void TriSurfTopology::initialize(int nt_, int* tri_)
{
    nv_tot = 0;
    nt_tot = nt_;
    tri = tri_;
}

//-----------------------------------------------------------------------------
TriSurfTopology::TriSurfTopology(int nt_, int* tri_)
{
    initialize(nt_, tri_);
}

//-----------------------------------------------------------------------------
TriSurfTopology::~TriSurfTopology()
{
    tic();
    for (int c=0;c<ncomp;c++)
        delete [] repaired_orientation[c];
    delete [] repaired_orientation;

    delete [] nv;
    delete [] nt;
    delete [] ne;
    delete [] nbound;
    delete [] oriented;
    delete [] orientable;
    delete [] manifold;
    delete [] edge_loop;
    delete [] collapsed_triangles;
    delete [] nonmanifold_vertices;
    delete [] nonmanifold_edges;
    delete [] bound_path;
    delete [] bound_path_sep;
    delete [] bound_path_comp;
    delete [] adjtri;
    toc("destructor");
}

//-----------------------------------------------------------------------------
bool TriSurfTopology::all_manifold()
{
    for (int c=0;c<ncomp;c++)
        if (!manifold[c]) return 0;
    return 1;
}

//-----------------------------------------------------------------------------
void TriSurfTopology::determine_topology()
{
    tic();
    nv_tot = count_vertices();
    toc("count vertices");
    identify_connected_components();
    toc("connected components");
    count_triangles();
    toc("count triangles");
    ne_tot = count_edges();
    toc("count edges");
    check_max_two_adjacent_triangles();
    toc("check adjacent triangles");
    identify_triangles_incident_to_vertex();
    toc("check incident triangles");
    check_triangle_fan();
    toc("check triangle fans");
    find_boundary_edges();
    toc("find boundary edges");
    count_boundaries();
    toc("count boundaries");
    if (all_manifold())
        follow_boundary_paths();
    else
        identify_boundary_components();
    associate_boundary_with_component();
    toc("identify boundaries");
    check_orientability();
    toc("check orientability");
}

//-----------------------------------------------------------------------------
int TriSurfTopology::count_vertices() //> nv_tot
{
    int maxid = -1;
    for (int i=0;i<3*nt_tot;i++)
        if (tri[i] > maxid) maxid = tri[i];
    return maxid+1;
}

//-----------------------------------------------------------------------------
void TriSurfTopology::identify_connected_components() //> ncomp, comp, nv
{
    comp.allocate(nv_tot);
    comp.reset();
    for (int i=0;i<nt_tot;i++) {
        comp.unite(tri[3*i], tri[3*i+1]);
        comp.unite(tri[3*i], tri[3*i+2]);
        comp.unite(tri[3*i+1], tri[3*i+2]);
    }
    ncomp = comp.assign_label();

    nv = new int [ncomp];
    nt = new int [ncomp];
    ne = new int [ncomp];
    nbound = new int [ncomp];
    oriented = new int [ncomp];
    manifold = new int [ncomp];
    collapsed_triangles = new std::vector<int> [ncomp];
    nonmanifold_vertices = new std::vector<int> [ncomp];
    nonmanifold_edges = new std::vector<int> [ncomp];

    for (int c=0;c<ncomp;c++) {
        nv[c]= 0;
        manifold[c] = 1;
    }
    for (int i=0;i<nv_tot;i++)
        nv[comp.label[i]]++;
}

//-----------------------------------------------------------------------------
void TriSurfTopology::count_triangles() //> nt, collapsed_triangles, adjtri(1)
{
    for (int c=0;c<ncomp;c++)
        nt[c] = 0;
    for (int i=0;i<nt_tot;i++) {
        int v0 = tri[3*i], v1 = tri[3*i+1], v2 = tri[3*i+2];
        int c = comp.label[v0];
        if ((v0 == v1) | (v1 == v2) | (v2 == v0)) {
            collapsed_triangles[c].push_back(i);
            manifold[c] = 0;
        }
        nt[c]++;
    }

    adjtri = new int [3*nt_tot];
    for (int i=0;i<3*nt_tot;i++)
        adjtri[i] = -1;
}

//-----------------------------------------------------------------------------
#define INSERT_ADJTRI(i,j) { \
    int m = (adjtri[3*i] >= 0) + (adjtri[3*i+1] >= 0); \
    adjtri[3*i+m] = j; \
}

//-----------------------------------------------------------------------------
int TriSurfTopology::insert_edge(int a, int b, int idtri)
// returns the number of edges added
{
    int idx_direct = hedgemap.index(a, b);
    if (idx_direct >= 0) { // inconsistent orientation
        int idtri0 = -hedgemap.val[idx_direct];
        if (idtri0 >= 0) {
            INSERT_ADJTRI(idtri0, idtri);
            INSERT_ADJTRI(idtri, idtri0);
            hedgemap.val[idx_direct] = 2;
        } else
            hedgemap.val[idx_direct]++;
        int c = comp.label[a];
        oriented[c] = 0;
        return 0;
    }
    int idx_reverse = hedgemap.index(b, a);
    if (idx_reverse >= 0) { // reverse edge already inserted
        int idtri0 = -hedgemap.val[idx_reverse];
        if (idtri0 >= 0) {
            INSERT_ADJTRI(idtri0, idtri);
            INSERT_ADJTRI(idtri, idtri0);
            hedgemap.val[idx_reverse] = 2;
        } else
            hedgemap.val[idx_reverse]++;
        return 0;
    }
    // new edge, give an initial value <= 0
    hedgemap.insert_at(idx_direct, b, -idtri);
    return 1;
}

//-----------------------------------------------------------------------------
int TriSurfTopology::count_edges() //> ne, edgemap, oriented, adjtri(2)
{
    for (int c=0;c<ncomp;c++) {
        ne[c] = 0;
        oriented[c] = 1;
    }

    hedgemap.allocate(nv_tot, nt_tot, tri);
    for (int i=0;i<nt_tot;i++) {
        int v0 = tri[3*i], v1 = tri[3*i+1], v2 = tri[3*i+2];
        int c = comp.label[v0];
        ne[c] += insert_edge(v0, v1, i)
               + insert_edge(v1, v2, i)
               + insert_edge(v2, v0, i);
    }
    return hedgemap.ne;
}

//-----------------------------------------------------------------------------
void TriSurfTopology::check_max_two_adjacent_triangles()
//> manifold(1), nonmanifold_edges
{
    hedgemap.find_values_larger_than_two(nonmanifold_edges, 
                                         comp.label, manifold);
}

//-----------------------------------------------------------------------------
void TriSurfTopology::identify_triangles_incident_to_vertex() //> edge_loop
{
    edge_loop = new std::vector<int> [nv_tot];
    for (int i=0;i<nv_tot;i++)
        edge_loop[i].reserve(16);
    
    for (int i=0;i<nt_tot;i++) {
        int a = tri[3*i], b = tri[3*i+1], c = tri[3*i+2];
        edge_loop[a].push_back(b); edge_loop[a].push_back(c);
        edge_loop[b].push_back(c); edge_loop[b].push_back(a);
        edge_loop[c].push_back(a); edge_loop[c].push_back(b);
    }
}

//-----------------------------------------------------------------------------
void TriSurfTopology::check_triangle_fan() // manifold(2), nonmanifold_vertices
{
    UnionFind uf;
    uf.allocate(nv_tot);
    for (int i=0;i<nv_tot;i++) {
        int* idx = edge_loop[i].data();
        int nb = edge_loop[i].size();
        if (nb <= 2) continue;

        // link the edges of the edge loop
        uf.partial_reset(nb, idx);
        for (int k=0;k<nb/2;k++)
            uf.unite(idx[2*k], idx[2*k+1]);
        
        // check if there is only one connected component
        int p = uf.find(idx[0]);
        for (int k=2;k<nb;k+=2) {
            if (uf.find(idx[k]) != p) {
                int c = comp.label[i];
                manifold[c] = 0;
                nonmanifold_vertices[c].push_back(i);
                break;
            }
        }
    }
}

//-----------------------------------------------------------------------------
void TriSurfTopology::find_boundary_edges() //> bound_edges
{
    hedgemap.find_negative_values(bound_edges);
}

//-----------------------------------------------------------------------------
void TriSurfTopology::count_boundaries() //> nbound_tot, nbound, bound_uf
{
    // separate the connected components of boundary edges
    bound_uf.allocate(nv_tot);
    int* v = bound_edges.data();
    int m = bound_edges.size();
    for (int i=0;i<nv_tot;i++) bound_uf.label[i] = -1; // reset all labels
    bound_uf.partial_reset(m, v);
    for (int i=0;i<m;i+=2)
        bound_uf.unite(v[i], v[i+1]);
    nbound_tot = bound_uf.partial_assign_label(m, v);

    // associate boundaries with the connected component they belong to
    int* bound_comp = new int [nbound_tot];
    for (int i=0;i<nbound_tot;i++)
        bound_comp[i] = -1;
    for (int i=0;i<m;i+=2) {
        int j = v[i];
        bound_comp[bound_uf.label[j]] = comp.label[j];
    }

    // count boundaries for each connected component of the mesh
    for (int i=0;i<ncomp;i++)
        nbound[i] = 0;
    for (int i=0;i<nbound_tot;i++)
        nbound[bound_comp[i]]++;

    delete [] bound_comp;
}

//-----------------------------------------------------------------------------
int follow_path(int v0, int v1, int* next_vertex, bool* visited, int* path)
{
    int current = v1;
    int size = 2;
    visited[v0] = visited[v1] = 1;
    path[0] = v0;
    path[1] = v1;
    while (1) {
        int next = next_vertex[2*current];
        if (visited[next]) next = next_vertex[2*current+1];
        if (visited[next]) return size;
        path[size++] = current = next;
        visited[current] = 1;
    }
}

//-----------------------------------------------------------------------------
void TriSurfTopology::follow_boundary_paths() //> bound_path, bound_path_sep
{ 
    // lookup table for the next step along the boundaries
    int* v = bound_edges.data();
    int m = bound_edges.size();
    int* next_vertex = new int [2*nv_tot];
    for (int i=0;i<2*nv_tot;i++)
        next_vertex[i] = -1;
    for (int i=0;i<m;i+=2) {
        int a = v[i], b = v[i+1];
        next_vertex[2*a + (next_vertex[2*a]>=0)] = b;
        next_vertex[2*b + (next_vertex[2*b]>=0)] = a;
    }

    // allocate boundary paths
    bound_path = new int [m];
    bound_path_sep = new int [nbound_tot+1];
    for (int i=0;i<=nbound_tot;i++)
        bound_path_sep[i] = 0;
    
    bool* visited = new bool [nv_tot];
    for (int i=0;i<nv_tot;i++)
        visited[i] = 0;

    // follow path along boundaries
    int npath = 0;
    while (1) {
        int i;
        for (i=0;i<m;i+=2) 
            if (!visited[v[i]]) break;
        if (i >= m) break;
        int len = follow_path(v[i], v[i+1], next_vertex, visited, 
                              bound_path + bound_path_sep[npath]);
        bound_path_sep[npath+1] = bound_path_sep[npath] + len;
        npath++;
    }

    delete [] next_vertex;
    delete [] visited;
}

//-----------------------------------------------------------------------------
void TriSurfTopology::identify_boundary_components() 
//> bound_path, bound_path_sep
{
    int* label = bound_uf.label;

    // allocate boundary paths
    bound_path = new int [bound_edges.size()];
    bound_path_sep = new int [nbound_tot+1];
    
    // compute boundary sizes
    for (int i=0;i<=nbound_tot;i++)
        bound_path_sep[i] = 0;
    for (int i=0;i<nv_tot;i++)
        if (label[i] >= 0) 
            bound_path_sep[label[i]+1]++;

    // compute separators
    for (int c=2;c<=nbound_tot;c++)
        bound_path_sep[c] += bound_path_sep[c-1];
    bound_path_sep[0] = 0;
    
    // fill vertex id
    int* pos = new int [nbound_tot];
    for (int c=0;c<nbound_tot;c++)
        pos[c] = bound_path_sep[c];
    for (int i=0;i<nv_tot;i++)
        if (label[i] >= 0)
            bound_path[pos[label[i]]++] = i;
    delete [] pos;
}

//-----------------------------------------------------------------------------
void TriSurfTopology::associate_boundary_with_component()
{
    bound_path_comp = new int [nbound_tot];
    for (int c=0;c<nbound_tot;c++) {
        int v0 = bound_path[bound_path_sep[c]];
        bound_path_comp[c] = comp.label[v0];
    }
}

//-----------------------------------------------------------------------------
inline int consistent_orientation(int i1, int i2, int i3, 
                                  int j1, int j2, int j3)
{
    // 0 = error; 1 = consistent orientation; -1 = reversed orientation
    signed char table[] = {0, 0, 0, 0, 0, 0, -1, 1, 0, 1, 0, -1, 0, -1, 1, 0, 
                           0, 0, 1, -1, 0, 0, 0, 0, -1, 0, 0, -1, 1, 0, 1, 0, 
                           0, -1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, -1, -1, 0, 0, 
                           0, 1, -1, 0, -1, 0, -1, 0, 1, 1, 0, 0, 0, 0, 0, 0};
    int k1 = (i1 == j1) + 2*(i1 == j2) + 3*(i1 == j3);
    int k2 = (i2 == j1) + 2*(i2 == j2) + 3*(i2 == j3);
    int k3 = (i3 == j1) + 2*(i3 == j2) + 3*(i3 == j3);
    int code = k1*16 + k2*4 + k3;
    return table[code];
}

//-----------------------------------------------------------------------------
void TriSurfTopology::depth_first_search(int c, int i, int sign, 
                                         signed char* visited)
{
    visited[i] = sign;
    int* T = repaired_orientation[c] + 3*count_tri;
    T[0] = tri[3*i];
    if (sign > 0) {
        T[1] = tri[3*i+1]; T[2] = tri[3*i+2]; // consistent orientation
    } else {
        T[1] = tri[3*i+2]; T[2] = tri[3*i+1]; // reverse orientation
    }
    count_tri++;

    for (int a=0;a<3;a++) {
        int j = adjtri[3*i+a];
        if (j < 0) break;
        int check = consistent_orientation(tri[3*i], tri[3*i+1], tri[3*i+2],
                                           tri[3*j], tri[3*j+1], tri[3*j+2]);
        if ((visited[j] == 0) && (check != 0))
            depth_first_search(c, j, sign*check, visited);
        else {
            if (check != sign*visited[j]) orientable[c] = 0;
        }
    }
}

//-----------------------------------------------------------------------------
void TriSurfTopology::check_orientability()
{
    orientable = new int [ncomp];
    repaired_orientation = new int* [ncomp];
    signed char* visited = new signed char [nt_tot];
    for (int i=0;i<nt_tot;i++)
        visited[i] = 0;
    
    for (int c=0;c<ncomp;c++) {
        orientable[c] = manifold[c] ? 1 : oriented[c];
        repaired_orientation[c] = new int [3*nt[c]];
        count_tri = 0;

        if (nt[c] == 0)
            continue;

        if (oriented[c] || !manifold[c]) {
            for (int i=0;i<nt_tot;i++) if (comp.label[tri[3*i]] == c) {
                int* T = repaired_orientation[c] + 3*(count_tri++);
                T[0] = tri[3*i]; T[1] = tri[3*i+1]; T[2] = tri[3*i+2];
            }
            continue;
        }

        int i;
        // find initial triangle
        for (i=0;i<nt_tot;i++) if (comp.label[tri[3*i]] == c) break;
        depth_first_search(c, i, +1, visited);
    }
    delete [] visited;
}

//-----------------------------------------------------------------------------
int* TriSurfTopology::get_array_ptr(int array_type, int index)
{
    if (ncomp == 0) return NULL;
    if (array_type == 0) return comp.label;
    if (array_type == 1) return collapsed_triangles[index].data();
    if (array_type == 2) return nonmanifold_vertices[index].data();
    if (array_type == 3) return nonmanifold_edges[index].data();
    if (array_type == 4) return repaired_orientation[index];
    return NULL;
}

//-----------------------------------------------------------------------------
int TriSurfTopology::get_array_size(int array_type, int index)
{
    if (ncomp == 0) return 0;
    if (array_type == 0) return nv_tot;
    if (array_type == 1) return collapsed_triangles[index].size();
    if (array_type == 2) return nonmanifold_vertices[index].size();
    if (array_type == 3) return nonmanifold_edges[index].size();
    if (array_type == 4) return 3*nt[index];
    return 0;
}