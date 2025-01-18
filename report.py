import pandas as pd
import json
import os

players = {
    "3509523174": "AESAH",
    "3499094771": "ALLSHAMNOWOW",
    "3280798806": "AMOUR",
    "1829436149": "BOXBOX",
    "1289472869": "BRICKY",
    "3870735880": "CONEY",
    "2092554397": "CURIOUSJOI",
    "3650683730": "ESKAY",
    "2181151249": "FAIRLIGHT EXCALIBUR",
    "1295222038": "FRODAN",
    "2760390926": "HUNTRESS",
    "1914145542": "JAKENBAKELIVE",
    "1537254233": "KARQ",
    "2054442633": "KOEFFICIENT",
    "1087725121": "MACHINA X FLAYON",
    "1520542298": "MOGU",
    "2241295718": "PHIDX",
    "1968071252": "ROBBIE ROTTEN",
    "2901758024": "SCARRA",
    "2772954449": "SEANIC",
    "1336392604": "SHOOMIMI",
    "3302923668": "STANZ",
    "1634094086": "SYKKUNO",
    "1569666085": "VGUMIHO",
}

columns = [
    "Date",
    "Player",
    "CFN",
    "Ranked Matches",
    "Custom Room Matches",
    "Practice",
    "Battle Hub",
    "Casual Matches",
    "Offline Matches",
    "Arcade",
    "World Tour",
    "Extreme",
    "Total Playtime",
    "rank_match_play_count",
    "custom_room_match_play_count",
    "battle_hub_match_play_count",
    "casual_match_play_count",
    "Matches Played",
    "corner_time",
    "cornered_time",
    "drive_parry",
    "just_parry",
    "drive_reversal",
    "drive_impact",
    "drive_impact_to_drive_impact",
    "received_drive_impact",
    "received_drive_impact_to_drive_impact",
    "punish_counter",
    "received_punish_counter",
    "stun",
    "received_stun",
    "throw_count",
    "throw_tech",
    "received_throw_count",
    "throw_drive_parry",
    "received_throw_drive_parry",
    "gauge_rate_drive_arts",
    "gauge_rate_drive_guard",
    "gauge_rate_drive_impact",
    "gauge_rate_drive_other",
    "gauge_rate_drive_reversal",
    "gauge_rate_drive_rush_from_cancel",
    "gauge_rate_drive_rush_from_parry",
    "gauge_rate_sa_lv1",
    "gauge_rate_sa_lv2",
    "gauge_rate_sa_lv3",
    "gauge_rate_ca",
]

# Initialize a list to collect rows
rows = []

# Iterate through each folder in the report directory
for folder in os.listdir("report"):
    folder_path = os.path.join("report", folder)
    if os.path.isdir(folder_path):  # Ensure it's a folder
        # Iterate through each file in the folder
        for file in os.listdir(folder_path):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                file_path = os.path.join(folder_path, file)
                try:
                    # Load the JSON file
                    with open(file_path, "r") as f:
                        data = json.load(f)

                    # Extract and process data
                    cfn = file.split(".")[0]
                    row = {"Date": folder, "Player": players[cfn], "CFN": cfn}
                    playtime = 0
                    for item in data["props"]["pageProps"]["play"]["base_info"][
                        "content_play_time_list"
                    ]:
                        if item["content_type_name"] in columns:
                            row[item["content_type_name"]] = item["play_time"]
                            playtime += item["play_time"]
                    row["Total Playtime"] = playtime

                    matches = 0
                    cfn = file.split(".")[0]
                    row = {"Date": folder, "Player": players[cfn], "CFN": cfn}
                    playtime = 0
                    for item in data["props"]["pageProps"]["play"]["base_info"][
                        "content_play_time_list"
                    ]:
                        if item["content_type_name"] in columns:
                            row[item["content_type_name"]] = item["play_time"]
                            playtime += item["play_time"]
                    row["Total Playtime"] = playtime

                    matches = 0
                    battle_stats = data["props"]["pageProps"]["play"]["battle_stats"]
                    for stat_key, stat_value in battle_stats.items():
                        if stat_key in columns:
                            row[stat_key] = stat_value
                            if stat_key in [
                                "rank_match_play_count",
                                "custom_room_match_play_count",
                                "battle_hub_match_play_count",
                                "casual_match_play_count",
                            ]:
                                matches += stat_value
                    row["Matches Played"] = matches

                    rows.append(row)  # Add row to list

                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error processing file {file_path}: {e}")

# Convert the collected rows into a DataFrame
df = pd.DataFrame(rows).reindex(columns=columns)
df = pd.DataFrame(rows).reindex(columns=columns)

# Save the DataFrame to a CSV file
df.to_csv("report.csv", index=False)
