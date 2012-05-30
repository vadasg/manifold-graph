import networkx, os
import matplotlib.pyplot as plt
import cPickle

edge_weight = 1
hop_weight = (8.0/3.0)**(0.5)
jump_weight = (3.0)**(0.5) + 0.5*((2.0)**(0.5))

#object for hashing graph data and doing statistics across graphs

class graph_hash(object):
    """graph_hash object
    debug levels:
    debug == 0: no debug. use full set.
    debug == 1: use the first 100 manifolds as a test set
    debug == 2: use 1 simple manifold as a test
    """
    def __init__(self,graph_dictionary_file_name,debug = 0):

        self.graph_dictionary_file_name = graph_dictionary_file_name
        self.debug = debug
        self.diameter_file_name = 'diameters_' + self.graph_dictionary_file_name

        if self.debug:
            print 'Debug level:', debug
            self.diameter_file_name = 'diameters_' + self.diameter_file_name
            self.graph_dictionary_file_name = 'debug_' + self.graph_dictionary_file_name
            self.clean()

        self.manifold_file_name = 'input.txt'
        self.manifold_type_file_name = 'manifolds_lex_d3_deg5.type.txt'

        #initialize by building manifolds,graphs,and diameters
        self.manifolds = self.get_manifolds()
        self.graph_dictionary = self.load_dictionary()

    def clean(self):
        #removes hashed files
        #prompt first for safety
        while True:
            sure = raw_input('Delete hashed data (y/n)?')
            if 'y' in sure.lower():
                os.system('rm -f ' + self.graph_dictionary_file_name)
                os.system('rm -f ' + self.diameter_file_name)
                break
            elif 'n' in sure.lower():
                break


    def get_manifolds(self):
        #read in raw file
        f = open(self.manifold_file_name,'r')
        manifolds = f.read()
        f.close()
        #fix dumb line splitting 
        manifolds = manifolds.replace(',\n',',').replace('\n\n','\n').replace('\n]',']') 
        
        end = -1
        
        if self.debug == 2: #deeper debug level -- only 1 manifold
            manifolds = [[[1,2,3,4],[1,3,4,5],[2,3,4,6],
                [3,4,5,7],[3,4,6,7],[3,6,7,9],
                [4,6,7,8],[6,7,8,10],[6,7,9,10]]]
            return manifolds

        elif self.debug == 1:  #simple debug level
            end = 101 # only run on first 100 manifolds

        #remove spurious newlines at end and beginning
        manifolds =  manifolds.split('\n')[1:end] 

        for i in range(len(manifolds)):
            manifolds[i]=  manifolds[i][manifolds[i].find('['):] #remove labels and text
            manifolds[i] = eval('list(' +manifolds[i] + ')') #turn into a python list
        
        return manifolds


    def build_dictionary(self):
        f = open(self.manifold_type_file_name ,'r')
        types = f.readlines()
        f.close()
        self.graph_dictionary = {}
        for i in range(len(self.manifolds)):
            t = types[i].split()[-1]
            manifold = self.manifolds[i]
            vertices,edges = get_graph(manifold)
            g = get_weighted_graph(manifold,vertices,edges)
            dists = networkx.all_pairs_dijkstra_path_length(g)
            d = get_diameter_from_dists(dists)
            self.graph_dictionary[i+1] = (g,t,d,dists)
            print (i+1), t, pretty_print(d)
        return self.graph_dictionary

    def load_dictionary(self):
        try:
            print 'loading dictionary from ' + self.graph_dictionary_file_name
            f = open(self.graph_dictionary_file_name,'rb')
            self.graph_dictionary = cPickle.load(f)
            f.close()
            print 'dictionary loaded!'
        except:
            print 'dictionary not found. building dictionary'
            self.graph_dictionary = self.build_dictionary()
            self.save_dictionary()
        return self.graph_dictionary

    def save_dictionary(self):
            f = open(self.graph_dictionary_file_name,'wb')
            cPickle.dump(self.graph_dictionary,f)
            f.close()

