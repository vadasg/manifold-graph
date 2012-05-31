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

def main():
    gh = mfld.graph_hash('manifold_graphs_small.dat', 1)
    gd = gh.graph_dictionary

    manifold_id = 23
    base_vertex = 1
    
    dists = gd[manifold_id][-1]
    m = gh.manifolds[manifold_id - 1]
    print m
    
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

