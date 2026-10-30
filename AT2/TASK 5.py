def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order


print(add_item_buggy("Tea"), add_item_buggy("Vada"))

print(add_item("Tea"))
print(add_item("Vada"))

print(add_item_buggy.__defaults__)