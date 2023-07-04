import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# States Code in Malaysia
states = ['St001','St002','St003','St004','St005','St006','St007','St008','St009','St010','St011','St012','St013','St501','St501']

# URL of the Public Info Banjir for Selangor water level data
url = f"https://www.met.gov.my/forecast/weather/state/{states[8]}/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

location = soup.find("p").find("strong").text.strip()
location = location.split(":")[-1].strip()
print("Location:", location)

# Find the table containing the water level data
table = soup.find("table")

# Find all rows in the table
rows = table.find_all("tr")

# Check if the water level data is available
if len(rows) == 0:
    print("Data is not available!")
else:
    data = {
        'Tarikh': [],
        'Cuaca': [],
        'Ramalan': []
    }

# Iterate over each row (skip the header row)
for row in rows[1:]:
    # Extract the columns of the current row
    columns = row.find_all("td")
    # print(columns)

    # Extract the text values from each column
    column_values = [column.text.strip().replace("\n", " ") for column in columns]
    # print(column_values)
    
    # Extract the Index, Station Name, District Name, Update Time, Water Level and Danger Level columns
    date = column_values[0]
    date = " ".join(date.split())
    data['Tarikh'].append(date)

    weather = column_values[1]
    data['Cuaca'].append(weather)

    forecast = column_values[2]
    data['Ramalan'].append(forecast)

print("Tarikh:", date)
print("Cuaca:", weather)
print("Ramalan:", forecast)
print("--------------------------")