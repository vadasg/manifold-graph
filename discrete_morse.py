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
from sage.all import *
import manifolds

triv_grp = SimplicialComplex(-1).homology()[0]


## {{{ http://code.activestate.com/recipes/52560/ (r1)
def unique(s):
    
    n = len(s)
    if n == 0:
        return []

    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()
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

    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u
## end of http://code.activestate.com/recipes/52560/ }}}

def is_empty(simplicial_complex):
    return simplicial_complex.facets() == SimplicialComplex(-1).facets()

def is_constant_simplex(simplex, vertex_order):
    d_min = min([vertex_order[v] for v in simplex.tuple()])
    d_max = max([vertex_order[v] for v in simplex.tuple()])
    return d_min == d_max


def descending_link(simplicial_complex, simplex, vertex_order):
    lk = simplicial_complex.link(simplex)
    verts = list(lk.effective_vertices().tuple())
    d = min([vertex_order[v] for v in simplex.tuple()])
    d_verts = [v for v in verts if vertex_order[v] < d]
    if d_verts:
        return lk.generated_subcomplex(d_verts)
    else:
        return SimplicialComplex(-1)

def constant_complex(simplicial_complex, vertex_order):
    facets = simplicial_complex.facets()
    levels = sorted(unique(vertex_order.values()))
     
    constant_facets = []
    for d in levels:
        for f in facets:
            constant_facet = []
            for v in f:
                if vertex_order[v] == d:
                    constant_facet.append(v)
            constant_facets.append(sorted(constant_facet))
    
    return SimplicialComplex(sorted(unique(constant_facets)))
                   
        
def same_homology(s1, s2):
    if is_empty(s1) != is_empty(s2):
        return False
    #get symmetric difference in homology groups
    diff = s1.homology().viewitems() ^ s2.homology().viewitems()
    diff_grps = [hom_group for (dim, hom_group) in diff]
    if not diff:
        return True
    else:
        return unique(diff_grps) == [triv_grp]

def descending_link_report(simplicial_complex,
                           vertex_order,
                           short_report = False):
    const_complex = constant_complex(simplicial_complex, vertex_order)
    facets = const_complex.facets()
    # sage's cell dictionary has an unneeded final entry
    dims = const_complex.cells().keys()[:-1]
    point = SimplicialComplex([[1]])
      
    nontrivial_links = {}
    for dim in dims:
        nontrivial_links[dim] = []
        for s in const_complex.cells()[dim]:
            dl = descending_link(simplicial_complex, s, vertex_order)
            if (is_empty(dl) or not same_homology(dl, point)):
                nontrivial_links[dim].append((s,dl))

    fmt_string = '  {0:20} {1:22} {2:22}'
    
    if not short_report:
        print fmt_string.format('simplex', 
                                'desc. link homology',
                                'critical simplices')
        print fmt_string.format('-'*20,'-'*22, '-'*22)
    
    morse_complex = {0:0, 1:0, 2:0, 3:0}
    for dim in nontrivial_links.keys():
        for (s, lk) in sorted(nontrivial_links[dim]):
            s_str = str(list(s.tuple()))
            if is_empty(lk):
                h_str = "link empty"
                c_str = str({dim: 1})
                morse_complex[dim] += 1
            elif not same_homology(lk, point):
                hom = lk.homology()
                h_str = str(hom)
                crit_simps = {}
                for hom_dim in hom.keys():
                    num_gens = hom[hom_dim].ngens()
                    if hom[hom_dim].ngens() > 0:
                        crit_simps[dim + hom_dim + 1] = num_gens
                        morse_complex[dim + hom_dim + 1] += num_gens
                c_str = str(crit_simps)
            if not short_report:
                print fmt_string.format(s_str, h_str, c_str)
    print '  discrete Morse complex: ' + str(morse_complex)
    
    is_perfect = True
    for cell_dim in morse_complex:
        hom_gens = simplicial_complex.homology()[cell_dim].ngens()
        if cell_dim == 0:
            hom_gens += 1 #account for sage providing reduced homology
        if morse_complex[cell_dim] !=  hom_gens:
            is_perfect = False
            break
            
    if is_perfect:
        print "  PERFECT morse function produced."
        return True
    else:
        print "  non-perfect morse function produces"
        return False
        
def main():      
    #g_hash = manifolds.graph_hash('manifold_graphs',0)
    g_hash = manifolds.graph_hash('manifold_graphs_small',1)
    #g_hash = manifolds.graph_hash('manifold_graphs_tiny',2)
    g_dict = g_hash.graph_dictionary
    
    num_perfects = 0
    for (indx, m) in enumerate(g_hash.manifolds):
        sc = SimplicialComplex(m)
        dists = g_dict[indx+1][-1]
        base_vertex = 1
        dist_order = dists[base_vertex]

        top_type = str(g_dict[indx+1][1])
        
        print ("manifold #" + str(indx+1) + ", top_type: " 
               + top_type + ", homology: " + str(sc.homology()))
        if descending_link_report(sc, dist_order, short_report = True):
            num_perfects += 1
    
    print ("There were " + str(num_perfects) 
           + " perfect DMFs produced, out of a total of " 
           + str(len(g_hash.manifolds)) + " manifolds.")
               
if __name__ == '__main__':
    main()

