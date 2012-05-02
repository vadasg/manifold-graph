import networkx, os
import matplotlib.pyplot as plt
import cPickle
#import sympy

small_list = False
debug = False

edge_weight = 1
hop_weight = (8.0/3.0)**(0.5)
jump_weight = (3.0)**(0.5) + 0.5*((2.0)**(0.5))

def clean():
    os.system('rm -f manifold_graphs_small.dat')
    os.system('rm -f diameters.txt')


def sorted_set(x):
    return sorted(set(x))

def get_edges(simplex):
    return [(simplex[y],simplex[x]) for y in xrange(len(simplex)) for x in xrange(y,len(simplex)) if x!=y]

def get_manifolds(inputfile):
    #read in raw file
    f = open(inputfile,'r')
    manifolds = f.read()
    f.close()

    manifolds = manifolds.replace(',\n',',').replace('\n\n','\n').replace('\n]',']') #fix dumb line splitting

    if debug: #only run part of the file for debugging purposes
        #pass
        manifolds = [[[1,2,3,4],[1,3,4,5],[2,3,4,6],[3,4,5,7],[3,4,6,7],[3,6,7,9],[4,6,7,8],[6,7,8,10],[6,7,9,10]]]
        return manifolds

    elif small_list:
        end = 75
    else: 
        end = -1
    
    manifolds =  manifolds.split('\n')[1:end] #remove spurious newlines at end and beginning

    for i in range(len(manifolds)):
        manifolds[i]=  manifolds[i][manifolds[i].find('['):] #remove labels and text
        manifolds[i] = eval('list(' +manifolds[i] + ')') #turn into a python list
    #if debug:
    #   manifolds = [manifolds[8]]
    return manifolds

def get_vertices(manifold):
    #get list of all vertices that appear in the manifold
    return sorted_set([vertex for simplex in manifold for vertex in simplex])

def get_graph(manifold):
    #first get all vertices
    vertices = get_vertices(manifold)
    #now get all edges by getting all edges in each simplex
    edges = []
    for simplex in manifold:
        edges += get_edges(simplex) 
    edges = sorted_set(edges)
    return vertices,edges

def get_degree(edge,manifold):
    return len(get_2_simplex_list(edge,manifold))

def get_2_simplex_list(edge,manifold):
    simplex_list=[]
    for simplex in manifold:
        if (edge[0] in simplex) and (edge[1] in simplex):
            simplex_list.append(simplex)
    return simplex_list

def get_hops(manifold,vertices,edges):
    #now do hops
    hops = []
    for v1 in vertices:
        check_in = [simplex for simplex in manifold if v1 in simplex]
        for ci in check_in:
            for v2 in vertices:
                #if (tuple(sorted([v1,v2])) not in edges) and (v1 != v2):
                if (v1 != v2):
                    test_simplex = ci[:]
                    if v2 not in test_simplex:
                        test_simplex[test_simplex.index(v1)] = v2
                        test_simplex.sort()
                        if test_simplex in manifold:
                            hops.append(tuple(sorted([v1,v2])))
    return sorted_set(hops)

def get_jumps(manifold,vertices,edges,hops):
    def traverse_edge(edge,vertex):
        next_edge = list(edge)
        next_edge.remove(vertex)
        return next_edge[0]

    def get_link_path(link,next_vertex):
        links = link[:]
        link_path = [next_vertex]
        for i in range(len(link)-1):
            next_edge = [x for x in links if (next_vertex in x)][0]
            next_vertex= traverse_edge(next_edge,next_vertex)
            links.remove(next_edge)
            link_path.append(next_vertex)
        return link_path

    def get_opposite_link_edge(link,vertex):
        link_path = get_link_path(link,vertex)
        v1 = traverse_link_path(link_path,vertex,nsteps=2)
        v2 = traverse_link_path(link_path,vertex,nsteps=3)
        return tuple(sorted([v1,v2]))
                
    def traverse_link_path(link_path,vertex,nsteps=1):
        vertex_index = link_path.index(vertex)
        if vertex_index < len(link_path)-nsteps:
            return link_path[vertex_index+nsteps]
        else:
            return link_path[0]
        
    def get_opposite_link_vertex(link,edge):
        link_path = get_link_path(link,edge[0])
        next_vertex = traverse_link_path(link_path,edge[0])
        if next_vertex in edge:
            next_vertex = traverse_link_path(link_path,next_vertex,2)
        else:
            next_vertex = traverse_link_path(link_path,next_vertex,1)
        
        return next_vertex

    def get_link(e,simplex_list):
        link = []
        for simplex in simplex_list:
            all_edges = get_edges(simplex)
            link += [x for x in all_edges if (e[0] not in x) and (e[1] not in x)]
        link= sorted_set(link)
        return link

    #now do jumps
    jumps = []

    #get edges that have diameter 5
    link_dict = {}
    degree_5_edges = []
    for e in edges:
        if get_degree(e,manifold) == 5:
            degree_5_edges.append(e)
            simplex_list = get_2_simplex_list(e,manifold)
            link_dict[e] = get_link(e,simplex_list)

    if len(degree_5_edges) >0:


        check_simplices = []
        edge_pairs  = get_edges(degree_5_edges)
        for pair in edge_pairs:
            check_vertices =  get_vertices(pair)
            if len(check_vertices) == 4:
                test_simplex = sorted(check_vertices)
                if test_simplex in manifold:
                    first_edge = pair[0]
                    second_edge = pair[1]
                    first_link  = link_dict[first_edge]
                    second_link  = link_dict[second_edge]
                    v1 = get_opposite_link_vertex(first_link,second_edge)
                    v2 = get_opposite_link_vertex(second_link,first_edge)
                #if (v1 != v2):
                    jumps.append(tuple(sorted([v1,v2])))


    if False:
        #now check all of the vertices that appear in the 2-simplices that contain that edge
        for first_edge in degree_5_edges:
                first_link  = link_dict[first_edge]
                check_v1 = get_vertices(first_link)
                for v1 in check_v1:
                    second_edge = get_opposite_link_edge(first_link,v1)  
                    #this must be in the link of another degree_5_edge
                    if second_edge not in degree_5_edges:
                        break
                    second_link = link_dict[second_edge]
                    v2 = get_opposite_link_vertex(second_link,first_edge)

                    #only keep jumps if minimal and not to the same node
                    #if (v1 != v2) and (keep not in edges) and (keep not in hops):
                    if (v1 != v2):
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

