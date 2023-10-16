from random import shuffle

# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

    node_values = args
    shuffle(node_values)
    choice = node_values.pop(0)
    return (choice, node_values)