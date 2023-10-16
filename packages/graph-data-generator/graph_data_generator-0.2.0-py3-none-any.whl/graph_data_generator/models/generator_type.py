from enum import Enum, unique

@unique
class GeneratorType(Enum):
    UNKNOWN = 0,
    BOOL = 1,
    INT = 2,
    FLOAT = 3,
    STRING = 4,
    DATETIME = 5,
    ASSIGNMENT = 6,
    RELATIONSHIP = 7,
    FUNCTION = 8

    @staticmethod
    def type_from_string(aType: str):
        type = aType.lower()
        if type == "string":
            return GeneratorType.STRING
        elif type == "int" or type == "integer":
            return GeneratorType.INT
        elif type == "float":
            return GeneratorType.FLOAT
        elif type =="function":
            return GeneratorType.FUNCTION
        elif type == "datetime":
            return GeneratorType.DATETIME
        elif type == "bool":
            return GeneratorType.BOOL
        elif type == "assignment":
            return GeneratorType.ASSIGNMENT
        elif type == "relationship":
            return GeneratorType.RELATIONSHIP
        else:
            raise TypeError("Type not supported")
    
    def to_string(self) -> str:
        """
        Convert a GeneratorType enum value to its corresponding string representation.

        Returns:
            str: The string representation of the GeneratorType enum value.

        Raises:
            TypeError: If the GeneratorType enum value is not supported.
        """
        type_map = {
            GeneratorType.STRING: "String",
            GeneratorType.INT: "Integer",
            GeneratorType.FLOAT: "Float",
            GeneratorType.FUNCTION: "Function",
            GeneratorType.DATETIME: "Datetime",
            GeneratorType.BOOL: "Bool",
            GeneratorType.ASSIGNMENT: "Assignment",
            GeneratorType.RELATIONSHIP: "Relationship"
        }
        result = type_map.get(self, None)
        if result is None:
            raise TypeError(f"{self} type not supported")
        return result
