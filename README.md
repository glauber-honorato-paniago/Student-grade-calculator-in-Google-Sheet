# Google Sheets Manipulation with Python

## Overview

This repository contains Python code for interacting with Google Sheets using the Google Sheets API. The code allows users to retrieve data from a Google Sheets spreadsheet, perform calculations on the data, and update the spreadsheet with the calculated results.

## Key Features

- **Authentication:** Utilizes OAuth 2.0 authentication to securely connect to the Google Sheets API. Users are required to provide a `credentials.json` file obtained through the Google Cloud Platform console.
  
- **Functionality:**
  - **Retrieve Data:** The code provides functionality to retrieve data from a specified range in a Google Sheets spreadsheet.
  - **Calculate Student Situations:** Includes a function to calculate the situation of students based on their data, such as absences and grades.
  - **Update Spreadsheet:** Allows users to update specific ranges in the Google Sheets spreadsheet with calculated results.

## Dependencies

- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Obtain the `credentials.json` file from the Google Cloud Platform console and place it in the root directory of the project.
4. Customize the `SAMPLE_SPREADSHEET_ID` and `SAMPLE_RANGE_NAME` variables in the script to match your Google Sheets spreadsheet ID and range.
5. Run the script to retrieve data from the spreadsheet, calculate student situations, and update the spreadsheet with the results.
