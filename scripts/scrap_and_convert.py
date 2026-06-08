import requests
from bs4 import BeautifulSoup
import csv

# Fetch Chart Data
def fetch_chart_data(soup):
    chart_data = []
    script_tag = soup.find("script", string=lambda text: text and "var RCPData" in text)
    if script_tag:
        script_content = script_tag.string
        start_index = script_content.find("data:")
        end_index = script_content.find("]", start_index)
        data_block = script_content[start_index + len("data:") : end_index + 1]
        entries = eval(data_block)  # Parse chart data
        for entry in entries:
            chart_data.append([entry['date'], entry['approve'], entry['disapprove']])
    return chart_data

# Fetch Table Data
def fetch_table_data(soup):
    table_data = []
    table = soup.find("table", {"id": "polling-data-full"})
    if table:
        headers = [header.text.strip() for header in table.find_all("th")]
        table_data.append(headers)
        rows = table.find_all("tr", class_=lambda x: x != "header")
        for row in rows:
            row_data = [cell.text.strip() for cell in row.find_all("td")]
            if row_data:
                table_data.append(row_data)
    return table_data

# Save Data to CSV File
def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

# Main Function
def scrap_and_create_csv():
    URL = "https://www.realclearpolling.com/polls/state-of-the-union/generic-congressional-vote"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Chart Data
        chart_data = fetch_chart_data(soup)
        save_to_csv(chart_data, "chart_data.csv")

        # Table Data
        table_data = fetch_table_data(soup)
        save_to_csv(table_data, "table_data.csv")
    else:
        print(f"Failed to fetch the webpage. Status Code: {response.status_code}")

if __name__ == "__main__":
    scrap_and_create_csv()