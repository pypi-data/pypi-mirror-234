#ifndef _Half_Edge_Map
#define _Half_Edge_Map

//-----------------------------------------------------------------------------
class HalfEdgeMap {
public:
    int nv, nt, ne;
    int* tri;
    int* sep;
    int* key;
    int* val;
    
    HalfEdgeMap() {}
    ~HalfEdgeMap();

    void allocate(int nv_, int nt_, int* tri_);
    int index(int a, int b);
    int insert(int a, int b, int v);
    int insert_at(int idx, int b, int v);

    void find_negative_values(std::vector<int> &list);
    void find_values_larger_than_two(std::vector<int> *lists, 
                                     int* id_list, int* flag);
};

#endif