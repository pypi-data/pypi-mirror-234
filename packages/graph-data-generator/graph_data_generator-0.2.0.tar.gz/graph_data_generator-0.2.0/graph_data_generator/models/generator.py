# from enum import Enum, unique
from graph_data_generator.models.generator_type import GeneratorType
from graph_data_generator.models.generator_arg import GeneratorArg
from graph_data_generator.logger import ModuleLogger
import re


class Generator():

    # TODO: Support pattern generation and property based values
    @staticmethod
    def from_dict(
        generator_dict: dict
    ):
        if 'gid' not in generator_dict.keys():
            raise Exception("Generator must have a gid property")
        if 'name' not in generator_dict.keys():
            raise Exception("Generator must have a name")
        if 'type' not in generator_dict.keys():
            raise Exception("Generator must have a type")
        if 'description' not in generator_dict.keys():
            raise Exception("Generator must have a description")
        if 'code' not in generator_dict.keys():
            raise Exception("Generator must have code")
        if 'args' not in generator_dict.keys():
            args = []
        else :
            args = GeneratorArg.list_from(generator_dict['args'])
        if 'tags' not in generator_dict.keys():
            tags = []
        else:
            tags = generator_dict['tags']
        
        return Generator(
            type = GeneratorType.type_from_string(generator_dict['type']),
            gid = generator_dict['gid'],
            name = generator_dict['name'],
            description = generator_dict['description'],
            code = generator_dict['code'],
            args = args,
            tags = tags
        )

    @staticmethod
    def empty():
        return Generator(
            gid = "",
            type = GeneratorType.UNKNOWN,
            name = "",
            description = "",
            code = "",
            args = [],
            tags = []
        )
    
    def __init__(
        self, 
        gid: str,
        name: str, 
        type : GeneratorType, 
        description: str, 
        code : any,
        # Information on arguments the generator CAN take. 
        # Argument values to use during generate are passed in the generate call
        args: list[GeneratorArg],
        tags: list[str]
        ):
        self.gid = gid
        self.name = name
        self.description = description
        self.code = code
        self.args = args
        self.type = type
        self.tags = tags

    def to_dict(self):
        return {
            "gid": self.gid,
            "name": self.name,
            "description": self.description,
            "code": self.code.name,
            "args": [arg.to_dict() for arg in self.args],
            "type": self.type.to_string(),
            "tags": self.tags
        }

    def __str__(self):
        return f'Generator: gid: {self.gid}, name: {self.name}, type: {self.type}, args: {self.args}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Generator) == False:
            return False
        if self.gid != other.gid:
            return False
        if self.name != other.name:
            return False
        if self.description != other.description:
            return False
        if self.code != other.code:
            return False
        if self.args != other.args:
            return False
        if self.type != other.type:
            return False
        if self.tags != other.tags:
            return False 
        return True

    def generate(self, args):  
        result = self.code.generate(args)
        return result
    
def generators_from_json(json : dict) -> dict:
    result = {}
    for key in json.keys():
        if key == "README":
            # Special key for embedding notes in the json 
            # Hacky but whatever
            continue
        data = json[key]
        data['gid'] = key
        generator = Generator.from_dict(data)
        result[key] = generator
    return result

def generators_dict_to_json(dict: dict[str, Generator]) -> str:
    return {key: value.to_dict() for key, value in dict.items()}

def generators_list_to_json(list: list[Generator]) -> str:
    return [generator.to_dict() for generator in list]

# TODO: Move this to a separate recommendation class
def recommended_generator_from(
    string: str, 
    generators: list[Generator]
    ) -> Generator:
    # Naive attempt to break up name into words
    replaced_string = string.lower().replace(" ", "_")
    possible_tags = re.split(r'[_-]', replaced_string)

    # Rank generators by number of tag matches
    highest_score = 0
    recommended_generators = []
    for generator in generators:
        lowered_tags = [tag.lower() for tag in generator.tags]
        score = len([possible_tags.index(i) for i in lowered_tags if i in possible_tags])
        if score > highest_score:
            highest_score = score
            recommended_generators.append({"generator": generator, "score": score})
        
    if len(recommended_generators) == 0:
        return None

    # Else recommend the highest scoring generator
    def sort_by_score(generator_dict):
        return generator_dict["score"]
    
    return sorted(recommended_generators, key=sort_by_score, reverse=True)[0]["generator"]