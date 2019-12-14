import numpy as np

from igraph import Graph, plot

# Создание вершин и ребер
vertices = [i for i in range(7)]
edges = [
    (0,2),(0,1),(0,3),
    (1,0),(1,2),(1,3),
    (2,0),(2,1),(2,3),(2,4),
    (3,0),(3,1),(3,2),
    (4,5),(4,6),
    (5,4),(5,6),
    (6,4),(6,5)
]

# Создание графа
g = Graph(vertex_attrs={"label":vertices},
    edges=edges, directed=False)

# Задаем стиль отображения графа
N = len(vertices)
visual_style = {}
visual_style["layout"] = g.layout_fruchterman_reingold(
    maxiter=1000,
    area=N**3,
    repulserad=N**3)

# Отрисовываем граф
plot(g, **visual_style)