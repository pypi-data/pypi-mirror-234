#ifndef _Union_Find
#define _Union_Find

class UnionFind {
public:
	int n;
	int* parent; // parent[i] = parent of i
	int* size;	 // size[i] = number of sites in tree rooted at i
	int count;	 // number of components
	int* label; // component id

	UnionFind();
	~UnionFind();
	void allocate(int n_);
	void reset();
	void partial_reset(int nb, int* idx);
	int find(int p);
	void mark(int p);
	void unite(int p, int q);
	void insert_labels(int* region, int num);
	bool connected(int p, int q);
	int assign_label(); // overwrite size
	int partial_assign_label(int nb, int* idx); // overwrite size
};
#endif