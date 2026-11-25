from googleapiclient.errors import HttpError

from google_connection import get_sheets_service


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


if __name__ == "__main__":
    try:
        result = create_spreadsheet("First_geeks_sheet")
        print("Spreadsheet created!")
        print(result["url"])
    except HttpError as error:
        print(f"Google API request failed: {error}")