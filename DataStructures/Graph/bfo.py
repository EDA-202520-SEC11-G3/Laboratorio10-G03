from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as dg
from DataStructures.List import single_linked_list as lt
from DataStructures.List import array_list as alt

def bfs(my_graph, source):
    visited_map = mp.new_map(num_elements=30000, load_factor=0.7, prime=109345121)

    if not dg.contains_vertex(my_graph, source):
        return visited_map

    vertex_data = {
        'edge_from': None,
        'dist_to': 0
    }
    mp.put(visited_map, source, vertex_data)

    bfs_result = bfs_vertex(my_graph, source, visited_map)

    return bfs_result

def bfs_vertex(my_graph, source, visited_map):
    queue = q.new_queue()
    q.enqueue(queue, source)

    while not q.is_empty(queue):
        current_vertex = q.dequeue(queue)
        current_info = mp.get(visited_map, current_vertex)

        if current_info is None:
            pass
        else:
            adj_vertices = dg.adjacents(my_graph, current_vertex)
            
            if adj_vertices is not None:
                size = alt.size(adj_vertices)
                i = 0
                while i < size:
                    adj_vertex_info = alt.get_element(adj_vertices, i)
                    
                    if isinstance(adj_vertex_info, tuple):
                        adj_vertex = adj_vertex_info[0]
                    else:
                        adj_vertex = adj_vertex_info

                    if dg.contains_vertex(my_graph, adj_vertex):
                        if not mp.contains(visited_map, adj_vertex):
                            new_distance = current_info['dist_to'] + 1

                            vertex_data = {
                                'edge_from': current_vertex,
                                'dist_to': new_distance
                            }
                            mp.put(visited_map, adj_vertex, vertex_data)

                            q.enqueue(queue, adj_vertex)
                    
                    i += 1

    return visited_map

def has_path_to(visited_map, key_v):
    return mp.contains(visited_map, key_v)

def path_to(visited_map, key_v):
    if not has_path_to(visited_map, key_v):
        return None

    path = st.new_stack()
    current_vertex = key_v

    max_iterations = 1000
    iteration = 0
    
    while current_vertex is not None and iteration < max_iterations:
        st.push(path, current_vertex)
        
        vertex_info = mp.get(visited_map, current_vertex)
        if vertex_info is None:
            current_vertex = None
        else:
            current_vertex = vertex_info['edge_from']
            iteration += 1

    return path

def dist_to(visited_map, key_v):
    if not has_path_to(visited_map, key_v):
        return float('inf')
        
    vertex_info = mp.get(visited_map, key_v)
    if vertex_info is None:
        return float('inf')
        
    return vertex_info['dist_to']