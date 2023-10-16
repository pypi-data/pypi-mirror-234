
#include <vector>
#include "halfedges.h"

//-----------------------------------------------------------------------------
void HalfEdgeMap::allocate(int nv_, int nt_, int* tri_)
{
    nv = nv_;
    nt = nt_;
    ne = 0;
    tri = tri_;
    sep = new int [nv+1];

    for (int i=0;i<nv+1;i++)
        sep[i] = 0;
    for (int i=0;i<3*nt;i++)
        sep[tri[i]+1]++;
    for (int i=0;i<nv;i++)
        sep[i+1] += sep[i];
    sep[0] = 0;

    key = new int [sep[nv]];
    val = new int [sep[nv]];
    for (int i=0;i<sep[nv];i++)
        key[i] = -1;
}

//-----------------------------------------------------------------------------
int HalfEdgeMap::index(int a, int b)
{
    for (int i=sep[a];i<sep[a+1];i++) {
        if (key[i] == -1) return -1-i;
        if (key[i] == b) return i;
    }
    return -1;
}

//-----------------------------------------------------------------------------
int HalfEdgeMap::insert(int a, int b, int v)
{
    for (int i=sep[a];i<sep[a+1];i++) {
        if (key[i] == -1) {
            key[i] = b;
            val[i] = v;
            ne++;
            return 1;
        }
    }
    return 0;
}

//-----------------------------------------------------------------------------
int HalfEdgeMap::insert_at(int idx, int b, int v)
{
    int i = -idx-1;
    key[i] = b;
    val[i] = v;
    ne++;
    return 1;
}

//-----------------------------------------------------------------------------
void HalfEdgeMap::find_negative_values(std::vector<int> &list)
{
    for (int a=0;a<nv;a++) {
        for (int i=sep[a];i<sep[a+1];i++) {
            int b = key[i];
            if (b < 0) break;
            if (val[i] <= 0) {
                list.push_back(b);
                list.push_back(a);
            }
        }
    }
}

//-----------------------------------------------------------------------------
void HalfEdgeMap::find_values_larger_than_two(std::vector<int> *lists, 
                                              int* id_list, int* flag)
{
    for (int a=0;a<nv;a++) {
        for (int i=sep[a];i<sep[a+1];i++) {
            int b = key[i];
            if (b < 0) break;
            if (val[i] > 2) {
                int j = id_list[a];
                flag[j] = 0;
                lists[j].push_back(a);
                lists[j].push_back(b);
            }
        }
    }
}

//-----------------------------------------------------------------------------
HalfEdgeMap::~HalfEdgeMap()
{
    delete [] sep;
    delete [] key;
    delete [] val;
}
