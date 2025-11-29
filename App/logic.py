"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

# ___________________________________________________
#  Importaciones
# ___________________________________________________

from DataStructures.List import single_linked_list as lt
from DataStructures.List import array_list as alt
from DataStructures.Map import map_linear_probing as m
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import bfo as bfs
from DataStructures.Graph import dijsktra as dijkstra
from DataStructures.Stack import stack as st
from DataStructures.Priority_queue import priority_queue as pq
import csv
import time
import os

data_dir = os.path.dirname(os.path.realpath('_file_')) + '/Data/'

def init():
    analyzer = new_analyzer()
    return analyzer

def new_analyzer():
    analyzer = {
        'stops': None,
        'connections': None,
        'paths': None
    }
    analyzer['stops'] = m.new_map(
        num_elements=8000, load_factor=0.7, prime=109345121)
    analyzer['connections'] = G.new_graph(order=20000)
    return analyzer

def load_services(analyzer, servicesfile, stopsfile):
    stopsfile = data_dir + stopsfile
    stops_input_file = csv.DictReader(open(stopsfile, encoding="utf-8"),
                                  delimiter=",")
    for stop in stops_input_file:
        add_stop(analyzer, stop)

    servicesfile = data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                            delimiter=",")
    lastservice = None
    for service in input_file:
        if not G.contains_vertex(analyzer['connections'], format_vertex(service)):
            add_stop_vertex(analyzer, format_vertex(service))
        add_route_stop(analyzer, service)

        if lastservice is not None:
            sameservice = lastservice['ServiceNo'] == service['ServiceNo']
            samedirection = lastservice['Direction'] == service['Direction']
            samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
            if sameservice and samedirection and not samebusStop:
                add_stop_connection(analyzer, lastservice, service)

        add_same_stop_connections(analyzer, service)
        lastservice = service

    return analyzer

def total_stops(analyzer):
    return G.order(analyzer['connections'])

def total_connections(analyzer):
    return G.size(analyzer['connections'])

def get_time():
    return float(time.perf_counter()*1000)

def delta_time(end, start):
    elapsed = float(end - start)
    return elapsed

def add_stop_connection(analyzer, lastservice, service):
    origin = format_vertex(lastservice)
    destination = format_vertex(service)
    clean_service_distance(lastservice, service)
    distance = float(service['Distance']) - float(lastservice['Distance'])
    distance = abs(distance)
    add_connection(analyzer, origin, destination, distance)
    return analyzer

def add_stop(analyzer, stop):
    stop['services'] = lt.new_list()
    m.put(analyzer['stops'], stop['BusStopCode'], stop)
    return analyzer

def add_stop_vertex(analyzer, stopid):
    G.insert_vertex(analyzer['connections'], stopid, stopid)
    return analyzer

def add_route_stop(analyzer, service):
    stop_info = m.get(analyzer['stops'], service['BusStopCode'])
    stop_services = stop_info['services']

    if lt.is_present(stop_services, service['ServiceNo'], lt.default_sort_criteria) == -1:
        lt.add_last(stop_services, service['ServiceNo'])
    return analyzer

def add_connection(analyzer, origin, destination, distance):
    if not G.contains_vertex(analyzer['connections'], origin):
        add_stop_vertex(analyzer, origin)
    if not G.contains_vertex(analyzer['connections'], destination):
        add_stop_vertex(analyzer, destination)

    G.add_edge(analyzer['connections'], origin, destination, distance)
    return analyzer

def add_same_stop_connections(analyzer, service):
    stop_1 = format_vertex(service)
    stop_info = m.get(analyzer['stops'], service['BusStopCode'])

    if stop_info is None:
        return analyzer

    stop_buses_lt = stop_info['services']

    node = stop_buses_lt['first']
    for _ in range(lt.size(stop_buses_lt)):
        if node and node['info']:
            stop_2 = format_vertex({'BusStopCode': service['BusStopCode'], 'ServiceNo': node['info']})
            if stop_1 != stop_2:
                add_connection(analyzer, stop_1, stop_2, 0)
        if node:
            node = node['next']
    return analyzer

