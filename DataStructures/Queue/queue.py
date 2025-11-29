def new_queue():
    newqueue = {
        "size": 0,
        "elements": [],
    }
    return newqueue

def enqueue(my_queue, item):
    my_queue["elements"].insert(len(my_queue["elements"]),item)
    my_queue["size"] += 1
    return my_queue

def dequeue(my_queue):
    if my_queue["size"] > 0:
        item = my_queue["elements"].pop(0)
        my_queue["size"] -= 1
        return item
    else:
        raise Exception('EmptyStructureError: queue is empty')

def peek(my_queue):
    if my_queue["size"]==0:
        raise Exception('EmptyStructureError: queue is empty')
    else:
        return my_queue["elements"][0]
    
def is_empty(my_queue):
    return my_queue["size"]== 0

def size(my_queue):
    return my_queue["size"]