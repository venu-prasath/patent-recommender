import networkx as nx
import pandas as pd
from itertools import combinations
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

def make_network(df, use_cpc=False, use_authors=False, use_year=False, use_abstract=False, make_plot=False):
    G = nx.Graph()
    G.add_nodes_from(df['patent_id'])

    # Use classification codes
    if use_cpc:
        classifications={}
        for row in df.values:
            for cpc in row[6]:
                cpc=cpc.strip()
                if cpc not in classifications:
                    classifications[cpc]=[row[0]]
                else:
                    classifications[cpc].append(row[0])

        for cpc in classifications:
            edges_subset=list(combinations(classifications[cpc], 2))
            G.add_edges_from(edges_subset)

    # Use years
    if use_year:
        years={}
        for row in df.values:
            year=row[9]
            if year not in years:
                years[year]=[row[0]]
            else:
                years[year].append(row[0])


        for year in years:
            edges_subset=list(combinations(years[year], 2))
            G.add_edges_from(edges_subset)

    # Use authors
    if use_authors:
        authors={}
        for row in df.values:
            for author in row[5]:
                author=author.strip()
                if author not in authors:
                    authors[author]=[row[0]]
                else:
                    authors[author].append(row[0])


        for author in authors:
            edges_subset=list(combinations(authors[author], 2))
            G.add_edges_from(edges_subset)

    # Use abstract
    if use_authors:
        edges_subset=list(combinations(df.index, 2))
        edge_sim_labelled=[]

        for idx1, idx2 in tqdm(edges_subset):

            embeddings_1=df['abstract_emb'][idx1]
            embeddings_2=df['abstract_emb'][idx2]
            cosine_sim_val=cosine_similarity( [ embeddings_1 ], [ embeddings_2 ])

            if cosine_sim_val>0.5:
                edge_sim_labelled.append([df['patent_id'][idx1], df['patent_id'][idx2]])
        G.add_edges_from(edge_sim_labelled)

    if make_plot:
        plt.figure(figsize=(200,200))
        nx.draw_networkx(G, node_size=500)
    
    return G