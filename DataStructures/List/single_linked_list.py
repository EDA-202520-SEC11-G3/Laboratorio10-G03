def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size": 0
    }
    return newlist

def get_element(my_list, pos):
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    return node["info"]

def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else:
            temp = temp["next"]
            count += 1
            
    if not is_in_array:
        count = -1
    return count

def add_first(my_list, element):
    new_node = {
        "info": element,
        "next": None
    }
    if my_list["first"] is None:
        my_list["first"] = new_node
        my_list["last"] = new_node
    else:
        new_node["next"] = my_list["first"]
        my_list["first"] = new_node
    if my_list["size"] is None:
        my_list["size"] = 1
    else:
        my_list["size"] += 1
    
    return my_list
        
def add_last(my_list, element):
    if my_list is None:
        my_list = new_list()
    new_node = {
        "info": element,
        "next": None
    }
    
    if my_list["first"] is None:
        my_list["first"] = new_node
        my_list["last"] = new_node
    else:
        my_list["last"]["next"] = new_node
        my_list["last"] = new_node
        
    if my_list["size"] is None:
        my_list["size"] = 1
    else:
        my_list["size"] += 1
        
    return my_list

def size(my_list):
    return my_list["size"]

def first_element(my_list):
    if my_list["first"] is not None:
        return my_list["first"]["info"]
    else:
        return None
    
def is_empty(my_list):
    if my_list["size"] == 0:
        return True
    else:
        return False


def last_element(my_list):
    return my_list["last"]

def remove_first(my_list):
    if is_empty(my_list):
        return None 
    eliminado = my_list["first"]
    nodo = my_list["first"]
    my_list["first"] = nodo["next"]
    my_list["size"] -= 1
    if my_list["size"] == 0:
        my_list["last"]= None
    return eliminado["info"]

def remove_last(my_list):
    if is_empty(my_list):
        return None 
    eliminado = my_list["last"]
    nodo = my_list["last"]
    my_list["last"] = nodo["next"]
    my_list["size"] -= 1
    if my_list["size"] == 0:
        my_list["first"]= None
    return eliminado["info"]

def insert_element(my_list, value, pos):
    nuevo = {
        "info":value,
        "next": None
    }
    if pos >= my_list['size']:
        if is_empty(my_list):
            my_list['first'] = nuevo
            my_list['last'] = nuevo
        else:
            my_list['last']['next'] = nuevo
            my_list['last'] = nuevo
        my_list['size'] += 1
        return nuevo
    elif pos <= 0:
        nuevo['next'] = my_list['first']
        my_list['first'] = nuevo
        if my_list['size'] == 0:
            my_list['last'] = nuevo
        my_list['size'] += 1
        return nuevo
    else:
        actual = my_list['first']
        for i in range(pos - 1):
            actual = actual['next']
        nuevo['next'] = actual['next']
        actual['next'] = nuevo
        if nuevo['next'] is None:
            my_list['last'] = nuevo
        my_list['size'] += 1
        return nuevo

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception('IndexError: list index out of range')
    if pos == 0:
        remove_first(my_list)
    else:
        prev = my_list["first"]
        for _ in range(pos - 1):
            prev = prev["next"]
        eliminado = prev["next"]
        prev["next"] = eliminado["next"]
        if eliminado == my_list["last"]:
            my_list["last"] = prev
        my_list["size"] -= 1
    return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception('IndexError: list index out of range')
    nodo = my_list["first"]
    for _ in range(pos):
        nodo = nodo["next"]
    nodo["info"] = new_info
    if nodo["next"] is None:
        my_list["last"]["info"] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    if pos_1 < 0 or pos_2 < 0 or pos_1 >= my_list["size"] or pos_2 >= my_list["size"]:
        raise Exception('IndexError: list index out of range')
    if pos_1 == pos_2:
        return my_list
    nodo1 = my_list["first"]
    nodo2 = my_list["first"]
    for _ in range(pos_1):
        nodo1 = nodo1["next"]
    for _ in range(pos_2):
        nodo2 = nodo2["next"]
    nodo1["info"], nodo2["info"] = nodo2["info"], nodo1["info"]
    return my_list

