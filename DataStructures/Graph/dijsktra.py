from DataStructures.Graph import dijsktra_structure as dijkstra_struct
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as st
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Priority_queue import pq_entry as pqe
import math
from DataStructures.List import array_list as alt

def dijkstra(my_graph, source):
    if not mp.contains(my_graph['vertices'], source):
        return None

    g_order = mp.size(my_graph['vertices'])
    structure = dijkstra_struct.new_dijsktra_structure(source, g_order)

    vertices_list = mp.key_set(my_graph['vertices'])
    
    for i in range(alt.size(vertices_list)):
        vertex_key = alt.get_element(vertices_list, i)
        
        if vertex_key == source:
            vertex_info = {
                'marked': False,
                'edge_from': None,
                'dist_to': 0.0
            }
            pq.insert(structure['pq'], 0.0, vertex_key)
        else:
            vertex_info = {
                'marked': False,
                'edge_from': None,
                'dist_to': float('inf')
            }
        
        mp.put(structure['visited'], vertex_key, vertex_info)

    while not pq.is_empty(structure['pq']):
        pq_element = pq.remove(structure['pq'])
        current_vertex = pqe.get_value(pq_element)
        current_priority = pqe.get_priority(pq_element)
        
        current_info = mp.get(structure['visited'], current_vertex)
        
        if current_info['marked']:
            pass
        else:
            current_info['marked'] = True
            mp.put(structure['visited'], current_vertex, current_info)

            vertex_obj = mp.get(my_graph['vertices'], current_vertex)
            if vertex_obj is not None:
                adjacents_map = vertex_obj['adjacents']
                adj_keys = mp.key_set(adjacents_map)

                for j in range(alt.size(adj_keys)):
                    adj_key = alt.get_element(adj_keys, j)
                    edge = mp.get(adjacents_map, adj_key)

                    if edge is not None:
                        adj_info = mp.get(structure['visited'], adj_key)
                        if adj_info is not None and not adj_info['marked']:
                            new_dist = current_info['dist_to'] + edge['weight']

                            if new_dist < adj_info['dist_to']:
                                adj_info['dist_to'] = new_dist
                                adj_info['edge_from'] = current_vertex
                                mp.put(structure['visited'], adj_key, adj_info)
                                pq.insert(structure['pq'], new_dist, adj_key)

    return structure

def dist_to(key_v, aux_structure):
    vertex_info = mp.get(aux_structure['visited'], key_v)
    if vertex_info is None:
        return float('inf')
    
    return vertex_info['dist_to']

def has_path_to(key_v, aux_structure):
    vertex_info = mp.get(aux_structure['visited'], key_v)
    if vertex_info is None:
        return False
    
    return vertex_info['dist_to'] < float('inf')

def path_to(key_v, aux_structure):
    if not has_path_to(key_v, aux_structure):
        return None

    path_stack = st.new_stack()
    current_vertex = key_v

    while current_vertex is not None:
        st.push(path_stack, current_vertex)
        vertex_info = mp.get(aux_structure['visited'], current_vertex)
        current_vertex = vertex_info['edge_from']

    return path_stack