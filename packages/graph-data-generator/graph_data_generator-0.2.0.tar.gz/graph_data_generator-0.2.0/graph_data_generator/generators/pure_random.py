import random
# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:
    to_node_values = args
    result = random.choice(to_node_values)
    return (result, to_node_values)