
from graph_data_generator.models.generator import Generator, GeneratorType
from graph_data_generator.logger import ModuleLogger
import json
import re
from datetime import datetime

# ORIGINAL GENERATOR ASSIGNMENT
def actual_generator_for_raw_property(
    property_value: str, 
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """Returns a generator and args for a property. Returns None if not found."""
    # Sample property_values: 
    #   "{\"company_name\":[]}"
    
    if isinstance(property_value, str):
        try:
            obj = json.loads(property_value)
        except Exception as e:
            ModuleLogger().warning(f'Could not parse JSON string: {property_value}')
            return (None, None)
    elif isinstance(property_value, dict):
        obj = property_value
    else:
        ModuleLogger().error(f'Raw Generator values must by of type str or dict. {property_value} received.')
    # Should only ever be one match. Return first
    for key, value in obj.items():
        generator_id = key
        generator = generators.get(generator_id, None)

        # Check special function generators
        if generator is not None and generator.type == GeneratorType.FUNCTION:
            # Extract the generators from the args and pass tuples of (Generator, Args) as higher level args 
            ModuleLogger().debug(f'Function generator {generator.name} detected. Arg value: {value}')

            # Value of function generators is a list of JSON object specifications for other generators. Retrieve these and insert them as arg values to be run by the actual function generators that are expecting tuples of (Generator, Args)
            new_value = []
            for gen_spec in value:
                gen, args = generator_for_raw_property(gen_spec, generators)
                new_value.append((gen, args))
            value = new_value
            
        if generator is None:
            ModuleLogger().warning(f'Generator_id "{generator_id}" not found in generators.')
            return (None, None)
        args = value
        return (generator, args)

    return (None, None)

# KEYWORD GENERATOR ASSIGNMENT
def keyword_generator_for_raw_property(
    value: str,
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """Returns a generator and args for a property value using a generic keyword. Returns None if not found."""

    result = None

    # Is an object? Not a keyword generator then
    if isinstance(value, dict):
        return (None, None)
    
    # Not a string? Then can't be a keyword generator
    if isinstance(value, str) == False:
         return (None, None)
    
    if value.lower() == "string":
            result = {
                "lorem_words": [1,3]
            }
    elif value.lower() == "int" or value.lower() == "integer":
            result = {
                "int_range": [1,100]
            }
    elif value.lower() == "float":
            result = {
                "float_range": [1.0,100.0, 2]
            }
    elif value.lower() == "bool":
            result = {
                "bool": [50]
            }
    elif value.lower() == "boolean":
            result = {
                "bool": [50]
            }
    elif value.lower() == "date":
            today = datetime.now().strftime('%Y-%m-%d')
            result = {
                "date": ["1970-01-01", f"{today}"]
            }     
    elif value.lower() == "datetime":
            today = datetime.now().strftime('%Y-%m-%d')
            result = {
                "date": ["1970-01-01", f"{today}"]
            }

    # Default
    if result is None:
        return (None, None)
    
    # Generator was assigned
    g_config = json.dumps(result)
    return actual_generator_for_raw_property(g_config, generators)


# LITERAL GENERATOR ASSIGNMENT SUPPORT
def all_ints(values: list[str]) -> bool:
    for value in values:
        if not is_int(value):
            return False
    return True

def some_floats(values: list[str]) -> bool:
    for value in values:
        if is_float(value):
            return True
    return False

def all_floats(values: list[str]) -> bool:
    for value in values:
        if not is_float(value):
            return False
    return True

def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False
    
def is_float(value: str) -> bool:
    try:
        _ = float(value)
        return True
    except ValueError:
        return False
    
def find_longest_float_precision(float_list):
    max_precision = 0
    for num in float_list:
        num_str = str(num)
        if '.' in num_str:
            decimal_part = num_str.split('.')[1]
            precision = len(decimal_part)
            max_precision = max(max_precision, precision)
    return max_precision

def extract_numbers(string):
    # Use regex to find all number patterns in the string
    number_list = re.findall(r"-?\d+(?:\.\d+)?", string)

    # Convert the extracted strings to appropriate number types
    number_list = [int(num) if num.isdigit() else float(num) for num in number_list]

    return number_list

def numbers_list_from(string):
    # numbers = []
    # ranges = string.split('-')
    # for r in ranges:
    #     numbers.extend(extract_numbers(r))
    # return numbers 
    options = re.split(r'(?<=[^-])-', string)
    return options

def literal_generator_from_value(
        value: str,
        generators: list[Generator]
    )-> tuple[Generator, list[any]]:
    """
        Attempts to find an actual generator based on more concise literal values from arrows.app JSON

        Support for:
            - ints
            - floats
            - ranges of ints
            - ranges of floats
            - lists of ints
            - lists of floats
            - string literals
            - list of strings

        TODO:
            - bools
            - lists of bools
            - date
            - lists of dates
            - datetime (ISO 8601)
            - list of datetimes
    """
    # Sample expected values: 
    #   "1"
    #   "1-10"
    #   "[3, 5, 10]"
    #   "[Yes, No]"
    #   "[True, False, False]"

    # Original specificaion took stringified JSON objects to notate generator and args to use. We're going to convert matching literal values to appropriate generators
    
    result = None

    # Dictionary objects are usually JSON specifications for generators
    # In any case, no literal generator based on such an object anyways
    if isinstance(value, dict):
         return None, None
    
    # Check if value is an int or float
    if is_int(value):
        integer = int(value)
        result = {
            "int": [integer]
        }

    if result is None and is_float(value):
        f = float(value)
        result = {
            "float": [f]
        }

    # NOTE: Not currently handling complex literals
     
    # Check if value is a range of positive ints or floats
    if result is None:
        numbers = numbers_list_from(value) 
        if len(numbers) == 2:
        # Check for correctly formatted int or float range string
            precision = find_longest_float_precision(numbers)
            if precision == 0:
                    result = {
                        "int_range": [int(numbers[0]), int(numbers[1])]
                    }
            else:
                    result = {
                        "float_range": [float(numbers[0]), float(numbers[1]), precision]
                    }

    # Check for literal list of ints, floats, or strings
    if result is None and value.startswith('[') and value.endswith(']'):
        values = value[1:-1].split(',')
        # Generators take a strange format where the args are always a string - including # lists of other data, like ints, floats. ie ["1,2,3"] is an expected arg type
        # because certain generators could take multiple args from different text fields
        # These literals, however, all only take a single generic arg

        # YES - this is terrible
        
        if all_ints(values):
            ints_as_string = ",".join([f'{int(v)}' for v in values])
            result = {
                "int_from_list": [f"{ints_as_string}"]
            }
        elif some_floats(values):
            floats_as_string = ",".join([f'{float(v)}' for v in values])
            result = {
                "float_from_list": [f"{floats_as_string}"]
            }
        else:
            result = {
                "string_from_list": [f"{value[1:-1]}"]
            }

    # Return nothing, so caller knows no generator was matched
    if result is None:
         return None, None

    # Package and return from legacy process
    actual_string = json.dumps(result)
    return actual_generator_for_raw_property(actual_string, generators)

def assignment_generator_for(
    config: str,
    generators: dict[str, Generator]
) -> tuple[Generator, list[any]]:
    
    gen, args =  actual_generator_for_raw_property(config, generators)
    if gen.type != GeneratorType.ASSIGNMENT:
        ModuleLogger().error(f'Generator {gen.name} is not an assignment generator.')
        return (None, None)
    return gen, args

def generator_for_raw_property(
    property_value: any, 
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """
        Returns a generator and args for specially formatted property values from the arrows.app JSON file. Attempts to determine if literal or original generator
        specification was use.

        Return None if no generator found.
    """

    generator, args = None, None

    # Supports literals like 1, 1-10, etc
    # Check for new literal assignments
    # Returns None if no matching generator found
    if generator is None: 
        generator, args = literal_generator_from_value(property_value, generators)

    # For supporting following options: "string", "bool", "boolean", "float", "integer", "number", "date", "datetime"
    if generator is None:
        generator, args = keyword_generator_for_raw_property(property_value, generators)

    # Original Sample expected string: "{\"company_name\":[]}"
    # New literal examples: 
    #     "{\"company_name\":\"Acme\"}"
    #     "{\"company_name\":[\"Acme\"]}"
    #     "{\"company_name\":\"string\"}"
    # Function generators are also handled here
    # Returns None if no matching generator found
    if generator is None:
        generator, args = actual_generator_for_raw_property(property_value, generators)


    # Default is to use string literal generator
    if generator is None:
        ModuleLogger().debug(f"No generator found for property value: {property_value}. Defaulting to string literal generator")
        default = {
            "string": [f"{property_value}"]
        }
        generator, args = actual_generator_for_raw_property(default, generators)
 
    return (generator, args)