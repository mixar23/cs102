from api import get_friends
import igraph
import time

from igraph import Graph, plot
from typing import Union, List, Tuple


users_ids = []
name_list = []
friends = get_friends(228147479)
for friend in friends:
    try:
        id = friend['id']
        name = friend['first_name'] + ' ' + friend['last_name']
        users_ids.append(id)
        name_list.append(name)
    except ValueError:
        pass

def get_network(users_ids, as_edgelist=True) -> Union[List[List[int]], List[Tuple[int, int]]]:
    if as_edgelist:
        edge_list = []
        for user in users_ids:
            try:
                friend_list = get_friends(user)
            except KeyError:
                continue
            else:
                for friend in friend_list:
                    if friend['id'] in users_ids:
                        edge_list.append((users_ids.index(user), users_ids.index(friend['id'])))
        return edge_list
    else:
        matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]
        for user in users_ids:
            try:
                friend_list = get_friends(user)
            except KeyError:
                continue
            else:
                for friend in friend_list:
                    if friend['id'] in users_ids:
                        matrix[users_ids.index(user)][users_ids.index(friend['id'])] = 1
        return matrix


def plot_graph(edge_list: list, name_list=[]) -> None:
    if name_list == 0:
        vertices = [i for i in range(len(edge_list))]
    else:
        vertices = name_list
    g = Graph(vertex_attrs={"label": vertices},
              edges=edge_list, directed=False)
    g.simplify(multiple=True, loops=True)
    N = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "edge_color": "gray",
        "autocurve": True,
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)


# Вызов функций для проверки:
# plot_graph(get_network(users_ids), name_list)
# print(get_network(users_ids, False))
