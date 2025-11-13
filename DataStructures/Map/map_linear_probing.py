from DataStructures.List import array_list as lt
from . import map_functions as mf
from . import map_entry as me
import random

def new_map(num_elements,load_factor,prime=109345121):
    capacity=mf.next_prime(num_elements/load_factor)
    scale=random.randint(1, prime-1)
    shift=random.randint(0, prime-1)
    table=lt.new_list()
    for i in range(capacity):
        lt.add_last(table, {"key":None,"value":None})
    my_table={"prime":prime,"capacity":capacity,"scale":scale,"shift":shift,"table":table,"current_factor":0,"limit_factor":load_factor,"size":0}
    my_table['scale'] = 1
    my_table['shift'] = 0
    return my_table

def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if mf.is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = lt.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif mf.default_compare(key, lt.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail

def contains(my_map,key):
    return mf.find_slot(my_map,key,mf.hash_value(my_map,key))[0]

def get(my_map, key):
    slot = mf.find_slot(my_map, key, mf.hash_value(my_map, key))
    if not slot[0]:
        return None
    entry = my_map["table"]["elements"][slot[1]]
    value = entry.get("value") if entry else None
    return value

def remove(my_map, key):
    slot=find_slot(my_map,key,mf.hash_value(my_map,key))
    if slot[0]:
        my_map["table"]["elements"][slot[1]]={"key":"__EMPTY__", "value":"__EMPTY__"}
        my_map["size"]-=1
        my_map["current_factor"]=my_map["size"]/my_map["capacity"]
    return my_map

def contains(my_map,key):
    slot=mf.find_slot(my_map,key,mf.hash_value(my_map,key))
    return slot[0]

def size(my_map):
    return my_map["size"]

def put(my_map, key, value):
    hash=mf.hash_value(my_map,key)
    slot=mf.find_slot(my_map,key,hash)
    if not slot[0]:
        my_map["size"]+=1
        my_map["current_factor"]=my_map["size"]/my_map["capacity"]
        my_map["table"]["elements"][slot[1]]={"key":key,"value":value}
        if my_map["current_factor"]>my_map["limit_factor"]:
            
            rehash(my_map)
    else:
        my_map["table"]["elements"][slot[1]]={"key":key,"value":value}
    return my_map
        
def rehash(my_map):
    n_map=new_map(my_map["capacity"]*2,my_map["limit_factor"])
    for i in range(my_map["capacity"]):
        if my_map["table"]["elements"][i]["key"]!=None:
            put(n_map, my_map["table"]["elements"][i]["key"],my_map["table"]["elements"][i]["value"])
    my_map=n_map
    return n_map

def is_empty(my_map):
    return my_map["size"]==0
    
def is_available(table, pos):
    entry = lt.get_element(table, pos)
    key = me.get_key(entry)
    if key is None or key == "__EMPTY__":
        return True
    return False

def key_set(my_map):
    keys=lt.new_list()
    for i in my_map["table"]["elements"]:
        if i["key"]!=None and i["key"]!="__EMPTY__":
            lt.add_last(keys, i["key"])
    return keys

def value_set(my_map):
    values=lt.new_list()
    for i in my_map["table"]["elements"]:
        if i["key"]!=None and i["key"]!="__EMPTY__":
            lt.add_last(values, i["value"])
    return values