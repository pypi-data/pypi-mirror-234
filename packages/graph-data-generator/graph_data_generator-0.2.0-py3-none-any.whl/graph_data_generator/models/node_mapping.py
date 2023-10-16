from graph_data_generator.models.property_mapping import PropertyMapping
from graph_data_generator.models.generator import Generator
from graph_data_generator.utils.list_utils import clean_list
from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.logger import ModuleLogger


class NodeMapping(BaseMapping):

    @staticmethod
    def empty():
        return NodeMapping(
            nid = "",
            position = {"x": 0, "y": 0},
            caption = "",
            labels = [],
            properties = {},
            count_generator = None,
            count_args = [],
            key_property = None
        )

    def __init__(
        self, 
        nid: str,
        position: dict,   # ie: {x: 0, y: 0}
        caption: str,
        labels: list[str], 
        properties: dict[str, PropertyMapping],
        count_generator: Generator,
        count_args: list[any],
        key_property: PropertyMapping,
        default_count : int = 1
        ):
        self.nid = nid
        self.position = position
        self.caption = caption
        self.labels = labels
        self.properties = properties
        self.count_generator = count_generator
        self.count_args = count_args
        self.default_count = default_count
        self.key_property = key_property # Property to use as unique key for this node
        self.generated_values = None # Will be a list[dict] when generated

    def __str__(self):
        return f"NodeMapping(nid={self.nid}, caption={self.caption}, labels={self.labels}, properties={self.properties}, count_generator={self.count_generator}, count_args={self.count_args}, default_count={self.default_count}, key_property={self.key_property})"

    # def __repr__(self):
    #     return self.__str__()

    # def __eq__(self, other):
    #     if not isinstance(other, NodeMapping):
    #         return False
    #     if self.nid != other.nid:
    #         return False
    #     if self.caption != other.caption:
    #         return False
    #     if self.labels != other.labels:
    #         return False
    #     if self.properties != other.properties:
    #         return False
    #     if self.count_generator != other.count_generator:
    #         return False
    #     if self.count_args != other.count_args:
    #         return False
    #     if self.default_count != other.default_count:
    #         return False
    #     if self.key_property != other.key_property:
    #         return False
    #     return True

    def to_dict(self):
        properties = {}
        for key, property in self.properties.items():
            if isinstance(property, PropertyMapping):
                properties[key] = property.to_dict()
                continue
            properties[key] = property
        return {
            "nid": self.nid,
            "caption": self.caption,
            "position": self.position,
            "labels": self.labels,
            "properties": properties,
            "count_generator": self.count_generator.to_dict() if self.count_generator is not None else None,
            "count_args": clean_list(self.count_args),
            "default_count": self.default_count,
            "key_property" : self.key_property.to_dict() if self.key_property is not None else None
        }

    def filename(self):
        return f"{self.caption.lower()}_{self.nid.lower()}"

    # TODO: Verify unique keys are respected during generation

    def ready_to_generate(self):
        # Validation that node object is ready to generate
        if self.caption is None:
            return False
        if self.count_generator is None and self.default_count is None:
            return False
        if self.key_property is None:
            return False
        return True

    def generate_values(self) -> list[dict]:
        # returns a list of dicts with the generated values
        # Example return:
        # [
        #     {
        #         "_uid": "n1_abc",
        #         "first_name": "John",
        #         "last_name": "Doe"
        #     },
        #     {
        #         "_uid": "n1_xyz",
        #         "first_name": "Jane",
        #         "last_name": "Doe"
        #     }
        # ]
        count = 0
        all_results = []

        if self.count_generator is None:
            ModuleLogger().debug(f'No COUNT generator assigned to node with caption {self.caption}. Using default count {self.default_count}')
            count = self.default_count
        else:
            # Have a count generator to use
            # Will throw an exception if the count generator fails
            count = self.count_generator.generate(self.count_args)

            if isinstance(count, int) == False:
                ModuleLogger().error(f'Count generator did not produce an int value: count read: {count}')
                raise Exception(f"Node mapping count_generator returned a non-integer value: {count}. Check code for generator: {self.count_generator.name}")
        

        for _ in range(count):
            node_result = {}
            for property_id, property in self.properties.items():
                # Pass literal values
                if isinstance(property, PropertyMapping) == False:
                    node_result[property_id] = property
                    ModuleLogger().warning(f'Node mapping properties contains a non-PropertyMapping object: {property}')
                    continue

                # Have PropertyMapping generate a value
                try:
                    values = property.generate_values()
                    if len(values) > 1:
                        ModuleLogger().error(f'Property naemd {property.name} generated more than one value: {values}')
                    value = values[0]
                    if value is None:
                        ModuleLogger().warning(f'Node mapping could not generate value for property: {property}')
                        continue
                    node_result[property.name] = value
                except Exception as e:
                    ModuleLogger().error(f'Node mapping failed to generate values for property: {property}. Error: {e}')
                    raise e
            all_results.append(node_result)
        
        # Store and return all_results
        self.generated_values = all_results

        ModuleLogger().debug(f'Node mapping named {self.caption} finished generating {len(self.generated_values)} values')

        return self.generated_values