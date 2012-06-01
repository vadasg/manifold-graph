#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Aaron Trout, Vadas Gintautas
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import manifolds as mfld

def get_faces(simplex):
    if isinstance(simplex, (int, long)):
        simplex = [simplex]
    

class SimplicialComplex:
    '''This class represents a finite simplicial complex.
    
    An object of this class represents a finite simplicial complex with
    vertices given by integers.\n'''
    
    def __init__(self, facets):
        self.facets = facets
    
    def get_star(self, simplex):
        if isinstance(simplex, (int, long)):
            simplex = [simplex]
        facets_in_star=[]
        for facet in self.facets:
            facet_in_star = True
            for vertex in simplex:
                if not vertex in facet:
                    facet_in_star = False
                    break
            if facet_in_star:
                facets_in_star.append(facet)
        return facets_in_star
        
        
class ThreeManifold(SimplicialComplex):
    '''This class represents a compact combinatorial 3-manifold.
    
    An object of this class represents a compact combinatorial
    3-manifold with vertices given by integers.\n'''
    
    def __init__(self, facets):
        SimplicialComplex.__init__(self, facets)
        # to do: code to check that link of each vertex is 2-sphere

def main():
    sc = SimplicialComplex([[1,2],[2,3,4],[3,4,5]])
    tm = ThreeManifold([[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5],
        [1, 3, 4, 5], [2, 3, 4, 6], [2, 3, 5, 7], [2, 3, 6, 7],
        [2, 4, 5, 8], [2, 4, 6, 8], [2, 5, 7, 8], [2, 6, 7, 9],
        [2, 6, 8, 9], [2, 7, 8, 9], [3, 4, 5, 10], [3, 4, 6, 10],
        [3, 5, 7, 10], [3, 6, 7, 11], [3, 6, 10, 11], [3, 7, 10, 11],
        [4, 5, 8, 10], [4, 6, 8, 12], [4, 6, 10, 12], [4, 8, 10, 12],
        [5, 7, 8, 10], [6, 7, 9, 11], [6, 8, 9, 12], [6, 9, 11, 12],
        [6, 10, 11, 12], [7, 8, 9, 13], [7, 8, 10, 13], [7, 9, 11, 13],
        [7, 10, 11, 13], [8, 9, 12, 13], [8, 10, 12, 13],
        [9, 11, 12, 14], [9, 11, 13, 14], [9, 12, 13, 14],
        [10, 11, 12, 13], [11, 12, 13, 14]])
    
    print tm.get_star([2])
       
    gh = mfld.graph_hash('manifold_graphs_small.dat',1)
    gd = gh.graph_dictionary

    manifold_id = 23
    base_vertex = 1
    
    dists = gd[manifold_id][-1]
    m = gh.manifolds[manifold_id - 1]
    
    vertices = dists.keys()
    print vertices
    for v in vertices:
        d = dists[base_vertex][v]
        lk = mfld.get_link(v, m)
        lk_verts = mfld.get_vertices(lk)
        ds = [w for w in lk_verts if dists[base_vertex][w] < d]
        print ds
    return 0

if __name__ == '__main__':
	main()

