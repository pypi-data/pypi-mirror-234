
import io
import json

from graph_data_generator.logic.generate_zip import generate_zip
from graph_data_generator.logic.generate_mapping import mapping_from_json

# Here also to expose for external use
from graph_data_generator.models.generator import Generator, generators_from_json
from graph_data_generator.models.generator_arg import GeneratorArg
from graph_data_generator.models.generator_type import GeneratorType
from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logger import ModuleLogger

VERSION = "0.2.0"

def generate(
    json_source : any,
    output_format : str = 'bytes',
    enable_logging : bool = False
) -> io.BytesIO:
    """
    Generates a zip file of data based on the provided JSON object.

    Args:
        json_source (any): A stringified JSON or dict object containing the mapping of nodes and relationships to generate.
        output_format (str, optional): The format of the output. Defaults to 'bytes' which can be added directly to a flask make_response() call. Otther options are 'string'.
    """
    # Validate json

    # jsonschema package did not work with pytest
    # from jsonschema import validate
    # try:
    #     validate(instance=json_object, schema=arrows_json_schema)
    # except jsonschema.exceptions.ValidationError as e:
    #     raise Exception("Invalid JSON object provided.")
    # except jsonschema.exceptions.SchemaError as e:
    #     raise Exception("Base JSON schema invalid. Contact developer")
    # except Exception as e:
    #     raise Exception(f"Unknown error validating JSON object. {e} Contact developer")

    # TODO: Replace with a enum for output_format or arg for a logger object
    if enable_logging is True:
        logger = ModuleLogger()
        logger.is_enabled = True
        logger.info(f'Logging enabled')

    # If json_object is a string, load and convert into a dict object
    if isinstance(json_source, str) is True:
        try:
            json_source = json.loads(json_source)
        except Exception as e:
            raise Exception(f'json_source string not a valid JSON format: {e}')
    
    # TODO: Check the dict key-value format matches what we're expecting
    
    # Create mapping file
    mapping, error_msg = mapping_from_json(
        json_source, 
        generators
    )
    if mapping is None:
        raise Exception(error_msg)
    if mapping.is_empty():
        raise Exception(f"No nodes or relationships generated. Check input file")

    # Generate output and return as bytes of a zip file
    bytes, error_msg = generate_zip(
        mapping
    )
    if bytes is None:
        raise Exception(error_msg)
    if error_msg is not None:
        ModuleLogger().error(error_msg)

    if output_format == 'string':
        data_bytes = bytes.getvalue()
        result = data_bytes.decode('utf-8')
    else:
        bytes.seek(0)
        result = bytes.getvalue()

    return result