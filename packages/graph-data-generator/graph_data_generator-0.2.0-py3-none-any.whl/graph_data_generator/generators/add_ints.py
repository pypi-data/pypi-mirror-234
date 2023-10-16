
from graph_data_generator.models.generator import Generator

def generate(args: list[any]):
    """
    Generate a sum of outputs from number generators.

    Args:
    args (list[any]): A list of generator specification to run and whose results to sum.

    Returns:
    int: Sum of outputs from specified number generators
    """
    result = 0
    for gen, gen_args in args:
        value = gen.generate(gen_args)
        result += int(value)
    return result