{
    "required": {
        "required": false,
        "default": false,
        "type": "bool",
        "comment": "Whether or not this Option is required"
    },
    "default": {
        "required": false,
        "type": "any",
        "comment": "Default Value if not required and not set"
    },
    "type": {
        "required": true,
        "default": "any",
        "type": "str",
        "comment": "Type the Value must be.",
        "values": [ "any", "str", "int", "list", "dict", "float", "bool", "file", "dir", "file:exist", "dir:exist", "path", "path:exist" ]
    },
    "comment": {
        "required": false,
        "type": "str",
        "comment": "Informational Comment about this Option and Value"
    },
    "example": {
        "required": false,
        "type": "any",
        "comment": "Example Data for this Option and Value"
    },
    "values": {
        "required": false,
        "type": "list",
        "comment": "List of Acceptable Values",
        "example": "[ \"value1\", \"value2\" ]"
    },
    "format": {
        "required": false,
        "type": "str",
        "comment": "Regex Acceptable Value",
        "example": "^\\d+\\w+$"
    },
    "spec_chain": {
        "required": false,
        "type": "str",
        "comment": "Add a specker spec which maps into this spec",
        "example": "mysecond_spec_name"
    }
}