from api import get_friends
import time
import igraph




def get_network(user_id: int, as_edgelist) -> list:
    users_ids = get_friends(user_id)['response']['items']
    edges = []
    matrix = [[0] * num for i in range(num)]

    for user1 in range(num):
        friends = get_friends(users_ids[user1])['response']['items']
        for user2 in range(user1 + 1, num):
            if users_ids[user2] in friends:
                if as_edgelist:
                    edges.append((user1, user2))
                else:
                    matrix[user1][user2] = 1
                    matrix[user2][user1] = 1
        time.sleep(0.33333334)

    if as_edgelist:
        return edges
    return matrix


def plot_graph(user_id: int) -> None:
    surnames = get_friends(user_id, 'last_name')['response']['items']
    vertices = [i['last_name'] for i in surnames]
    edges = get_network(user_id, True)

    g = igraph.Graph(vertex_attrs={"shape": "circle",
                                   "label": vertices,
                                   "size": 10},
                     edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_label_dist": 1.6,
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }
    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(g, **visual_style)

if __name__ == '__main__':
    user_id = int(input('Enter id: '))
    num = get_friends(user_id)['response']['count']
    plot_graph(user_id)
