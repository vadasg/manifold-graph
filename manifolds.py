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
    def __init__(self, graph_dictionary_file_name, debug = 0):

        self.graph_dictionary_file_name = graph_dictionary_file_name
        self.debug = debug
        self.diameter_file_name = ('diameters_' 
            + self.graph_dictionary_file_name)

        if self.debug:
            print 'Debug level:', debug
            self.diameter_file_name = ('diameters_'
                + self.diameter_file_name)
            self.graph_dictionary_file_name = ('debug_'
                + self.graph_dictionary_file_name)
            self.clean()

        self.manifold_file_name = 'input.txt'
        self.manifold_type_file_name = 'manifolds_lex_d3_deg5.type.txt'

        #initialize by building manifolds, graphs, and diameters
        self.manifolds = self.get_manifolds()
        self.graph_dictionary = self.load_dictionary()

    def clean(self):
        #removes hashed files, prompting first for safety
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
        manifolds = manifolds\
            .replace(',\n',',').replace('\n\n','\n').replace('\n]',']') 
        end = -1
        
        #deeper debug level -- only 1 manifold
        if self.debug == 2:
            # The following is number 4784 in the census of positively
            # curved manifolds (Lutz/Sullivan). It should have diameter
            # of one jump and topological type L(4,1) 
            manifolds = [[[1,2,3,4],[1,2,3,5],[1,2,4,6],[1,2,5,7],
                [1,2,6,7],[1,3,4,8],[1,3,5,9],[1,3,8,9],[1,4,6,10],
                [1,4,8,10],[1,5,7,11],[1,5,9,11],[1,6,7,12],[1,6,10,12],
                [1,7,11,12],[1,8,9,13],[1,8,10,13],[1,9,11,13],
                [1,10,12,13],[1,11,12,13],[2,3,4,14],[2,3,5,15],
                [2,3,14,15],[2,4,6,16],[2,4,14,16],[2,5,7,17],
                [2,5,15,17],[2,6,7,18],[2,6,16,18],[2,7,17,18],
                [2,14,15,19],[2,14,16,19],[2,15,17,19],[2,16,18,19],
                [2,17,18,19],[3,4,8,20],[3,4,14,20],[3,5,9,16],
                [3,5,15,16],[3,8,9,21],[3,8,20,21],[3,9,16,21],
                [3,14,15,22],[3,14,20,22],[3,15,16,22],[3,16,21,22],
                [3,20,21,22],[4,5,6,10],[4,5,6,16],[4,5,9,11],
                [4,5,9,16],[4,5,10,11],[4,8,10,11],[4,8,11,20],
                [4,9,11,20],[4,9,14,16],[4,9,14,20],[5,6,10,17],
                [5,6,15,16],[5,6,15,17],[5,7,10,11],[5,7,10,17],
                [6,7,12,23],[6,7,18,23],[6,10,12,17],[6,12,17,23],
                [6,15,16,18],[6,15,17,23],[6,15,18,23],[7,10,11,24],
                [7,10,17,25],[7,10,24,25],[7,11,12,24],[7,12,23,24],
                [7,17,18,25],[7,18,23,25],[7,23,24,25],[8,9,13,26],
                [8,9,21,26],[8,10,11,24],[8,10,13,24],[8,11,20,27],
                [8,11,24,27],[8,13,24,26],[8,20,21,27],[8,21,26,27],
                [8,24,26,27],[9,11,13,20],[9,13,20,26],[9,14,16,21],
                [9,14,20,26],[9,14,21,26],[10,12,13,25],[10,12,17,25],
                [10,13,24,25],[11,12,13,27],[11,12,24,27],[11,13,20,27],
                [12,13,25,27],[12,17,23,28],[12,17,25,28],[12,23,24,28],
                [12,24,27,28],[12,25,27,28],[13,20,26,29],[13,20,27,29],
                [13,24,25,29],[13,24,26,29],[13,25,27,29],[14,15,19,30],
                [14,15,22,30],[14,16,19,21],[14,19,21,30],[14,20,22,26],
                [14,21,26,30],[14,22,26,30],[15,16,18,22],[15,17,19,23],
                [15,18,22,30],[15,18,23,30],[15,19,23,30],[16,18,19,22],
                [16,19,21,22],[17,18,19,28],[17,18,25,28],[17,19,23,28],
                [18,19,22,28],[18,22,28,30],[18,23,25,30],[18,25,28,30],
                [19,21,22,29],[19,21,29,30],[19,22,28,29],[19,23,28,29],
                [19,23,29,30],[20,21,22,29],[20,21,27,29],[20,22,26,29],
                [21,26,27,30],[21,27,29,30],[22,26,28,29],[22,26,28,30],
                [23,24,25,29],[23,24,28,29],[23,25,29,30],[24,26,27,28],
                [24,26,28,29],[25,27,28,30],[25,27,29,30],
                [26,27,28,30]]]
                
            return manifolds

        #simple debug level -- only run on first 100 manifolds
        elif self.debug == 1: end = 101
            
        #remove spurious newlines at end and beginning
        manifolds =  manifolds.split('\n')[1:end] 

        for i in range(len(manifolds)):
            #remove labels and text
            manifolds[i]=  manifolds[i][manifolds[i].find('['):]
            #turn into a python list
            manifolds[i] = eval('list(' +manifolds[i] + ')')        
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
            print ('loading dictionary from '
                + self.graph_dictionary_file_name)
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
    for num_edges in range(0,max_edges):
        for num_hops in range(0, max_hops):
            for num_jumps in range(0, max_jumps):
                d = (num_edges * edge_weight
                    + num_hops * hop_weight
                    + num_jumps * jump_weight)
                if abs(d-float(dist)) < 0.000000001:
                    out_string = ''
                    if (num_edges > 0):
                        out_string += str(num_edges) + 'E '
                    if (num_hops > 0):
                        out_string += str(num_hops) + 'H '
                    if (num_jumps > 0):
                        out_string += str(num_jumps) + 'J'
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
    #get list of all vertices v that appear in the manifold
    return sorted_set([v for simplex in manifold for v in simplex])

