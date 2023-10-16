// Weighted Quick-Union with path compression
// based on code by Robert Sedgewick and Kevin Wayne
#include <stdlib.h>
#include <stdio.h>
#include "unionfind.h"

UnionFind::UnionFind() {
	n = count = 0;
	parent = size = label = NULL;
}

void UnionFind::allocate(int n_) {
	n = n_;
	parent = new int [n];
	size = new int [n];
	label = new int [n];
}

UnionFind::~UnionFind()
{
	delete [] parent;
	delete [] size;
	delete [] label;
}

void UnionFind::reset()
{
	for (int i = 0; i < n; i++) {
		parent[i] = i;
		size[i] = 1;
		label[i] = -1;
	}
	count = n;
}

void UnionFind::partial_reset(int nb, int* idx)
{
	for (int j = 0; j < nb; j++) {
		int i = idx[j];
		parent[i] = i;
		size[i] = 1;
		label[i] = -1;
	}
	count = nb;
}

int UnionFind::find(int p) {
	int root = p;
	while (root != parent[root])
		root = parent[root];
	while (p != root) {
		int newp = parent[p];
		parent[p] = root;
		p = newp;
	}
	return root;
}

void UnionFind::mark(int p) {
	label[p] = 0;
}

void UnionFind::unite(int p, int q) {
	int rootP = find(p);
	int rootQ = find(q);
	label[p] = label[q] = 0;
	if (rootP == rootQ) return;

	// make smaller root point to larger one
	if (size[rootP] < size[rootQ]) {
		parent[rootP] = rootQ;
		size[rootQ] += size[rootP];
	}
	else {
		parent[rootQ] = rootP;
		size[rootP] += size[rootQ];
	}
	count--;
}

bool UnionFind::connected(int p, int q) {
	return find(p) == find(q);
}

void UnionFind::insert_labels(int* region, int num)
{
	if (num <= 0) return;
	int* idx = new int [num];
	for (int i = 0; i < num; i++) idx[i] = -1;
	for (int i = 0; i < n; i++) if (region[i] >= 0) {
		if (idx[region[i]] < 0) {
			mark(i);
			idx[region[i]] = i;
		} else {
			unite(i, idx[region[i]]);
		}
	}
	delete [] idx;
}

int UnionFind::assign_label()
{
	int i, max_label = 0;
	for (i = 0; i < n; i++) size[i] = -1;
	for (i = 0; i < n; i++) { //if (label[i] >= 0) { because of isolated vertices
		int p = find(i);
		if (size[p] < 0) size[p] = max_label++;
		label[i] = size[p];
	}
	return max_label;
}

int UnionFind::partial_assign_label(int nb, int* idx)
{
	int max_label = 0;
	for (int j = 0; j < nb; j++) {
		int i = idx[j];
		size[i] = -1;
	}
	for (int j = 0; j < nb; j++) {
		int i = idx[j];
		if (label[i] >= 0) {
			int p = find(i);
			if (size[p] < 0) size[p] = max_label++;
			label[i] = size[p];
		}
	}
	return max_label;
}


	 
