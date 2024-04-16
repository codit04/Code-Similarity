import ast
import numpy as np
import networkx as nx
from networkx.algorithms import graph_edit_distance, optimize_graph_edit_distance
import matplotlib.pyplot as plt
from Visualize import visualize
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
from Levenshtein import distance, ratio, hamming


def idist(trav1, trav2):
    return ratio(trav1, trav2)


def hdist(trav1, trav2):
    return hamming(trav1, trav2)


def ldist(trav1, trav2):
    return distance(trav1, trav2)


def similarity(preorder1, preorder2, inorder1, inorder2):
    preorder1 = "".join([str(i) for i in preorder1])
    preorder2 = "".join([str(i) for i in preorder2])
    inorder1 = "".join([str(i) for i in inorder1])
    inorder2 = "".join([str(i) for i in inorder2])
    totLen = len(preorder1) + len(preorder2)
    scores = []
    scores.append(idist(preorder1, preorder2) + idist(inorder1, inorder2) / 2)
    scores.append(
        (hdist(preorder1, preorder2) / totLen + hdist(inorder1, inorder2) / totLen) / 2
    )
    scores.append(
        (ldist(preorder1, preorder2) / totLen + ldist(inorder1, inorder2) / totLen) / 2
    )
    return scores

def get_ast_tree(code):
    tree = ast.parse(code)
    return tree


def ast_to_nx(tree):

    G = nx.DiGraph()
    G.add_node(0, label=tree)
    queue = [(0, tree)]
    count = 1
    while queue:
        parent, node = queue.pop(0)
        for child in ast.iter_child_nodes(node):
            G.add_node(count, label=child)
            G.add_edge(parent, count)
            queue.append((count, child))
            count += 1
    return G


def calculate_similarity(code1, code2):
    tree1 = get_ast_tree(code1)
    tree2 = get_ast_tree(code2)

    G1 = ast_to_nx(tree1)
    G2 = ast_to_nx(tree2)

    preorder1 = list(nx.dfs_preorder_nodes(G1, source=0))
    preorder2 = list(nx.dfs_preorder_nodes(G2, source=0))
    inorder1 = list(nx.dfs_tree(G1, source=0))
    inorder2 = list(nx.dfs_tree(G2, source=0))
    similarity_score = similarity(preorder1, preorder2, inorder1, inorder2)
    return similarity_score
