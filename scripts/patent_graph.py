import networkx as nx
from scripts.preprocess import get_claims
import json
import re
import matplotlib.pyplot as plt

def make_graph(patent_file_loc, make_plot=False, file_loc=None):
    '''
    
    data:       A dictionary where keys are the nodes and values are the nodes which it depends on. 
                If claim 1 depends on claims 2 and 3 then 1 is key and [2, 3] is the value. 
    make_plot:  Boolean to plot the graph
    file_loc:   Gives file location of where to save the Adjacency List. file extension should be .adjlist
    
    '''

    patent_file=json.load(open(patent_file_loc))
    claims=[claim for claim in get_claims(patent_file['claims']) if not claim.isspace()]


    edges=[]
    for idx, claim in enumerate(claims):
        matched_val=re.findall(r"claim ([0-9]+)", claim)
        if matched_val!=[]:
            for val in matched_val:
                try:
                    edges.append([idx+1, int(val)])
                except Exception as e:
                    print(f"Error on value: {val}, regex matches: {matched_val}")
                    print(f"Error: {e}")
        else:
            edges.append([idx+1, 0])

    G = nx.Graph()
    G.add_nodes_from(range(len(claims)+1))

    G.add_edges_from(edges)
    if make_plot:
        plt.figure(figsize=(20,20))
        nx.draw_networkx(G, node_size=500)
    
    if file_loc!=None:
        nx.write_adjlist(G, file_loc)
    # G_read = nx.read_adjlist("patent.adjlist")
        
    return G


