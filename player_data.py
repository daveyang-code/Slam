import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

players = [
    3499094771,
    1829436149,
    2054442633,
    3650683730,
    2241295718,
    2760390926,
    1968071252,
    2092554397,
    1914145542,
    3870735880,
    1537254233,
    2901758024,
    3509523174,
    2772954449,
    3280798806,
    3302923668,
    1634094086,
    1520542298,
    1087725121,
    1336392604,
    1295222038,
    1289472869,
    1569666085,
    2181151249,
]


def main():

    try:

        if os.path.exists("cookies.json"):
            with open("cookies.json", "r") as file:
                cookies = json.load(file)
                cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                timestamp = datetime.now().strftime("%Y-%m-%d")
                for player in players:
                    cfn = str(player)
                    url = f"https://www.streetfighter.com/6/buckler/profile/{cfn}"
                    response = requests.get(url, headers=headers, cookies=cookies_dict)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        script_tag = soup.find("script", id="__NEXT_DATA__")
                        if script_tag:
                            next_data = json.loads(script_tag.text)  # Parse the JSON
                            if not os.path.exists("report"):
                                os.makedirs("report")
                            if not os.path.exists(f"report/{timestamp}"):
                                os.makedirs(f"report/{timestamp}")
                            with open(f"report/{timestamp}/{cfn}.json", "w") as file:    
                                json.dump(next_data, file, indent=4)
                        else:
                            print("Unable to find the '__NEXT_DATA__' script tag.")
                    else:
                        print(
                            f"Request failed with status code {response.status_code}."
                        )

    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
