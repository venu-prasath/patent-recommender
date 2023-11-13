import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_graph_similarity(patent_id1, patent_id2):
    G1=nx.read_adjlist(f"dataset/{patent_id1}/{patent_id1}.adjlist")
    G2=nx.read_adjlist(f"dataset/{patent_id2}/{patent_id2}.adjlist")
    claims_emb1 = np.load(f"dataset/{patent_id1}/{patent_id1}_claim_emb.npy")
    claims_emb2 = np.load(f"dataset/{patent_id2}/{patent_id2}_claim_emb.npy")
    matched_node_combinations=[]

    for node1 in G1.nodes:
        for node2 in G2.nodes:
            if node1=='0' or node2=='0':
                continue
            if cosine_similarity([claims_emb1[int(node1)-1]], [claims_emb2[int(node2)-1]])>0.97:
                matched_node_combinations.append([node1, node2])
    return matched_node_combinations
            

def random_walk(G, node, num_steps=100):
    visited=[]
    counter=0
    while counter<num_steps:
        neighbors=[i for i in nx.all_neighbors(G, node)]
        visited_node=np.random.choice(neighbors)
        node=visited_node
        visited.append(visited_node)
        counter+=1
    return list(set(visited))