def build_dict():
    inputfile = 'input.txt'
    manifolds = get_manifolds(inputfile)
    f = open('manifolds_lex_d3_deg5.type.txt','r')
    types = f.readlines()
    f.close()
    manifold_dict = {}
    for i in range(len(manifolds)):
        t = types[i].split()[-1]
        manifold = manifolds[i]
        vertices,edges = get_graph(manifold)
        g = get_weighted_graph(manifold,vertices,edges)
        manifold_dict[i+1] = (g,t)
        print (i+1), t
    return manifold_dict

def load_dict(file_name):
    if debug:
        d = build_dict()
        return d
    try:
        print 'loading dictionary from ' + file_name
        f = open(file_name,'rb')
        d = cPickle.load(f)
        f.close()
        print 'dictionary loaded!'
    except:
        print 'dictionary not found. building dictionary'
        d = build_dict()
        save_dict(d,file_name)
    return d

def save_dict(d,file_name):
        f = open(file_name,'wb')
        cPickle.dump(d,f)
        f.close()

def get_diameter(g):
    vertices = g.nodes()
    pairs = get_edges(vertices)
    shortest_paths = networkx.all_pairs_dijkstra_path_length(g)
    #for s in  shortest_paths.keys():
    #    print s,shortest_paths[s]
    return  max(get_vertices([x.values() for x in shortest_paths.values()]))

def get_all_diameters(manifold_dict):
    out = ''
    for i in range(1,len(manifold_dict)+1):
        print i
        g,t = manifold_dict[i]
        d = get_diameter(g)
        out += t + '\t' + str(d) + '\n'

    f = open('diameters.txt','w')
    f.write(out)
    f.close()

def pretty_print(dist):
    dist_dict = {}
    for i in range(1,6):
        dist_dict[i*edge_weight] = str(i)+'E'
        dist_dict[i*hop_weight] = str(i)+'H'
        dist_dict[i*jump_weight] = str(i)+'J'
    dist_dict[edge_weight+hop_weight] = '1E+1H'
    dist_dict[edge_weight+jump_weight] = '1E+1J'
    dist_dict[2*edge_weight+jump_weight] = '2E+1J'
    for d in dist_dict.keys():
        if abs(d-float(dist)) < 0.000000001:
            return dist_dict[d]
    else:
        return dist

#clean()
#for small dictionary (debugging) use:
manifold_dict = load_dict('./manifold_graphs_small.dat')
#g = manifold_dict[1][0]
#networkx.draw(g)
#plt.show()
#get_diameter( manifold_dict[1][0])

#get_all_diameters(manifold_dict)

if True:
    f = open('diameters.txt','r')
    dt = f.readlines()
    f.close()


    print 'diameter statistics by topological type'
    print 'format: diameter, diameter_by_steps, count\n'

    diameters = []
    types = []
    i =1
    for line in dt:
        print i,line
        t,d = line.split()
        diameters.append(d)
        types.append(t)
        i += 1

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




        #diameters.append(get_diameter(g))
        #types.append(t)




    #networkx.write_graphml(g,'./graphs/' + str(i+1) + '.xml')
    #networkx.draw(g,weights=gw,colors=colors)
    #plt.show()

#for full dictionary use:
#manifold_dict = load_dict('./manifold_graphs.dat')
