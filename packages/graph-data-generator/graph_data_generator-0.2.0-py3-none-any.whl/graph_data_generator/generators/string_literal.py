# Do not change function name or arguments
def generate(args: list[any]):
    result = args[0]
    if isinstance(result, str) is False:
        result = str(result)
    return result