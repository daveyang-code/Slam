import pandas as pd
import json
import os

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
                    row = {"Date": folder, "Player": file.split(".")[0]}
                    for item in data["props"]["pageProps"]["play"]["base_info"]["content_play_time_list"]:
                        row[item["content_type_name"]] = item["play_time"]
                    
                    battle_stats = data["props"]["pageProps"]["play"]["battle_stats"]
                    for stat_key, stat_value in battle_stats.items():
                        row[stat_key] = stat_value
                    
                    rows.append(row)  # Add row to list
                    
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error processing file {file_path}: {e}")

# Convert the collected rows into a DataFrame
df = pd.DataFrame(rows)

# Save the DataFrame to a CSV file
df.to_csv("report.csv", index=False)