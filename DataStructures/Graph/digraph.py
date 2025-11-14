from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import vertex as vtx


def new_graph(order):
    return { "vertices": mlp.new_map(order, 0.5),
             "num_edges": 0}


def insert_vertex(graph, key_u, value_u):
    vertex = vtx.new_vertex(key_u, value_u)
    mlp.put(graph["vertices"], key_u, vertex)
    return graph


def add_edge(my_graph, key_u, key_v, weight=1.0):
    u_value = mlp.get(my_graph["vertices"], key_u)
    v_value = mlp.get(my_graph["vertices"], key_v)
    
    if u_value is None:
        raise KeyError("El vertice u no existe")
    if v_value is None:
        raise KeyError("El vertice v no existe")
    
    edges_u = u_value["num_edges"]
    if mlp.get(edges_u, key_v) is None:
        mlp.put(edges_u, key_v, weight)
        my_graph["num_edges"] += 1
    
    return my_graph


def size(my_graph):
    return my_graph["num_edges"]


def order(my_graph):
    return mlp.size(my_graph["vertices"])