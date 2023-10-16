# from graph_data_generator.models.generator import Generator
from graph_data_generator.models.generator_type import GeneratorType

class GeneratorArg():

    @staticmethod
    def from_dict(dict: dict):
        if "type" not in dict.keys():
            raise KeyError("Arg dict missing type key")
        if "label" not in dict.keys():
            raise KeyError("Arg dict missing label key")
        if "default" not in dict.keys():
            default = None
        else: 
            default = dict["default"]
        if "hint" not in dict.keys():
            hint = ""
        else:   
            hint = dict["hint"]
        if "description" not in dict.keys():
            description = ""
        else:
            description = dict["description"]

        return GeneratorArg(
            type = GeneratorType.type_from_string(dict["type"]),
            label = dict["label"],
            default= default,
            hint = hint,
            description=description
        )

    def __init__(
        self, 
        type: GeneratorType, 
        label: str,
        default: any = None,
        hint : str = None,
        description : str = None
    ):
        self.type = type
        self.label = label
        self.default = default
        self.hint = hint
        self.description = description

    def __str__(self):
        return f'GeneratorArg: type: {self.type}, label: {self.label}, default: {self.default}, hint: {self.hint}, description: {self.description}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, GeneratorArg) == False:
            return False
        if self.type != other.type:
            return False
        if self.label != other.label:
            return False 
        if self.default != other.default:
            return False
        if self.hint != other.hint:
            return False
        if self.description != other.description:
            return False
        return True

    def to_dict(self):
        return {
            "type": self.type.to_string(),
            "label": self.label,
            "default": self.default,
            "hint": self.hint,
            "description": self.description
        }

    @staticmethod
    def list_from(list: list[dict]):
        return [GeneratorArg.from_dict(item) for item in list]