def get_graph(manifold):
    vertices = get_vertices(manifold)
    
    #get all edges by getting all edges in each simplex
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
    if degree_5_edges:
        check_simplices = []
        edge_pairs = get_pairs(degree_5_edges)
        for pair in edge_pairs:
            check_vertices =  get_vertices(pair)
            if len(check_vertices) == 4:
                test_simplex = sorted(check_vertices)
                if test_simplex in manifold:
                    first_edge = pair[0]
                    second_edge = pair[1]
                    first_link  = link_dictionary[first_edge]
                    second_link  = link_dictionary[second_edge]
                    v1 = get_opposite_simplex_in_circle(first_link,
                                                        second_edge)
                    v2 = get_opposite_simplex_in_circle(second_link,
                                                        first_edge)
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
    #pairs = get_pairs(vertices)
    dists = networkx.all_pairs_dijkstra_path_length(g)
    #for s in  shortest_paths.keys():
    #    print s,shortest_paths[s]
    return  max(get_vertices([x.values() for x in dists.values()]))

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
            out += (str(d)[:4] + '\t' + pretty_print(d)
                    + ' '*(9-len(pretty_print(d)))
                    + str(type_diameter.count(d)) + '\n')
        print t
        print out
    
    print 'global diameter statistics by topological type\n'

    for d in sorted_set(diameters):
        print str(d)[:4] + '\t' + pretty_print(d)\
            +' '*(9-len(pretty_print(d))), diameters.count(d)

print __name__
if __name__ == '__main__':
    h = graph_hash('manifold_graphs.dat',0)
    #h = graph_hash('manifold_graphs_small.dat',1)
    diameter_report(h)
