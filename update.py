import requests
from bs4 import BeautifulSoup
import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        if os.path.exists("cookies.json"):
            with open("cookies.json", "r") as file:
                cookies = json.load(file)
                cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_rows = []
                for player in values:
                    cfn = player[0]
                    url = f"https://www.streetfighter.com/6/buckler/profile/{cfn}"
                    response = requests.get(url, headers=headers, cookies=cookies_dict)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        # Find the script tag with the JSON data
                        script_tag = soup.find("script", id="__NEXT_DATA__")
                        if script_tag:
                            next_data = json.loads(script_tag.text)  # Parse the JSON
                            new_rows.append(
                                [
                                    timestamp,
                                    cfn,
                                    next_data["props"]["pageProps"][
                                        "fighter_banner_info"
                                    ]["favorite_character_alpha"],
                                    next_data["props"]["pageProps"][
                                        "fighter_banner_info"
                                    ]["favorite_character_league_info"][
                                        "league_rank_info"
                                    ][
                                        "league_rank_name"
                                    ],
                                    next_data["props"]["pageProps"][
                                        "fighter_banner_info"
                                    ]["favorite_character_league_info"]["league_point"],
                                    next_data["props"]["pageProps"][
                                        "fighter_banner_info"
                                    ]["favorite_character_league_info"][
                                        "master_rating"
                                    ],
                                ]
                            )
                        else:
                            print("Unable to find the '__NEXT_DATA__' script tag.")
                    else:
                        print(
                            f"Request failed with status code {response.status_code}."
                        )
                # Append rows to the sheet
                response = (
                    service.spreadsheets()
                    .values()
                    .append(
                        spreadsheetId=SPREADSHEET_ID,
                        range="RatingHistory",
                        valueInputOption="USER_ENTERED",  # "RAW" or "USER_ENTERED"
                        insertDataOption="INSERT_ROWS",  # Options: "INSERT_ROWS" or "OVERWRITE"
                        body={"values": new_rows},
                    )
                    .execute()
                )

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
