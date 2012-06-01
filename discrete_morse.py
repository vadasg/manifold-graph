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

import itertools
import manifolds as mfld
       
def is_face_of(first_simplex, second_simplex):
    for vertex in first_simplex:
        if not vertex in second_simplex:
            return False
    return True

class SimplicialComplex:
    '''This class represents a finite simplicial complex.
    
    An object of this class represents a finite simplicial complex with
    vertices given by integers.\n'''
    
    def __init__(self, facets):
        self.facets = sorted(facets)
    
    def get_closed_star(self, simplex):
        if isinstance(simplex, (int, long)):
            simplex = [simplex]
        star = [f for f in self.facets if is_face_of(simplex, f)]
        return SimplicialComplex(star)
        
    def get_link(self, simplex):
        if isinstance(simplex, (int, long)):
            simplex = [simplex]
        link = []
        for facet in self.get_closed_star(simplex).facets:
            new_facet = facet[:]
            for vertex in simplex:
                new_facet.remove(vertex)
            link.append(new_facet)
        return SimplicialComplex(link)
        
    def get_simplices_of_dimension(self, dim):
        simplices = set()
        for facet in self.facets:
            s = set(itertools.combinations(facet, dim+1))
            simplices = simplices.union(s)
        return map(list, sorted(simplices))
    
    def __str__(self):
        return "Simplicial complex with facets: " + str(self.facets)

        
class ThreeManifold(SimplicialComplex):
    '''This class represents a compact combinatorial 3-manifold.
    
    An object of this class represents a compact combinatorial
    3-manifold with vertices given by integers.\n'''
    
    def __init__(self, facets):
        SimplicialComplex.__init__(self, facets)
        # to do: code to check that link of each vertex is 2-sphere
        
    def get_degree(self, simplex):
        return len(self.get_closed_star(simplex).facets)


    def __str__(self):
        return "3-manifold with facets: " + str(self.facets)
        
def main():
    sc = SimplicialComplex([[1,2],[2,3,4],[3,4,5]])
       
    gh = mfld.graph_hash('manifold_graphs_tiny.dat',2)
    gd = gh.graph_dictionary   
    dists = gd[1][-1]
    m = gh.manifolds[0]
    tm = ThreeManifold(m)
    
    vertices = dists.keys()
    base_vertex = 1
    
    print tm.get_closed_star(1)
    print tm.get_link(1)
    print tm.get_simplices_of_dimension(2)
    print tm.get_degree(1)

    
    for v in vertices:
        d = dists[base_vertex][v]
        lk = tm.get_link(v).facets
        lk_verts = mfld.get_vertices(lk)
        ds = [w for w in lk_verts if dists[base_vertex][w] < d]
        #print ds
    return 0

if __name__ == '__main__':
	main()