def get_most_concurrent_stops(analyzer):
    vertices = G.vertices(analyzer['connections'])
    
    stops_degree_dict = {}
    
    n = alt.size(vertices)
    for i in range(1, n + 1):
        vertex = alt.get_element(vertices, i)
        if vertex is None or '-' not in vertex:
            continue
            
        bus_stop_code, _ = vertex.split('-')
        
        # Solo grado de salida
        out_degree = G.degree(analyzer['connections'], vertex)
        
        stops_degree_dict[bus_stop_code] = stops_degree_dict.get(bus_stop_code, 0) + out_degree
    
    if not stops_degree_dict:
        return None
    
    sorted_stops = sorted(stops_degree_dict.items(), key=lambda x: x[1], reverse=True)
    
    # CAMBIO: Usar single_linked_list en lugar de array_list
    top_5 = lt.new_list()
    for bus_stop_code, total_degree in sorted_stops[:5]:
        # Obtener información de la parada del mapa
        stop_info_value = m.get(analyzer['stops'], bus_stop_code)
        
        # Si stop_info_value es un diccionario, usarlo directamente
        if isinstance(stop_info_value, dict):
            desc = stop_info_value.get('Description', 'N/A')
            road = stop_info_value.get('RoadName', 'N/A')
            services_count = lt.size(stop_info_value.get('services', lt.new_list()))
        else:
            # Si es un string u otro tipo, usar valores por defecto
            desc = "N/A"
            road = "N/A" 
            services_count = 0
        
        # Crear diccionario con la información
        stop_data = {
            'BusStopCode': bus_stop_code,
            'Description': desc,
            'RoadName': road,
            'TotalDegree': total_degree,
            'ServicesCount': services_count
        }
        
        lt.add_last(top_5, stop_data)
    
    return top_5



def get_route_between_stops_dfs(analyzer, stop1, stop2):
    if not G.contains_vertex(analyzer['connections'], stop1) or not G.contains_vertex(analyzer['connections'], stop2):
        return None

    bfs_result = bfs.bfs(analyzer['connections'], stop1)

    if bfs.has_path_to(bfs_result, stop2):
        path = bfs.path_to(bfs_result, stop2)
        return path
    else:
        return None

def get_route_between_stops_bfs(analyzer, stop1, stop2):
    if not G.contains_vertex(analyzer['connections'], stop1) or not G.contains_vertex(analyzer['connections'], stop2):
        return None

    bfs_result = bfs.bfs(analyzer['connections'], stop1)

    if bfs.has_path_to(bfs_result, stop2):
        path = bfs.path_to(bfs_result, stop2)
        return path
    else:
        return None

def get_shortest_route_between_stops(analyzer, stop1, stop2):
    if not G.contains_vertex(analyzer['connections'], stop1) or not G.contains_vertex(analyzer['connections'], stop2):
        return None, float('inf')

    dijkstra_result = dijkstra.dijkstra(analyzer['connections'], stop1)

    analyzer['paths'] = dijkstra_result

    if dijkstra.has_path_to(stop2, dijkstra_result):
        path = dijkstra.path_to(stop2, dijkstra_result)
        distance = dijkstra.dist_to(stop2, dijkstra_result)
        return path, distance
    else:
        return None, float('inf')

def show_calculated_shortest_route(analyzer, destination_stop):
    if analyzer['paths'] is None:
        return "No se ha calculado ninguna ruta mínima"

    if dijkstra.has_path_to(analyzer['paths'], destination_stop):
        path = dijkstra.path_to(analyzer['paths'], destination_stop)
        distance = dijkstra.dist_to(analyzer['paths'], destination_stop)

        current_bus = None
        route_description = lt.new_list()
        node = path['first']
        while node is not None:
            stop_vertex = node['info']
            bus_stop_code, service_no = stop_vertex.split('-')

            if current_bus != service_no:
                if current_bus is not None:
                    lt.add_last(route_description, f"Cambiar a bus '{service_no}' en parada '{bus_stop_code}'")
                else:
                    lt.add_last(route_description, f"Tomar bus '{service_no}' desde '{stop_vertex}'")
                current_bus = service_no

            lt.add_last(route_description, bus_stop_code)
            node = node['next']

        return route_description, distance
    else:
        return "No hay ruta disponible", float('inf')

def clean_service_distance(lastservice, service):
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0

def format_vertex(service):
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name