
arrows_json_schema = {
    "nodes" : [
      {
          "id" : {"type" : "string"},
          "position":{
              "x" : {"type" : "number"},
              "y" : {"type" : "number"},
          },
          "caption" : {"type" : "string"},
          "labels": [{"type" : "string"}],
          "properties" : {},
          "style":{}
      },
    ],
    "relationships":[
        {
          "id": {"type" : "string"},
          "fromId": {"type" : "string"},
          "toId": {"type" : "string"},
          "type": {"type" : "string"},
          "properties": {
          },
          "style": {}
        }
    ]
}

arrows_import_schema = {
  "nodes": [
    {
      "id": "n0",
      "position": {
        "x": -668.1260488667057,
        "y": 703.8206888663991
      },
      "caption": "string",
      "labels": [],
      "properties": {
        "property_key": "string",
      },
      "style": {}
    },
    {
      "id": "n3",
      "position": {
        "x": 201.17949326333164,
        "y": -176.50000000000003
      },
      "caption": "Company",
      "labels": [],
      "properties": {
        "property_key": "string",
        "COUNT": "1"
      },
      "style": {}
    },
  ],
  "relationships": [
    {
      "id": "n6",
      "fromId": "n3",
      "toId": "n0",
      "type": "EMPLOYS",
      "properties": {
        "COUNT": "50"
      },
      "style": {}
    }
  ]
}