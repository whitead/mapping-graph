import networkx as nx
import operator
from collections import deque
def hash_neighs(queue, graph,tree=None):
    '''Builds a tree to fixed depth of all neighbors of n'''
    n=queue.popleft()
    if(tree is None):
        tree = nx.Graph(root=graph.node[n]['bond'])
        tree.add_node(n, bond=graph.node[n]['bond'])

    for neigh in sorted(nx.all_neighbors(graph, n)):
        if(not neigh in tree.node):
            
            tree.add_node(neigh, bond=graph.node[neigh]['bond'])
            tree.add_edge(neigh, n)
            queue.append(neigh)
    
    if(len(queue) == 0):
        return tree
    else:
        return(hash_neighs(queue,graph,tree))   

def bond_equiv_classes(G, LG, depth=None):
    '''Function to identify equivalent bonds'''

    #Sub trees are constructed setting each node of edge graph LG to be root
    sub_trees = dict()

    def node_equal(n1, n2):
        '''Determine if two nodes are isomorphic'''
        return (n1['bond'] == n2['bond'])

    #build all the trees
    for i,n in enumerate(LG.nodes_iter()):
        p = hash_neighs(deque([n]), LG)
        sub_trees[n] = p

    #equivalence classes
    equiv = [set() for x in LG.nodes_iter()]
    for e,n in zip(equiv, LG.nodes_iter()):
        e.add(n)

    #find the isomorphic trees and equivalence classes

    for k1,g1 in sub_trees.items():


        for k2, g2 in sub_trees.items():

            if(k1 == k2):
                continue
            if (LG.node[k1]['bond']==LG.node[k2]['bond']):
                '''If the root labels are different
                the sub-trees are not isomorphic'''
                gm = nx.isomorphism.GraphMatcher(g1, g2, node_match=node_equal)
                if(gm.is_isomorphic()):

                    for i in range(len(equiv)):
                        if k1 in equiv[i]:
                            break
                    for j in range(len(equiv)):
                        if k2 in equiv[j]:
                            break
                    if(i != j):
                        equiv[i] |= equiv[j]
                        del equiv[j]


    return equiv
