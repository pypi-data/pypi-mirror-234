
# Attempts to import by filename when in a package did not work - so importing all the generator files explicitly here. This is not ideal but works for now.

from graph_data_generator.models.generator import generators_from_json

# Regular generators
from graph_data_generator.generators import bool, catch_phrase, city, company_name, country, date, email, exhaustive_random, first_name, float, float_from_list, float_range, int, int_from_list, int_range, last_name, lorem_paragraphs, loremtext_sentence, loremtext_words, md5, pure_random, string_from_csv, string_from_list, string_literal, technical_phrase, uri, uuid

# Functional genertators
from graph_data_generator.generators import add_floats, add_ints, add_strings

# key name and generator name somewhat duplicitous currently. Keys will remain unchanged, but name add separately to support multi-lingu support (someday) 
generators_json = {
    "README":{
        "content": "This is the default list of all generators used by the app. If you add new generators they will be added to this file. The default_generators.json file contains a copy of this from the repo maintainer(s)"
    },
    "add_ints": {
        "args": [
            {
                "default": "",
                "label": "Generator Specifications",
                "type": "String"
            }
        ],
        "code": add_ints,
        "description": "Combines output from a list of other generators into a single integer value",
        "name": "Add Integers",
        "tags": [
            "function",
            "int",
            "integer",
            "integers"
            "generators",
            "sum",
            "combine"
        ],
        "type": "Function"
    },
    "add_floats": {
        "args": [
            {
                "default": "",
                "label": "Generator Specifications",
                "type": "String"
            }
        ],
        "code": add_floats,
        "description": "Combines output from a list of other generators into a single float value",
        "name": "Add Floats",
        "tags": [
            "function",
            "float",
            "numbers",
            "generators",
            "sum",
            "combine"
        ],
        "type": "Function"
    },
    "add_strings": {
        "args": [
            {
                "default": "",
                "label": "Generator Specifications",
                "type": "String"
            }
        ],
        "code": add_strings,
        "description": "Combines output from a list of other generators into a single string",
        "name": "Add Strings",
        "tags": [
            "function",
            "string",
            "generators",
            "aggregate",
            "combine"
        ],
        "type": "Function"
    },
    "bool": {
        "args": [
            {
                "default": 50,
                "label": "Percent chance of true (out of 100)",
                "type": "Integer"
            }
        ],
        "code": bool,
        "description": "Bool generator using the Faker library.",
        "name": "Bool",
        "tags": [
            "bool",
            "boolean"
        ],
        "type": "Bool"
    },
    "catch_phrase": {
        "args": [],
        "code": catch_phrase,
        "description": "Phrase with first letter capitalized. Faker Library",
        "name": "Catch Phrase",
        "tags": [
            "phrase",
            "phrases",
            "catch",
            "project",
            "description"
        ],
        "type": "String"
    },
    "city": {
        "args": [],
        "code": city,
        "description": "City name generator using the Faker library.",
        "name": "City",
        "tags": [
            "city",
            "name"
        ],
        "type": "String"
    },
    "company_name": {
        "args": [],
        "code": company_name,
        "description": "Company name generator using the Faker library.",
        "name": "Company Name",
        "tags": [
            "company",
            "name"
        ],
        "type": "String"
    },
    "country": {
        "args": [],
        "code": country,
        "description": "Country name generator using the Faker library.",
        "name": "Country",
        "tags": [
            "country",
            "from"
        ],
        "type": "String"
    },
    "date": {
        "args": [
            {
                "default": "1970-01-01",
                "label": "Oldest Date",
                "type": "Datetime"
            },
            {
                "default": "2022-11-24",
                "label": "Newest Date",
                "type": "Datetime"
            }
        ],
        "code": date,
        "description": "Generate a random date between 2 specified dates. Exclusive of days specified.",
        "name": "Date",
        "tags": [
            "date",
            "datetime",
            "created",
            "updated",
            "at"
        ],
        "type": "Datetime"
    },
    "email": {
        "args": [
            {
                "default": "",
                "label": "Optional Domain (ie: company.com)",
                "type": "String"
            }
        ],
        "code": email,
        "description": "Random email with Faker library.",
        "name": "Email",
        "tags": [
            "email"
        ],
        "type": "String"
    },
    "exhaustive_random": {
        "args": [],
        "code": exhaustive_random,
        "description": "Assigns each source node to a random target node, until target node records are exhausted. No duplicates, no orphan to nodes.",
        "name": "Exhaustive Random",
        "tags": [
            "exhaustive"
        ],
        "type": "Assignment"
    },
    "first_name": {
        "args": [],
        "code": first_name,
        "description": "First name generator using the Faker library",
        "name": "First Name",
        "tags": [
            "first",
            "name"
        ],
        "type": "String"
    },
    "float_from_list": {
        "args": [
            {
                "default": "",
                "label": "List of float values (ie: 1.0, 2.2, 3.3)",
                "type": "String"
            }
        ],
        "code": float_from_list,
        "description": "Randomly selected float from a comma-seperated list of options.",
        "name": "Float from list",
        "tags": [
            "float",
            "list"
        ],
        "type": "Float"
    },
    "float": {
        "args": [
            {
                "default": 0.0,
                "label": "Value",
                "type": "Float"
            }
        ],
        "code": float,
        "description": "Literal float value",
        "name": "Float",
        "tags": [
            "float",
            "decimal",
            "number",
            "num",
            "count",
            "cost",
            "price"
        ],
        "type": "Float"
    },
    "float_range": {
        "args": [
            {
                "default": 0.0,
                "label": "Min",
                "type": "Float"
            },
            {
                "default": 1.0,
                "label": "Max",
                "type": "Float"
            },
            {
                "default": 2,
                "label": "Decimal Places",
                "type": "Integer"
            }
        ],
        "code": float_range,
        "description": "Random float between a range. Inclusive.",
        "name": "Float from range",
        "tags": [
            "float",
            "decimal",
            "number",
            "num",
            "count",
            "cost",
            "price"
        ],
        "type": "Float"
    },
    "int_from_list": {
        "args": [
            {
                "default": "",
                "label": "List of integers (ie: 1, 2, 3)",
                "type": "String"
            }
        ],
        "code": int_from_list,
        "description": "Randomly selected int from a comma-seperated list of options. If no list provided, will return 0",
        "name": "Int from list",
        "tags": [
            "int",
            "integer",
            "number",
            "num",
            "count",
            "list",
            "salary",
            "cost"
        ],
        "type": "Integer"
    },
    "int": {
        "args": [
            {
                "default": 1,
                "label": "Value",
                "type": "Integer"
            }
        ],
        "code": int,
        "description": "Constant integer value",
        "name": "Int",
        "tags": [
            "int",
            "integer",
            "num",
            "number",
            "count"
        ],
        "type": "Integer"
    },
    "int_range": {
        "args": [
            {
                "default": 1,
                "label": "Min",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Max",
                "type": "Integer"
            }
        ],
        "code": int_range,
        "description": "Random integer from a min and max value argument. Argument values are inclusive.",
        "name": "Int Range",
        "tags": [
            "int",
            "integer",
            "number",
            "num",
            "count"
        ],
        "type": "Integer"
    },
    "last_name": {
        "args": [],
        "code": last_name,
        "description": "Last name generator using the Faker library.",
        "name": "Last Name",
        "tags": [
            "last",
            "name"
        ],
        "type": "String"
    },
    "lorem_words": {
        "args": [
            {
                "default": 1,
                "label": "Minimum Number",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Maximum Number",
                "type": "Integer"
            }
        ],
        "code": loremtext_words,
        "description": "String generator using the lorem-text package",
        "name": "Words",
        "tags": [
            "words",
            "lorem",
            "text",
            "description"
        ],
        "type": "String"
    },
    "lorem_paragraphs": {
        "args": [
            {
                "default": 1,
                "label": "Minimum Number",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Maximum Number",
                "type": "Integer"
            }
        ],
        "code": lorem_paragraphs,
        "description": "String generator using the lorem-text package",
        "name": "Paragraphs",
        "tags": [
            "string",
            "lorem",
            "ipsum",
            "paragraph",
            "paragraphs"
        ],
        "type": "String"
    },
    "lorem_sentences": {
        "args": [
            {
                "default": 1,
                "label": "Minimum Number",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Maximum Number",
                "type": "Integer"
            }
        ],
        "code": loremtext_sentence,
        "description": "String generator using the lorem-text package",
        "name": "Sentences",
        "tags": [
            "sentence",
            "sentences",
            "lorem",
            "text",
            "description"
        ],
        "type": "String"
    },
    "md5": {
        "args": [
            {
                "default": 33,
                "label": "Limit Character Length",
                "type": "Integer"
            }
        ],
        "code": md5,
        "description": "Random MD5 hash using Faker library. 33 Characters max",
        "name": "MD5",
        "tags": [
            "md5",
            "hash",
            "unique"
        ],
        "type": "String"
    },
    "pure_random": {
        "args": [],
        "code": pure_random,
        "description": "Randomly assigns to a target node. Duplicates and orphan nodes possible.",
        "name": "Pure Random",
        "tags": [
            "random"
        ],
        "type": "Assignment"
    },
    "string": {
        "args": [
            {
                "default": "",
                "label": "List of words (ie: alpha, brave, charlie)",
                "type": "String"
            }
        ],
        "code": string_literal,
        "description": "Explicit string value",
        "name": "String Literal",
        "tags": [
            "string",
            "word",
            "literal"
        ],
        "type": "String"
    },
    "string_from_list": {
        "args": [
            {
                "default": "",
                "label": "List of words (ie: alpha, brave, charlie)",
                "type": "String"
            }
        ],
        "code": string_from_list,
        "description": "Randomly selected string from a comma-seperated list of options.",
        "name": "String from list",
        "tags": [
            "string",
            "list",
            "word",
            "words",
            "status",
            "type"
        ],
        "type": "String"
    },
    "string_from_csv": {
        "args": [
            {
                "default": "",
                "label": "CSV Filepath",
                "type": "String",
                "hint": "mock_generators/datasets/tech_companies.csv",
                "description":""
            },
            {
                "default": "",
                "label": "Header Column Field",
                "type": "String",
                "hint": "Company Name",
                "description":""
            }
        ],
        "code": string_from_csv,
        "description": "Random string row value from a specified csv file. Be certain field contains string values.",
        "name": "String from CSV",
        "tags": [
            "csv",
            " string",
            " random"
        ],
        "type": "String"
    },
    "technical_phrase": {
        "args": [],
        "code": technical_phrase,
        "description": "Technobabble words all lower-cased. Faker Library",
        "name": "Technical BS Phrase",
        "tags": [
            "phrase",
            "phrases",
            "technical",
            "jargon",
            "task",
            "description"
        ],
        "type": "String"
    },
    "uri": {
        "args": [],
        "code": uri,
        "description": "Random URI with Faker library.",
        "name": "URL",
        "tags": [
            "uri",
            "url"
        ],
        "type": "String"
    },
    "uuid": {
        "args": [
            {
                "default": 37,
                "label": "Limit character length",
                "type": "Integer"
            }
        ],
        "code": uuid,
        "description": "Random UUID 4 hash using Faker library. 37 Characters Max.",
        "name": "UUID",
        "tags": [
            "uuid",
            "hash",
            "unique",
            "uid"
        ],
        "type": "String"
    }
}


generators = generators_from_json(generators_json)

# function_generators = generators_from_json(function_generators_json)

# def new_generators_list():
    # return generators_from_json(generators_json)

# def new_function_generators_list():
#     return generators_from_json(function_generators_json)