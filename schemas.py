from tools import (
    add,
    soustraction,
    create_spreadsheet,
    write_to_spreadsheet,
    edit_spreadsheet,
    set_background_color,
    connect_mongodb,
    add_mongo_data,
)

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers and return the sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number to add.",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number to add.",
                    },
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "soustraction",
            "description": "Soustraction two numbers and return the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number to soustraction.",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number to soustraction.",
                    },
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_spreadsheet",
            "description": (
                "Create a new Google Spreadsheet with a single sheet named "
                "'Data'. Returns the spreadsheet ID and URL."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Non-empty title for the new spreadsheet.",
                    },
                },
                "required": ["title"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_to_spreadsheet",
            "description": (
                "Append rows of data to the 'Data' sheet of an existing "
                "Google Spreadsheet. Pass data as a list of rows, where each "
                "row is a list of cell values."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "ID of the spreadsheet to write to.",
                    },
                    "data": {
                        "type": "array",
                        "description": (
                            "Rows to append. Example: "
                            '[["Name", "Age"], ["Alice", 30], ["Bob", 25]]'
                        ),
                        "items": {
                            "type": "array",
                            "items": {
                                "type": ["string", "number", "boolean", "null"],
                            },
                        },
                    },
                },
                "required": ["spreadsheet_id", "data"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_spreadsheet",
            "description": (
                "Update a specific cell in an existing Google Spreadsheet. "
                "Use A1 notation for the range, e.g. 'Data!B2'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "ID of the spreadsheet to edit.",
                    },
                    "range": {
                        "type": "string",
                        "description": (
                            "Cell to update in A1 notation, "
                            "e.g. 'Data!A1' or 'Data!B2'."
                        ),
                    },
                    "value": {
                        "type": "string",
                        "description": "New non-empty value to write into the cell.",
                    },
                },
                "required": ["spreadsheet_id", "range", "value"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_background_color",
            "description": (
                "Change the background color of one cell or a range of cells "
                "in a Google Spreadsheet. Color must be a hex string like "
                "#FF0000."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "ID of the spreadsheet to format.",
                    },
                    "range": {
                        "type": "string",
                        "description": (
                            "Cell or range in A1 notation, "
                            "e.g. 'Data!A1' or 'Data!A1:C3'."
                        ),
                    },
                    "color": {
                        "type": "string",
                        "description": (
                            "Background color as hex, e.g. '#FFFF00' for yellow "
                            "or '#00FF00' for green."
                        ),
                    },
                },
                "required": ["spreadsheet_id", "range", "color"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "connect_mongodb",
            "description": (
                "Connect to MongoDB using the configured MONGODB_URI and "
                "return the connection status, database name, and existing "
                "collections."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_mongo_data",
            "description": (
                "Insert one document into a MongoDB collection. "
                "Creates the collection automatically if it does not exist."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "collection_name": {
                        "type": "string",
                        "description": "Name of the collection to insert into.",
                    },
                    "data": {
                        "type": "object",
                        "description": (
                            "Document to insert, e.g. "
                            '{"name": "Alice", "age": 30}.'
                        ),
                    },
                    "db_name": {
                        "type": "string",
                        "description": (
                            "Optional database name. Defaults to MONGODB_DB "
                            "from .env (agent_v1)."
                        ),
                    },
                },
                "required": ["collection_name", "data"],
                "additionalProperties": False,
            },
        },
    },
]

REGISTERY_SCHEMAS = {
    "add": add,
    "soustraction": soustraction,
    "create_spreadsheet": create_spreadsheet,
    "write_to_spreadsheet": write_to_spreadsheet,
    "edit_spreadsheet": edit_spreadsheet,
    "set_background_color": set_background_color,
    "connect_mongodb": connect_mongodb,
    "add_mongo_data": add_mongo_data,
}
