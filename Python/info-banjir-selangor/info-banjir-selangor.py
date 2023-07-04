import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# States Code in Malaysia
states = ['PLS','KDH','PNG','PRK','SEL','WLH','NSN','MLK','JHR','PHG','TRG','KEL','SRK','SAB','WLP']

# URL of the Public Info Banjir for Selangor water level data
url = f"http://publicinfobanjir.water.gov.my/aras-air/data-paras-air/aras-air-data/?state={states[13]}&district=ALL&station=ALL"

try:
    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table containing the water level data
    table = soup.find("table")

    # Find all rows in the table
    rows = table.find_all("tr", class_="item")

    # Check if the water level data is available
    if len(rows) == 0:
        print("Data is not available!")
    else:
        data = {
            'Station Index': [],
            'Station Name': [],
            'District Name': [],
            'Update Time': [],
            'Water Level': [],
            'Danger Level': []
        }

        # Declare how many station has reached danger level
        danger_level_count = 0

        # Iterate over each row (skip the header row)
        for row in rows[1:]:

            # Extract the columns of the current row
            columns = row.find_all("td")

            # Extract the text values from each column
            column_values = [column.text.strip() for column in columns]
            
            # Extract the Index, Station Name, District Name, Update Time, Water Level and Danger Level columns
            station_index = column_values[0]
            data['Station Index'].append(station_index)

            station_name = column_values[2]
            data['Station Name'].append(station_name)

            district_name = column_values[3]
            data['District Name'].append(district_name)

            update_time = column_values[6]
            data['Update Time'].append(update_time)

            water_level = float(column_values[7])
            data['Water Level'].append(water_level)

            danger_level = float(column_values[11])
            data['Danger Level'].append(danger_level)

            # Check if the water level has reached the danger level
            if water_level >= danger_level:
                danger_level_count = danger_level_count + 1

                print("Station ID:", station_name)
                print("District Name:", district_name)
                print("Water Level:", water_level, "m")
                print("Danger Level:", danger_level, "m")
                print("--------------------------")

        # Check how
        if danger_level_count == 0:
            print("Good news, no stations have reach to dangerous levels.")
        else:
            print(f"Alert, {danger_level_count} station have reach dangerous level!" )

        # Specify the file path and name for the CSV file
        csv_file_path = "info-banjir-selangor.csv"

        # Check if the CSV file exists
        if os.path.exists(csv_file_path):
            # Delete the existing CSV file
            os.remove(csv_file_path)
            print("Existing CSV file deleted.")
        
        # Save data into CSV file
        df = pd.DataFrame(data)
        df.to_csv(csv_file_path, index=False)

        print("Water level data saved to", csv_file_path)

except requests.exceptions.RequestException as e:
    print("Error occurred while sending the request:", str(e))

except Exception as ex:
    print("Error occurred while parsing the HTML content:", str(ex))