#misc functions for making things nicer

def sorted_set(x):
    return sorted(set(x))

def pretty_print(dist):
    dist_dictionary = {}
    max_edges = int(dist / edge_weight) + 1
    max_hops = int(dist / hop_weight) + 1
    max_jumps = int(dist / jump_weight) + 1
    for edges in range(0,max_edges):
        for hops in range(0, max_hops):
            for jumps in range(0, max_jumps):
                d = edges*edge_weight + hops*hop_weight + jumps*jump_weight
                if abs(d-float(dist)) < 0.000000001:
                    out_string = ''
                    if (edges > 0):
                        out_string += str(edges) + 'E '
                    if (hops > 0):
                        out_string += str(hops) + 'H '
                    if (jumps > 0):
                        out_string += str(jumps) + 'J'
                    return out_string
    return str(dist)

def get_pairs(input_list):
	return [(x,y) for y in input_list for x in input_list if x != y]

#functions for manifolds.  refactor?		

def traverse_edge(edge, start_vertex):
    next_edge = list(edge)
    next_edge.remove(start_vertex)
    return next_edge[0]

def get_vertices_around_circle(circle, start_vertex):
    edges = circle[:]
    vertices = [start_vertex]
    next_vertex = start_vertex
    while len(edges) > 1:
        next_edge = [x for x in edges if (next_vertex in x)][0]
        next_vertex = traverse_edge(next_edge, next_vertex)
        edges.remove(next_edge)
        vertices.append(next_vertex)
    return vertices

def get_opposite_simplex_in_circle(circle, simplex):
	if isinstance(simplex, (int, long)):
		simplex = [simplex]
	vertices = get_vertices_around_circle(circle, simplex[0])
	num_edges = len(circle)
	diam = num_edges / 2
	if len(simplex)==2:
		other_index = vertices.index(simplex[1])
		if num_edges % 2 == 0:
			if other_index == (num_edges - 1):
				return [vertices[diam-1], vertices[diam]]
			elif other_index == 1:
				return [vertices[diam], vertices[diam+1]]
		if num_edges % 2 == 1:
			if other_index == (num_edges - 1):
				return vertices[diam]
			elif other_index == 1:
				return vertices[diam+1]
	elif len(simplex)==1:
		if num_edges % 2 == 0:
			return vertices[diam]
		if num_edges % 2 == 1:
			return [vertices[diam], vertices[diam+1]]
	else:
		sys.exit("wrong dimension simplex")

def get_link(simplex, manifold):
    if isinstance(simplex, (int, long)):
		simplex = [simplex]
    link = []
    for facet in get_star(simplex, manifold):
        new_facet = facet[:]
        for vertex in simplex:
            new_facet.remove(vertex)
        link.append(new_facet)
    return link

def get_star(simplex, manifold):
    if isinstance(simplex, (int, long)):
		simplex = [simplex]
    facets_in_star=[]
    for facet in manifold:
    	facet_in_star = True
        for vertex in simplex:
    	    if not vertex in facet:
        		facet_in_star = False
        		break
        if facet_in_star:
    	    facets_in_star.append(facet)
    return facets_in_star


#functions for graphs. refactor?

def get_vertices(manifold):
    #get list of all vertices that appear in the manifold
    return sorted_set([vertex for simplex in manifold for vertex in simplex])

def get_graph(manifold):
    #first get all vertices
    vertices = get_vertices(manifold)
    #now get all edges by getting all edges in each simplex
    edges = []
    for simplex in manifold:
        edges += get_pairs(simplex) 
    edges = sorted_set(edges)
    return vertices,edges

def get_degree(simplex,manifold):
    return len(get_star(simplex,manifold))

def get_hops(manifold,vertices,edges):
    #now do hops
    hops = []
    for v1 in vertices:
        check_in = [simplex for simplex in manifold if v1 in simplex]
        for ci in check_in:
            for v2 in vertices:
                 if (v1 != v2):
                    test_simplex = ci[:]
                    if v2 not in test_simplex:
                        test_simplex[test_simplex.index(v1)] = v2
                        test_simplex.sort()
                        if test_simplex in manifold:
                            hops.append(tuple(sorted([v1,v2])))
    return sorted_set(hops)

