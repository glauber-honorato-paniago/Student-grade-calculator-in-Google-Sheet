import os
import time
import datetime
from typing import Callable
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def print_logger(msg: str) -> None:
    """
    Prints a message along with the current timestamp.

    Args:
        msg (str): The message to be printed.
    """
    date_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f'[{date_now}] {msg}')


def execution_time_looger(func: Callable[..., None]) -> Callable[..., None]:
    """
    A decorator function to log the start and end of a function's execution.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        print_logger('Job has started.')
        
        func_result = func(*args, **kwargs)
        
        end = time.time()

        print_logger(f'The job finished, execution time: {round(end - start, 2)} seconds.')
        return func_result
    
    return wrapper
    

class GoogleSheetsApi:
    """
    A class to interact with Google Sheets API.

    Attributes:
        spreadsheet_id (str): The ID of the spreadsheet.
        range_name (str): The range of cells to interact with.
        service (googleapiclient.discovery.Resource): The Google Sheets service instance.
    """
    def __init__(self, spreadsheet_id: str, range_name: str) -> None:
        """
        Initializes GoogleSheetsApi with provided spreadsheet ID and range.

        Args:
            spreadsheet_id (str): The ID of the spreadsheet.
            range_name (str): The range of cells to interact with.
        """
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self._autenticate()
        self.sheet = self.service.spreadsheets()

    def _autenticate(self):
        """
        Authenticates with Google Sheets API.
        This method requires a `credentials.json` file to authenticate
        with Google's OAuth system. This file should be obtained by
        setting up a project in the Google Cloud Platform console, creating
        credentials, and downloading them as a JSON file. This JSON file
        should be stored in the same directory as this script.
        """
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build("sheets", "v4", credentials=creds)
    
    def sheet_get_values(self, spreadsheetId: str=None, range: str=None) -> dict:
        """
        Retrieves values from Google Sheets.

        Args:
            spreadsheetId (str, optional): The ID of the spreadsheet. Defaults to None.
            range (str, optional): The range of cells to retrieve. Defaults to None.

        Returns:
            dict: The retrieved values.
        """
        print_logger("Getting data from google sheets")

        results =  self.sheet.values().get(spreadsheetId=
                                            self.spreadsheet_id if not spreadsheetId else spreadsheetId,
                                        range=
                                            self.range_name if not range else range
                                        ).execute()
        
        print_logger("Successfully obtained data")

        return results
    
    def sheet_batch_update(self, data: dict) -> None:
        """
        Sends updates to Google Sheets.

        Args:
            data (dict): The data to be updated in the spreadsheet.
            range is a parameter specifying the range of cells to be updated in the spreadsheet,
            while "values" contains the actual data to be inserted into those cells.
            example: {"range": "G4", "values": situation_students}
        """
        print_logger("Sending spreadsheet updates to google sheets")

        body = {"valueInputOption": "USER_ENTERED", "data": data}
        result = (
            self.service.spreadsheets()
            .values()
            .batchUpdate(spreadsheetId=self.spreadsheet_id, body=body)
            .execute()
        )
        print_logger("Data sent successfully")
