import re

from google_connection import get_sheets_service
from mongo_connect import get_collection, get_database, get_mongo_client


def add(a,b):
    return a+b

def soustraction(a,b):
    return a-b


def _hex_to_rgb(color):
    if not isinstance(color, str) or not color.strip():
        raise ValueError("color must be a non-empty hex string like #FF0000.")

    hex_value = color.strip().lstrip("#")
    if len(hex_value) != 6:
        raise ValueError("color must be a 6-digit hex string like #FF0000.")

    try:
        red = int(hex_value[0:2], 16) / 255
        green = int(hex_value[2:4], 16) / 255
        blue = int(hex_value[4:6], 16) / 255
    except ValueError as error:
        raise ValueError("color must be a valid hex string like #FF0000.") from error

    return {"red": red, "green": green, "blue": blue}


def _column_to_index(column):
    index = 0
    for char in column.upper():
        if not "A" <= char <= "Z":
            raise ValueError(f"Invalid column letter: {column}")
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def _a1_to_grid_range(a1_range, sheet_id):
    cell_range = a1_range
    if "!" in a1_range:
        cell_range = a1_range.split("!", 1)[1]
    cell_range = cell_range.replace("$", "").strip()

    match = re.fullmatch(
        r"([A-Za-z]+)(\d+)(?::([A-Za-z]+)(\d+))?",
        cell_range,
    )
    if not match:
        raise ValueError(
            "range must use A1 notation, e.g. 'Data!A1' or 'Data!A1:C3'."
        )

    start_col, start_row, end_col, end_row = match.groups()
    start_row_index = int(start_row) - 1
    start_col_index = _column_to_index(start_col)

    if end_col is None:
        end_row_index = start_row_index + 1
        end_col_index = start_col_index + 1
    else:
        end_row_index = int(end_row)
        end_col_index = _column_to_index(end_col) + 1

    return {
        "sheetId": sheet_id,
        "startRowIndex": start_row_index,
        "endRowIndex": end_row_index,
        "startColumnIndex": start_col_index,
        "endColumnIndex": end_col_index,
    }


def _sheet_id_from_range(service, spreadsheet_id, a1_range):
    sheet_title = "Data"
    if "!" in a1_range:
        sheet_title = a1_range.split("!", 1)[0].strip().strip("'")

    spreadsheet = (
        service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id, fields="sheets.properties")
        .execute(num_retries=0)
    )

    for sheet in spreadsheet.get("sheets", []):
        properties = sheet.get("properties", {})
        if properties.get("title") == sheet_title:
            return properties["sheetId"], sheet_title

    raise ValueError(f"Sheet '{sheet_title}' was not found in the spreadsheet.")



def create_spreadsheet(title):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("The spreadsheet needs a non-empty title.")

    service = get_sheets_service()
    spreadsheet = service.spreadsheets().create(
        body={
            "properties": {"title": title.strip()},
            "sheets": [{"properties": {"title": "Data"}}],
        },
        fields="spreadsheetId,spreadsheetUrl",
    ).execute(num_retries=0)

    return {
        "spreadsheet_id": spreadsheet["spreadsheetId"],
        "url": spreadsheet["spreadsheetUrl"],
    }


def write_to_spreadsheet(spreadsheet_id, data):
    if not isinstance(spreadsheet_id, str) or not spreadsheet_id.strip():
        raise ValueError("spreadsheet_id must be a non-empty string.")
    if not isinstance(data, list) or not data:
        raise ValueError("data must be a non-empty list of rows.")
    if not all(isinstance(row, list) for row in data):
        raise ValueError("Each item in data must be a list of cell values.")

    service = get_sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id.strip(),
            range="Data!A1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": data},
        )
        .execute(num_retries=0)
    )

    updated_range = result.get("updates", {}).get("updatedRange", "")
    updated_rows = result.get("updates", {}).get("updatedRows", 0)

    return {
        "spreadsheet_id": spreadsheet_id.strip(),
        "updated_range": updated_range,
        "updated_rows": updated_rows,
    }


def edit_spreadsheet(spreadsheet_id, range, value):
    if not isinstance(spreadsheet_id, str) or not spreadsheet_id.strip():
        raise ValueError("spreadsheet_id must be a non-empty string.")
    if not isinstance(range, str) or not range.strip():
        raise ValueError("range must be a non-empty string.")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("value must be a non-empty string.")

    service = get_sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id.strip(),
            range=range.strip(),
            valueInputOption="USER_ENTERED",
            body={"values": [[value]]},
        )
        .execute(num_retries=0)
    )

    return {
        "spreadsheet_id": spreadsheet_id.strip(),
        "updated_range": result.get("updatedRange", ""),
        "updated_cells": result.get("updatedCells", 0),
        "value": value,
    }


def set_background_color(spreadsheet_id, range, color):
    if not isinstance(spreadsheet_id, str) or not spreadsheet_id.strip():
        raise ValueError("spreadsheet_id must be a non-empty string.")
    if not isinstance(range, str) or not range.strip():
        raise ValueError("range must be a non-empty string.")

    rgb = _hex_to_rgb(color)
    service = get_sheets_service()
    spreadsheet_id = spreadsheet_id.strip()
    a1_range = range.strip()

    sheet_id, sheet_title = _sheet_id_from_range(
        service, spreadsheet_id, a1_range
    )
    grid_range = _a1_to_grid_range(a1_range, sheet_id)

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {
                    "repeatCell": {
                        "range": grid_range,
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": rgb,
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor",
                    }
                }
            ]
        },
    ).execute(num_retries=0)

    return {
        "spreadsheet_id": spreadsheet_id,
        "sheet": sheet_title,
        "range": a1_range,
        "color": color.strip(),
    }


def connect_mongodb():
    client = get_mongo_client()
    db = get_database()
    return {
        "status": "connected",
        "database": db.name,
        "collections": db.list_collection_names(),
    }


def add_mongo_data(collection_name, data, db_name=None):
    if not isinstance(collection_name, str) or not collection_name.strip():
        raise ValueError("collection_name must be a non-empty string.")
    if not isinstance(data, dict) or not data:
        raise ValueError("data must be a non-empty object/document.")

    collection = get_collection(collection_name, db_name)
    result = collection.insert_one(data)

    return {
        "database": collection.database.name,
        "collection": collection.name,
        "inserted_id": str(result.inserted_id),
        "data": data,
    }