def sub_list(my_list, pos, num_elements):
    if pos < 0 or pos >= my_list["size"] or num_elements < 0 or (pos + num_elements) > my_list["size"]:
        raise Exception('IndexError: list index out of range')
    nueva_lista = new_list()
    actual = my_list["first"]
    for _ in range(pos):
        actual = actual["next"]
    for _ in range(num_elements):
        add_last(nueva_lista, actual["info"])
        actual = actual["next"]
    return nueva_lista

def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def selection_sort(my_list, cmp_function):
    size = my_list["size"]
    for i in range(size - 1):
        min_index = i
        for j in range(i + 1, size):
            if cmp_function(get_element(my_list, j), get_element(my_list, min_index)) < 0:
                min_index = j
        if min_index != i:
            exchange(my_list, i, min_index)
    return my_list

def insertion_sort(my_list, cmp_function):
    size = my_list["size"]
    for i in range(1, size):
        j = i
        while j > 0 and cmp_function(get_element(my_list, j), get_element(my_list, j - 1)) < 0:
            exchange(my_list, j, j - 1)
            j -= 1
    return my_list

def shell_sort(my_list, cmp_function):
    size = my_list["size"]
    gap = size // 2
    while gap > 0:
        for i in range(gap, size):
            j = i
            while j >= gap and cmp_function(get_element(my_list, j), get_element(my_list, j - gap)) < 0:
                exchange(my_list, j, j - gap)
                j -= gap
        gap //= 2
    return my_list

def merge_sort(my_list, cmp_function):
    if my_list["size"] <= 1:
        return my_list

    mid = my_list["size"] // 2
    left = sub_list(my_list, 0, mid)
    right = sub_list(my_list, mid, my_list["size"] - mid)

    left = merge_sort(left, cmp_function)
    right = merge_sort(right, cmp_function)

    return merge(left, right, cmp_function)


def merge(left, right, cmp_function):
    result = new_list()
    i, j = 0, 0
    while i < left["size"] and j < right["size"]:
        if cmp_function(get_element(left, i), get_element(right, j)) <= 0:
            add_last(result, get_element(left, i)); i += 1
        else:
            add_last(result, get_element(right, j)); j += 1
    while i < left["size"]:
        add_last(result, get_element(left, i)); i += 1
    while j < right["size"]:
        add_last(result, get_element(right, j)); j += 1
    return result

def quick_sort(my_list, sort_crit):
    if my_list["size"] <= 1:
        return my_list
    my_list["first"] = _quick_sort_nodes(my_list["first"], sort_crit)
    size = 0
    node = my_list["first"]
    prev = None
    while node:
        size += 1
        prev = node
        node = node["next"]

    my_list["size"] = size
    my_list["last"] = prev
    return my_list

def _quick_sort_nodes(head, compare):
    if head is None or head["next"] is None:
        return head

    pivot = head               # tomamos el primer nodo como pivote
    less_head = less_tail = None
    greater_head = greater_tail = None

    # Particionar el resto de la lista
    node = head["next"]
    pivot["next"] = None       # desconectamos el pivote para trabajar limpio
    while node:
        nxt = node["next"]
        node["next"] = None
        if compare(node["info"], pivot["info"]):
            if less_head is None:
                less_head = less_tail = node
            else:
                less_tail["next"] = node
                less_tail = node
        else:
            if greater_head is None:
                greater_head = greater_tail = node
            else:
                greater_tail["next"] = node
                greater_tail = node
        node = nxt

    # Ordenar sublistas
    less_head    = _quick_sort_nodes(less_head, compare)
    greater_head = _quick_sort_nodes(greater_head, compare)

    # Unir: menores + pivote + mayores
    if less_head:
        head = less_head
        tail = less_head
        while tail["next"]:
            tail = tail["next"]
        tail["next"] = pivot
    else:
        head = pivot
    pivot["next"] = greater_head

    return head