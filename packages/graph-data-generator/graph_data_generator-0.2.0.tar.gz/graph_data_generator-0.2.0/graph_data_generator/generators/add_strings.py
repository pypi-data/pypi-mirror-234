

from graph_data_generator.models.generator import Generator
def generate(args: list[any]):
    """
    Aggregates outputs from other generators.

    Args:
    args (list[any]): A list of (generator, args) to run.

    Returns:
    string: Aggregate string output from specified generators
    """
    result = ""
    for gen, gen_args in args:
        result += gen.generate(gen_args)
    return result
