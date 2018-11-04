#import json
import operator
#import copy
import tabulate as tb
import networkx as nx
G = nx.read_edgelist('C:/Users/samiu/Desktop/8009 LAB/polblogs.edgelist.simple_format_unweighted', create_using=nx.Graph())
gMatrix = nx.to_scipy_sparse_matrix(G)
nodeDictList = nx.to_dict_of_lists(G)
class DirectedGraphADT(object):
    
    def __init__(self):
        self.graph = {}
        self.noOfEdges = 0.0
       
    def vertices(self):
        return self.graph.keys()
        
    def getGraph(self):
        if self.graph == None or len(self.graph) == 0:
            raise Exception("Graph is empty")
        return self.graph
     
    def setGraph(self, graph):
        self.graph = graph
        
# Fr. = (1-d)/N + summ(d*Prank(v)/outgoing edges)
def computePageRank(graph, damping_factor = 0.80, eps = 0.00001):
    vertices = len(graph.vertices())    
    old_prank, new_prank = {}, {}
    for vertex in graph.vertices():
        old_prank[vertex] = 1.0/vertices
    for iter_ in range(1, 101):
        print ("Iteration: %d" % iter_)        
        diff = []
        for u in graph.vertices():
            rank = (1-damping_factor)/vertices
            for v in graph.vertices():
                if u in graph.getGraph()[v]:
                    rank += damping_factor*old_prank[v]/len(graph.getGraph()[v])
            diff.append(abs(old_prank[u] - rank))
            new_prank[u] = rank
        old_prank = copy.deepcopy(new_prank)
        new_prank.clear()
        if sum(diff) < eps:
            print ("Total iterations: %d" % iter_)
            break
    return old_prank

def topthirtyusers(scores):
    """
    Display the top 30 users in the graph ranked by
    their page rank scores
    """
    table = sorted(scores.items(), key = lambda x: x[1], reverse = True)
    headers = ["User", "PageRank Score"]
    print (tb.tabulate(table[:30], headers, tablefmt = "rst"))
    
graph = DirectedGraphADT()
graph.setGraph(nodeDictList)
ranks = computePageRank(graph, 0.8)
sort = sorted(ranks.items(),key=operator.itemgetter(-1))
for i in sort:
    print(i)

topthirtyusers(ranks)    