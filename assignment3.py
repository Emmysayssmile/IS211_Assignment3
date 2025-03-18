# Import necessary modules
import argparse
import requests
import csv
import re
from collections import defaultdict
from datetime import datetime

# **PART 1: File Download**
def download_file(url):
    """Download the file from a given URL"""
    response = requests.get(url)
    if response.status_code == 200:
        print("File downloaded successfully!")  # Debugging statement
        return response.text.splitlines()
    else:
        print(f"Error: Unable to fetch file. HTTP Status: {response.status_code}")
        return None

# **PART 2: Parse Date Function**
def parse_date(date_string):
    """Try multiple date formats for parsing"""
    date_formats = ["%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]  # Added new format

    for date_format in date_formats:
        try:
            return datetime.strptime(date_string, date_format)
        except ValueError:
            continue

    print(f"Skipping row due to unrecognized date format: {date_string}")
    return None  # Return None if no format matches

# **PART 3: Process CSV Data**
def process_csv(file_content):
    """Read and process the CSV file"""
    data = []
    reader = csv.reader(file_content)

    for row in reader:
        if len(row) < 5:
            continue  # Skip rows with missing values
        
        path, date_time, browser, status, size = row
        
        parsed_datetime = parse_date(date_time)
        if not parsed_datetime:
            continue  # Skip invalid date rows

        try:
            status = int(status)
            size = int(size)
        except ValueError:
            print(f"Skipping row due to invalid status/size: {row}")
            continue

        data.append({
            "path": path,
            "datetime": parsed_datetime,
            "browser": browser,
            "status": status,
            "size": size
        })

    return data

# **PART 4: Find Image Requests**
def find_image_requests(data):
    """Finds image requests and calculates percentage"""
    image_pattern = re.compile(r".*\.(jpg|png|gif)$", re.IGNORECASE)
    total_requests = len(data)
    image_requests = sum(1 for entry in data if image_pattern.match(entry["path"]))

    if total_requests == 0:
        print("No requests found.")
        return

    percentage = (image_requests / total_requests) * 100
    print(f"Image requests account for {percentage:.2f}% of all requests")

# **PART 5: Find Most Popular Browser**
def find_popular_browser(data):
    """Finds the most commonly used browser"""
    browser_counts = defaultdict(int)

    for entry in data:
        browser = entry["browser"]
        if "Firefox" in browser:
            browser_counts["Firefox"] += 1
        elif "Chrome" in browser:
            browser_counts["Chrome"] += 1
        elif "Safari" in browser:
            browser_counts["Safari"] += 1
        elif "MSIE" in browser or "Trident" in browser:
            browser_counts["Internet Explorer"] += 1

    if browser_counts:
        most_popular = max(browser_counts, key=browser_counts.get)
        print(f"Most popular browser: {most_popular}")

# **PART 6: Find Busiest Hours (Extra Credit)**
def find_busiest_hours(data):
    """Finds the busiest hours of the day based on request count"""
    hourly_counts = defaultdict(int)

    for entry in data:
        hour = entry["datetime"].hour
        hourly_counts[hour] += 1

    sorted_hours = sorted(hourly_counts.items(), key=lambda x: x[1], reverse=True)

    for hour, count in sorted_hours:
        print(f"Hour {hour:02d} has {count} hits")

# **PART 7: Main Function**
def main(url):
    """Main function to handle the program execution"""
    file_content = download_file(url)
    if not file_content:
        return  # Stop execution if download fails
    
    data = process_csv(file_content)  # Convert CSV into structured data
    
    find_image_requests(data)  # Analyze image request percentage
    find_popular_browser(data)  # Find most used browser
    find_busiest_hours(data)  # Find busiest hours (Extra Credit)

# **PART 8: Argument Parser**
if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
