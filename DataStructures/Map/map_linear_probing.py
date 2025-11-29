from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me
import random

def new_map(num_elements, load_factor, prime=109345121):

    # evitar capacity cero
    base = max(1, int(num_elements / load_factor))
    capacity = mf.next_prime(base)

    # cambio para grafos
    scale = 1
    shift = 0

    
    #scale = random.randint(1, prime - 1)
    #shift = random.randint(0, prime - 1)
    
    limit_factor = load_factor
    
    new_map = {
        "prime": prime,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": lt.new_list(),
        "current_factor": 0,
        "limit_factor": limit_factor,
        "size": 0,
    }

    for i in range(capacity):
        lt.add_last(new_map["table"], me.new_map_entry(None, None)) 

    return new_map


def put(my_map, key, value):
    hash_val = mf.hash_value(my_map, key)
    ocupied, idx = mf.find_slot(my_map, key, hash_val)
    if idx is None:
        raise Exception(f"No se encontró un slot válido para la clave: {key}. El mapa puede estar lleno o corrupto.")
    dato = lt.get_element(my_map["table"], idx)

    if ocupied:
        dato['value'] = value
    else:
        dato['key'] = key
        dato['value'] = value
        my_map["size"] += 1

    my_map['current_factor'] = my_map["size"] / my_map["capacity"]

    if my_map['current_factor'] > my_map['limit_factor']:
        my_map = rehash(my_map)

    return my_map


def contains(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    ocupied, idx = mf.find_slot(my_map, key, hash_val)
    if ocupied:
        entry = lt.get_element(my_map["table"], idx)
        return me.get_key(entry) == key
    return False


def get(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    ocupied, idx = mf.find_slot(my_map, key, hash_val)
    if ocupied:
        entry = lt.get_element(my_map["table"], idx)['value']
        return entry
    return None


def remove(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    ocupied, idx = mf.find_slot(my_map, key, hash_val)
    if not ocupied:
        return my_map
    else:
        me.set_value(lt.get_element(my_map["table"], idx), None)
        me.set_key(lt.get_element(my_map["table"], idx), None)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"] 
        
    return my_map   




def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = lt.new_list()
    for i in range(my_map["capacity"]):
        entry = lt.get_element(my_map["table"], i)
        k = me.get_key(entry)
        if k is not None and k != "_EMPTY_":
            lt.add_last(keys, k)
    return keys

def value_set(my_map):
    values = lt.new_list()
    for e in my_map["table"]["elements"]:
        vale= e['value']
        if vale != None:
            lt.add_last(values, vale)
    return values

def rehash(my_map):
    old_table = my_map["table"]
    new_capacity = mf.next_prime(my_map["capacity"] * 2)
    new_map_obj = new_map(new_capacity, my_map["limit_factor"], my_map["prime"])
    for i in range(my_map["capacity"]):
        entry = lt.get_element(old_table, i)
        k = me.get_key(entry)
        v = me.get_value(entry)
        if k is not None and k != "_EMPTY_":
            put(new_map_obj, k, v)
    return new_map_obj

# ya estaban hechas xd
def default_compare(key, entry):

   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1

def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = lt.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, lt.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail

def is_available(table, pos):

   entry = lt.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "_EMPTY_":
      return True
   return False