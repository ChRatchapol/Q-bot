# GGSheet main file
# | IMPORT SECTION
import os
import sys
from typing import Dict, List, Union
from googleapiclient.discovery import build
from google.oauth2 import service_account

# | GLOBAL VARAIBLES AND GLOBAL EXECUTIONS

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "ggsheet\\keys.json"
SERVICE_ACCOUNT_FILE = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], SERVICE_ACCOUNT_FILE)

CREDS = None
CREDS = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

SPREADSHEET_ID = ""

# | FUNCTIONS

def sheet_read(range: str) -> List[List[str]]:
    """
    read data to GGSheet (SPREADSHEET_ID) at range provide

    Parameters
    ----------
    range : str
        range of data on GGSheet that will be read

    Returns
    -------
    List[List[str]]
        result of reading
    """

    global CREDS
    global SPREADSHEET_ID

    service = build("sheets", "v4", credentials=CREDS)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=range)
        .execute()
    )

    values = result.get("values", [])
    return values

def sheet_write(range: str, data: List[List[str]], input_mode: str = "USER_ENTERED") -> Dict[str, Union[str, int]]:
    """
    write data to GGSheet (SPREADSHEET_ID) at range and input_mode provide

    Parameters
    ----------
    range : str
        range of GGSheet that data will write to
    data : List[List[str]]
        data that will be written to GGSheet
    input_mode : str, optional
        input mode for more intel visit: https://developers.google.com/sheets/api/reference/rest, by default "USER_ENTERED"

    Returns
    -------
    Dict[str, Union[str, int]]
        result of write request
    """
    global CREDS
    global SPREADSHEET_ID

    service = build("sheets", "v4", credentials=CREDS)

    # Call the Sheets API
    sheet = service.spreadsheets()

    request = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range,
        valueInputOption=input_mode,
        body={"values": data},
    ).execute()

    return request

def sheet_template_gen() -> List[List[str]]:
    """
    create template for writing to GGSheet (For Inno. queue only)

    Returns
    -------
    List[List[str]]
        template list
    """

    res = [["Group", "Topic"]]
    for _ in range(17):
        res.append(["", ""])
    
    return res

def sheet_init(id: str) -> None:
    """
    Set SPREADSHEET_ID to id to identify which GGSheet will be read and write.

    Parameters
    ----------
    id : str
        id of GGSheet
    """

    global SPREADSHEET_ID
    SPREADSHEET_ID = id

# | MAIN

if __name__ == "__main__":
    print(sheet_read("Queue!A1:B18"))
    print(sheet_write("Queue!C1", sheet_template_gen()))