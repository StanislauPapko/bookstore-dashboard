import pandas as pd
import networkx as nx
from itertools import combinations

def create_id_dict(users, *columns, original_id:str = 'user_id', subset_size:int = 3) -> dict:
    G = nx.Graph()
    G.add_nodes_from(users[original_id])
    MIN_COMBINATION_CONDITION = 2
    COMBINATION_SIZE = 2
    for subset in combinations(columns, subset_size):
        for ids in users.groupby(list(subset))[original_id].apply(list):
            if len(ids) >= MIN_COMBINATION_CONDITION:
                G.add_edges_from(combinations(ids, COMBINATION_SIZE))
    id_dict = {}
    for new_id, ids in enumerate(nx.connected_components(G)):
        for old_id in ids:
            id_dict[old_id] = new_id
    return id_dict