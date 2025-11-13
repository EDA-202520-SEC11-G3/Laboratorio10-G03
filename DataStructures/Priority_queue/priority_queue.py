import DataStructures.List.array_list as lt
import DataStructures.Priority_queue.pq_entry as pqentry

def default_compare_higher_value(a, b):
    return a > b

def default_compare_lower_value(a, b):
    return a < b

def new_heap(cmp_function=None):
    if cmp_function is None:
        cmp_function = default_compare_lower_value
    return {
        "size": 0,
        "elements": lt.new_list(),
        "cmp_function": cmp_function
    }

def size(heap):
    return heap["size"]

def is_empty(heap):
    return heap["size"] == 0

def exchange(heap, i, j):
    e_i = lt.get_element(heap["elements"], i)
    e_j = lt.get_element(heap["elements"], j)
    heap["elements"]["elements"][i] = e_j
    heap["elements"]["elements"][j] = e_i

def priority(heap, entry1, entry2):
    return heap["cmp_function"](pqentry.get_priority(entry1), pqentry.get_priority(entry2))

def swim(heap, k):
    while k > 0 and priority(heap, lt.get_element(heap["elements"], k), lt.get_element(heap["elements"], (k-1)//2)):
        exchange(heap, k, (k-1)//2)
        k = (k-1)//2

def insert(heap, priority, value):
    entry = {"priority": priority, "value": value}
    lt.add_last(heap["elements"], entry)
    heap["size"] += 1
    swim(heap, size(heap)-1)

def sink(heap, k):
    n = size(heap)
    while 2*k + 1 < n:
        j = 2*k + 1
        if j + 1 < n and priority(heap, lt.get_element(heap["elements"], j+1), lt.get_element(heap["elements"], j)):
            j += 1
        if priority(heap, lt.get_element(heap["elements"], k), lt.get_element(heap["elements"], j)):
            break
        exchange(heap, k, j)
        k = j

def remove(heap):
    if is_empty(heap):
        return None
    n = size(heap)
    exchange(heap, 0, n-1)
    removed = lt.remove_last(heap["elements"])
    heap["size"] -= 1
    if not is_empty(heap):
        sink(heap, 0)
    return pqentry.get_value(removed)

def get_first_priority(heap):
    if is_empty(heap):
        return None
    return pqentry.get_priority(lt.get_element(heap["elements"], 0))

def contains(heap, value):
    return is_present_value(heap, value) != -1

def is_present_value(heap, value):
    for i in range(size(heap)):
        entry = lt.get_element(heap["elements"], i)
        if pqentry.get_value(entry) == value:
            return i  # Retornar índice como exigen los tests
    return -1

def improve_priority(heap, value, newpriority):
    idx = is_present_value(heap, value)
    if idx != -1:
        entry = lt.get_element(heap["elements"], idx)
        pqentry.set_priority(entry, newpriority)
        swim(heap, idx)
        return True
    return False