from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


PROJECT_DIR = Path(__file__).resolve().parent
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_sheets_service():
    token_file = PROJECT_DIR / "token.json"
    credentials_file = PROJECT_DIR / "credentials.json"
    credentials = None

    if token_file.exists():
        credentials = Credentials.from_authorized_user_file(
            str(token_file), SCOPES
        )

    if not credentials or not credentials.valid:
        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES
            )
            credentials = flow.run_local_server(port=0)

        token_file.write_text(credentials.to_json(), encoding="utf-8")

    return build("sheets", "v4", credentials=credentials)


if __name__ == "__main__":
    get_sheets_service()
    print("Google authorization succeeded. Sheets client ready!")