from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as vtx
from DataStructures.List import array_list as alt

def dfs(my_graph, source):
    g_order = dg.order(my_graph)

    search_structure = {
        'marked': mp.new_map(num_elements=g_order, load_factor=0.5),
        'edge_to': mp.new_map(num_elements=g_order, load_factor=0.5),
        'start_vertex': source
    }

    if not dg.contains_vertex(my_graph, source):
        return search_structure

    mp.put(search_structure['edge_to'], source, None)
    dfs_vertex(my_graph, source, search_structure)

    return search_structure

def dfs_vertex(my_graph, vertex_key, search_structure):
    mp.put(search_structure['marked'], vertex_key, True)

    adj_vertices = dg.adjacents(my_graph, vertex_key)

    if adj_vertices is not None:
        adj_size = alt.size(adj_vertices)

        if adj_size > 0:
            for i in range(adj_size):
                adj_vertex = alt.get_element(adj_vertices, i)

                if adj_vertex is not None:
                    is_marked = mp.contains(search_structure['marked'], adj_vertex)
                    if is_marked:
                        marked_value = mp.get(search_structure['marked'], adj_vertex)
                        if not marked_value:
                            mp.put(search_structure['edge_to'], adj_vertex, vertex_key)
                            dfs_vertex(my_graph, adj_vertex, search_structure)
                    else:
                        mp.put(search_structure['edge_to'], adj_vertex, vertex_key)
                        dfs_vertex(my_graph, adj_vertex, search_structure)

def adjacents(my_graph, key_u):
    vertex = mp.get(my_graph['vertices'], key_u)

    if vertex is None:
        return alt.new_list()

    adjacents_map = vtx.get_adjacents(vertex)

    if adjacents_map is None:
        return alt.new_list()

    keys = mp.key_set(adjacents_map)
    return keys

def has_path_to(key_v, search_structure):
    if 'marked' not in search_structure:
        return False

    marked_map = search_structure['marked']
    return mp.contains(marked_map, key_v) and mp.get(marked_map, key_v)

def path_to(key_v, search_structure):
    if not has_path_to(key_v, search_structure):
        return None

    path_stack = st.new_stack()
    current = key_v

    max_iterations = 1000
    iteration = 0

    while current is not None and iteration < max_iterations:
        st.push(path_stack, current)

        if current == search_structure['start_vertex']:
            current = None
        else:
            current = mp.get(search_structure['edge_to'], current)
            iteration += 1

    return path_stack

