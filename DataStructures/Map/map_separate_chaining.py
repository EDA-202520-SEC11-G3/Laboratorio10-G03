from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll
from . import map_functions as mf
from . import map_entry as me
import random

def new_map(num_elements,load_factor,prime=109345121):
    capacity=mf.next_prime(num_elements/load_factor)
    scale=random.randint(1, prime-1)
    shift=random.randint(0, prime-1)
    table=lt.new_list()
    for i in range(capacity):
        lt.add_last(table, sll.new_list())
    my_table={"prime":prime,"capacity":capacity,"scale":scale,"shift":shift,"table":table,"current_factor":0,"limit_factor":load_factor,"size":0}
    my_table['scale'] = 1
    my_table['shift'] = 0
    return my_table

def put(my_map, key, value):
    hash=mf.hash_value(my_map,key)
    if sll.is_empty(my_map["table"]["elements"][hash]):
        sll.add_last(my_map["table"]["elements"][hash],{"key":key,"value":value})
        my_map["size"]+=1
        my_map["current_factor"]=my_map["size"]/my_map["capacity"]
        if my_map["current_factor"]>my_map["limit_factor"]:
            rehash(my_map)
        return my_map
    else:
        i=0
        current=my_map["table"]["elements"][hash]["first"]
        while i<my_map["table"]["elements"][hash]["size"]:
            if current["info"]["key"]==key:
                sll.change_info(my_map["table"]["elements"][hash],i,{"key":key,"value":value})
                return my_map
            current=current["next"]
            i+=1
    sll.add_last(my_map["table"]["elements"][hash],{"key":key,"value":value})
    my_map["size"]+=1
    my_map["current_factor"]=my_map["size"]/my_map["capacity"]
    if my_map["current_factor"]>my_map["limit_factor"]:
        rehash(my_map)
    return my_map
        
def rehash(my_map):
    new_size=mf.next_prime(my_map["capacity"]*2)
    new_table=lt.new_list()
    for i in range(new_size):
        lt.add_last(new_table, sll.new_list())
    i=0
    k=0
    while i<my_map["size"]:
        if not sll.is_empty(my_map["table"]["elements"][k]):
            for j in range(my_map["table"]["elements"][k]["size"]):
                entry=sll.get_element(my_map["table"]["elements"][k],j)
                key=me.get_key(entry)
                value=me.get_value(entry)
                hash=mf.hash_value(my_map,key)
                sll.add_last(new_table["elements"][hash],{"key":key,"value":value})
                i+=1
        k+=1
    my_map["table"]=new_table
    my_map["capacity"]=new_size
    my_map["load_factor"]=my_map["size"]/new_size
    return my_map

def contains(my_map, key):
    hash=mf.hash_value(my_map,key)
    if sll.is_empty(my_map["table"]["elements"][hash]):
        return False
    else:
        i=0
        current=my_map["table"]["elements"][hash]["first"]
        while i<my_map["table"]["elements"][hash]["size"]:
            if current["info"]["key"]==key:
                return True
            current=current["next"]
            i+=1
        return
    
def get(my_map, key):
    hash=mf.hash_value(my_map,key)
    if sll.is_empty(my_map["table"]["elements"][hash]):
        return None
    else:
        i=0
        current=my_map["table"]["elements"][hash]["first"]
        while i<my_map["table"]["elements"][hash]["size"]:
            if current["info"]["key"]==key:
                return current["info"]["value"]
            current=current["next"]
            i+=1
        return None
    
def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"]==0

def key_set(my_map):
    keyset=lt.new_list()
    i=0
    k=0
    while i<my_map["size"]:
        if not sll.is_empty(my_map["table"]["elements"][k]):
            for j in range(my_map["table"]["elements"][k]["size"]):
                entry=sll.get_element(my_map["table"]["elements"][k],j)
                lt.add_last(keyset, entry["key"])
                i+=1
        k+=1
    return keyset

def value_set(my_map):
    valueset=lt.new_list()
    i=0
    k=0
    while i<my_map["size"]:
        if not sll.is_empty(my_map["table"]["elements"][k]):
            for j in range(my_map["table"]["elements"][k]["size"]):
                entry=sll.get_element(my_map["table"]["elements"][k],j)
                lt.add_last(valueset, entry["value"])
                i+=1
        k+=1
    return valueset

def remove(my_map, key):
    hash=mf.hash_value(my_map,key)
    if sll.is_empty(my_map["table"]["elements"][hash]):
        return my_map
    else:
        i=0
        current=my_map["table"]["elements"][hash]["first"]
        while i<my_map["table"]["elements"][hash]["size"]:
            if current["info"]["key"]==key:
                sll.delete_element(my_map["table"]["elements"][hash],i)
                my_map["size"]-=1
                my_map["load_factor"]=my_map["size"]/my_map["capacity"]
                return my_map
            current=current["next"]
            i+=1
        return my_map