import argparse
import csv
import requests
import re
from collections import defaultdict


def download_web_log(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading web log: {e}")
        return None


def process_web_log(log_data):
    image_hits = 0
    total_hits = 0
    browser_counts = defaultdict(int)
    hour_counts = defaultdict(int)

    # Use csv.reader to process the log data
    reader = csv.reader(log_data.splitlines())

    for row in reader:
        if len(row) < 5:
            continue  # Skip incomplete rows

        path, timestamp, user_agent, status, size = row

        # Part III: Search for Image Hits using regular expressions
        if re.search(r'\.(jpg|gif|png)$', path, re.IGNORECASE):
            image_hits += 1

        # Part IV: Finding Most Popular Browser
        browser_match = re.search(r'Firefox|Chrome|Internet Explorer|Safari', user_agent)
        if browser_match:
            browser = browser_match.group()
            browser_counts[browser] += 1

        # Extract the hour from timestamp for Part VI
        hour = int(timestamp.split()[1].split(':')[0])
        hour_counts[hour] += 1

        total_hits += 1

    return image_hits, total_hits, browser_counts, hour_counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Log Processing")
    parser.add_argument("--url", type=str, help="URL of the web log file")
    args = parser.parse_args()

    if args.url:
        log_data = download_web_log(args.url)
        if log_data:
            image_hits, total_hits, browser_counts, hour_counts = process_web_log(log_data)

            # Part III: Print percentage of image requests
            image_percentage = (image_hits / total_hits) * 100
            print(f"Image requests account for {image_percentage:.1f}% of all requests")

            # Part IV: Print the most popular browser
            most_popular_browser = max(browser_counts, key=browser_counts.get)
            print(f"The most popular browser is {most_popular_browser}")

            # Part VI: Print hours with hit counts (Extra Credit)
            for hour, count in sorted(hour_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"Hour {hour:02d} has {count} hits")
    else:
        print("Please provide the URL of the web log file using the --url argument.")
