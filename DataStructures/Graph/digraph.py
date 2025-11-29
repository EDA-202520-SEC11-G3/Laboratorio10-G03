from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import vertex as V
from DataStructures.Map import map_linear_probing as lp


def new_graph(order):
    return {
        "vertices": lp.new_map(order, 0.5),
        "num_edges": 0
    }


def contains_vertex(my_graph, key_u):
    return lp.contains(my_graph["vertices"], key_u)


def order(my_graph):
    return my_graph["vertices"]["size"]


def size(my_graph):
    return my_graph["num_edges"]


def insert_vertex(my_graph, key_u, info_u=None):

 
    vertex = V.new_vertex(key_u, info_u)

    lp.put(my_graph["vertices"], key_u, vertex)

    return my_graph


def get_vertex_information(my_graph, key_u):

    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")

    return lp.get(my_graph["vertices"], key_u)


def vertices(my_graph):
    return lp.key_set(my_graph["vertices"])


def degree(my_graph, key_u):

    vertex = get_vertex_information(my_graph, key_u)

    return lp.size(vertex["adjacents"])


def add_edge(my_graph, key_u, key_v, weight=1.0):

    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice u no existe")

    if not contains_vertex(my_graph, key_v):
        raise Exception("El vertice v no existe")

    vertex_u = get_vertex_information(my_graph, key_u)

    existed = lp.contains(vertex_u["adjacents"], key_v)

    
    lp.put(vertex_u["adjacents"], key_v, weight)

    if not existed:
        my_graph["num_edges"] += 1

    return my_graph


def adjacents(my_graph, key_u):

    vertex = get_vertex_information(my_graph, key_u)

    # Retornar lista de llaves adyacentes
    return lp.key_set(vertex["adjacents"])


def get_vertex(my_graph, key_u):
    """Retorna el vértice completo (key, value, adj)."""
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vértice no existe")
    return lp.get(my_graph["vertices"], key_u)




def update_vertex_info(my_graph, key_u, new_info):
    """Actualiza la información (value) asociada al vértice."""
    vertex = get_vertex(my_graph, key_u)
    vertex["value"] = new_info
    lp.put(my_graph["vertices"], key_u, vertex)
    return my_graph



def edges_vertex(my_graph, key_u):
    """
    Retorna una lista de tuplas (v, peso) para cada adyacente.
    Ejemplo: [(2, 3.0), (4, 1.5)]
    """
    vertex = get_vertex(my_graph, key_u)
    adj_map = vertex["adjacents"]

    keys = lp.key_set(adj_map)
    result = []

    for k in keys["elements"]:
        if k is not None:
            weight = lp.get(adj_map, k)
            result.append((k, weight))

    return result