#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  discrete_morse.py
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

## {{{ http://code.activestate.com/recipes/52560/ (r1)
def unique(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """

    n = len(s)
    if n == 0:
        return []

    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u
## end of http://code.activestate.com/recipes/52560/ }}}
       
def is_face_of(first_simplex, second_simplex):
    for vertex in first_simplex:
        if not vertex in second_simplex:
            return False
    return True

class SimplicialComplex:
    '''This class represents a finite simplicial complex.\n'''
    
    def __init__(self, simplices):
        self.facets = []
        temp_simplices = unique(sorted(simplices))
        for s in temp_simplices:
            is_facet = True
            for t in temp_simplices:
                if s != t and is_face_of(s, t):
                    is_facet = False
            if is_facet:
                self.facets.append(s)
                    
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

    def get_descending_link(self, simplex, vertex_order):
        if isinstance(simplex, (int, long)):
            simplex = [simplex]
        lk = self.get_link(simplex)
        d = min([vertex_order[v] for v in simplex])
        descending_link_facets = []
        for facet in self.get_link(simplex).facets:
            descending_facet = []
            for vertex in facet:
                if vertex_order[vertex] < d:
                    descending_facet.append(vertex)
            if descending_facet:
                descending_link_facets.append(descending_facet)
        return SimplicialComplex(descending_link_facets)
        
        
        
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
    
    #print tm.get_closed_star(1)
    #print tm.get_link(23)
    #print tm.get_simplices_of_dimension(0)
    #print tm.get_degree(1)

    #print tm.get_descending_link(23, dists[1])
    #print tm.get_descending_link(13, dists)
    #print tm.get_descending_link(23, dists)

    for i in range(30):
        print tm.get_descending_link(i+1, dists[1])
  
if __name__ == '__main__':
    main()

