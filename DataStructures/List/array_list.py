def new_list():
    newlist = {
        'elements': [],
        'size': 0} 
    return newlist

def get_element(my_list, index):

    return my_list["elements"][index]

def is_present(my_list, element, cmp_function):
    if my_list is None:
        return -1
    size = my_list["size"]
    if size > 0:
        keyexist = False 
        for keypos in range(0,size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
                keyexist = True
                break 
        if keyexist:
            return keypos
    return -1

def add_first(my_list, element):
    my_list["elements"].insert(0,element)
    my_list["size"] +=1

    return my_list
        
def add_last(my_list, element):
    if my_list is None:
        my_list = new_list()
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list

def size(my_list):
    if my_list is None:
        return 0
    return my_list["size"]

def first_element(my_list):
    if my_list["size"] == 0:
        return None 
    return my_list["elements"][0]

def is_empty(my_list):
    if my_list["size"] == 0:
        return True
    else:
        return False
def remove_first(my_list):
    my_list["size"] -=1
    return my_list["elements"].pop(0)

def remove_last(my_list):
    my_list["size"] -=1
    return my_list["elements"].pop(-1)

def insert_element(my_list,element,pos):
    my_list["elements"].insert(pos, element)
    my_list["size"] +=1
    return my_list

def delete_element(my_list,pos):
    del my_list["elements"][pos]
    my_list["size"] -=1
    return my_list

def change_info(my_list, pos, new_info):
    my_list["elements"][pos] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    x = pos_1
    y = pos_2
    my_list["elements"][pos_1] = my_list["elements"][y]
    my_list["elements"][pos_2] = my_list["elements"][x]
    return my_list 

def sub_list(my_list, pos_i, num_elements):
    new = {
        "elements": [],
        "size": 0
    }
    if (
        my_list is None or
        my_list.get("elements") is None or
        pos_i < 0 or
        pos_i + num_elements > size(my_list)
    ):
        return new
    for i in range(num_elements):
        new["elements"].append(my_list["elements"][pos_i + i])
        new["size"] += 1
    return new

def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def selection_sort(my_list, sort_crit):
    elements = my_list["elements"]
    n = my_list["size"]
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if sort_crit(elements[j], elements[min_idx]):
                min_idx = j
        elements[i], elements[min_idx] = elements[min_idx], elements[i]
    return my_list

def insertion_sort(my_list, sort_crit):
    elements = my_list["elements"]
    n = my_list["size"]
    for i in range(1, n):
        key = elements[i]
        j = i - 1
        while j >= 0 and sort_crit(key, elements[j]):
            elements[j + 1] = elements[j]
            j -= 1
        elements[j + 1] = key
    return my_list

def shell_sort(my_list, cmp_function):
    n = my_list["size"]
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = my_list["elements"][i]
            j = i
            while j >= gap and cmp_function(temp, my_list["elements"][j - gap]) < 0:
                my_list["elements"][j] = my_list["elements"][j - gap]
                j -= gap
            my_list["elements"][j] = temp
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

def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def selection_sort(my_list, sort_crit):
    for i in range(my_list["size"]):
        for j in range(my_list["size"]):
            menor = max(my_list["elements"])
            vale_o_novale = 0
            ind = 0
            if default_sort_criteria(my_list["elements"][j],menor):
                my_list["elements"].index(menor)
                vale_o_novale = menor 
                menor = my_list["elements"][j]
        my_list["elements"][ind] = vale_o_novale
        my_list["elements"][i] = menor

def shell_sort(my_list, sort_crit):
    n = len(my_list)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = my_list[i]
            j = i
            while j >= gap and not sort_crit(my_list[j - gap], temp):
                my_list[j] = my_list[j - gap]
                j -= gap
            my_list[j] = temp
        gap //= 2
    return my_list

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

def quick_sort(my_list, cmp_function):
    if my_list["size"] <= 1:
        return my_list

    pivot = get_element(my_list, my_list["size"] // 2)
    left, right, equal = new_list(), new_list(), new_list()

    for i in range(my_list["size"]):
        element = get_element(my_list, i)
        cmp = cmp_function(element, pivot)
        if cmp < 0:
            add_last(left, element)
        elif cmp > 0:
            add_last(right, element)
        else:
            add_last(equal, element)

    left = quick_sort(left, cmp_function)
    right = quick_sort(right, cmp_function)

    result = new_list()
    for i in range(left["size"]):
        add_last(result, get_element(left, i))
    for i in range(equal["size"]):
        add_last(result, get_element(equal, i))
    for i in range(right["size"]):
        add_last(result, get_element(right, i))
    return result