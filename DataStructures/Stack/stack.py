def new_stack():
    newstack={
        "size":0,
        "first":None,
        "last":None
    }
    return newstack
    
def push(my_stack, element):
    node = my_stack["first"]
    my_stack["first"] = element
    my_stack["first"]["next"] = node 
    my_stack["size"] += 1
    return my_stack

def pop(my_stack):
    if my_stack["size"] == 0:
        raise Exception('EmptyStructureError: stack is empty')
    if my_stack["size"] == 1:
        it = my_stack["first"]
        my_stack["first"] = None
        my_stack["last"] = None
        my_stack["size"] = 0 
        return it 
    next = my_stack["first"]
    item = my_stack.pop("first")
    my_stack["first"] = next["next"]
    my_stack["size"] -= 1
    return item

def is_empty(my_stack):
    return my_stack["size"] == 0

def top(my_stack):
    if my_stack["size"] == 0:
        raise Exception('EmptyStructureError: stack is empty')
    item = my_stack.get("first")
    return item

def size(my_stack):
    return my_stack["size"]



        