def get_jumps(manifold,vertices,edges,hops):
    #get edges that have degree 5
    link_dictionary = {}
    degree_5_edges = []
    for e in edges:
        if get_degree(e,manifold) == 5:
            degree_5_edges.append(e)
            simplex_list = get_star(e,manifold)
            link_dictionary[e] = get_link(e,manifold)

    jumps = []
    if len(degree_5_edges) >0:
        check_simplices = []
        edge_pairs  = get_pairs(degree_5_edges)
        for pair in edge_pairs:
            check_vertices =  get_vertices(pair)
            if len(check_vertices) == 4:
                test_simplex = sorted(check_vertices)
                if test_simplex in manifold:
                    first_edge = pair[0]
                    second_edge = pair[1]
                    first_link  = link_dictionary[first_edge]
                    second_link  = link_dictionary[second_edge]
                    v1 = get_opposite_simplex_in_circle(first_link,second_edge)
                    v2 = get_opposite_simplex_in_circle(second_link,first_edge)
                    jumps.append(tuple(sorted([v1,v2])))

    return sorted_set(jumps)
                    
def get_weighted_graph(manifold,vertices,edges,report=False):

    hops = get_hops(manifold,vertices,edges)
    jumps = get_jumps(manifold,vertices,edges,hops)

    if report:
        print manifold 
        print 'simplices\t', len(manifold)
        print 'edges\t\t', len(edges)
        #print 'hops\t\t', len(hops)
        #print 'jumps\t\t', len(jumps),jumps

    g = networkx.MultiGraph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges,weight=edge_weight)
    g.add_edges_from(hops,weight=hop_weight)
    g.add_edges_from(jumps,weight=jump_weight)

    if False:
        ew = []
        colors = []
        for e in edges:
            ew.append(edge_weight)
            colors.append('green')
        for h in hops:
            ew.append(hop_weight)
            colors.append('red')
        for j in jumps:
            ew.append(jump_weight)
            colors.append('blue')
        weights = {}
        for e in edges:
            weights[e] = 1
        for h in hops:
            weights[h] = hop_weight
        for j in jumps:
            weights[h] = jump_weight
        return weights

    return g

def get_diameter(g):
    vertices = g.nodes()
    pairs = get_pairs(vertices)
    shortest_paths = networkx.all_pairs_dijkstra_path_length(g)
    #for s in  shortest_paths.keys():
    #    print s,shortest_paths[s]
    return  max(get_vertices([x.values() for x in shortest_paths.values()]))

def get_diameter_from_dists(dists):
    return  max(get_vertices([x.values() for x in dists.values()]))

def diameter_report(graph_hash):

    print 'diameter statistics by topological type'
    print 'format: diameter, diameter_by_steps, count\n'

    diameters = []
    types = []
    i =1
    for v in graph_hash.graph_dictionary.values():
        t = v[1]
        d = v[2]
        diameters.append(d)
        types.append(t)

    for t in set(types):
        type_diameter = []
        for i in range(len(types)):
            if types[i] == t:
                type_diameter.append(diameters[i])
        out = ''
        #print t,set(type_diameter)
        for d in sorted_set(type_diameter):
            out += str(d)[:4]+'\t'+pretty_print(d)+' '*(9-len(pretty_print(d))) + str(type_diameter.count(d)) +'\n'
        print t
        print out


    print 'global diameter statistics by topological type\n'

    for d in sorted_set(diameters):
        print str(d)[:4]+'\t'+pretty_print(d)+' '*(9-len(pretty_print(d))), diameters.count(d)

print __name__
if __name__ == '__main__':
    #h = graph_hash('manifold_graphs.dat',0)
    h = graph_hash('manifold_graphs_small.dat',1)
    diameter_report(h)

