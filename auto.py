import json 
import csv
import os
import random
import requests
from datetime import datetime
from dateutil import rrule, parser
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

# Function to post log to JIRA
def post_log(post_date, worklog, ticket_id, time_spent):
    username = os.getenv("JIRA_USERNAME")
    password = os.getenv("JIRA_PASSWORD")
    jira_url = os.getenv("JIRA_URL")
    auth = HTTPBasicAuth(username, password)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    url = f"{jira_url}/rest/api/3/issue/{ticket_id}/worklog"
    print(url)
    payload = {
        "timeSpentSeconds": time_spent,
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": worklog,
                            "type": "text"
                        }
                    ]
                }
            ]
        },
        "started": f"{post_date}T17:00:00.000+0000"  # Adjust time format if needed
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": ")))
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Read CSV and process each row
def process_csv(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            process_ticket(row)

# Process each ticket
def process_ticket(row):
    ticket_id = row['ticket-id']
    log_file = row['log_detail_file_name']
    hours_per_day = int(row['hour-per-day'])
    start_date = parser.parse(row['start-date']).date()
    end_date = parser.parse(row['end-date']).date()
    post_logs_for_ticket(ticket_id, log_file, hours_per_day, start_date, end_date)

# Post logs for a single ticket
def post_logs_for_ticket(ticket_id, log_file, hours_per_day, start_date, end_date):
    with open('offday.conf') as date_conf, open(log_file) as log_conf:
        off_dates = [line.rstrip() for line in date_conf]
        log_messages = [line.rstrip() for line in log_conf]

    date_range = list(rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date))
    for day in date_range:
        today = day.date()
        today_str = str(today)
        week_day = day.strftime("%A")

        if today_str in off_dates or week_day in ['Friday', 'Saturday']:
            continue

        n = random.randint(0, len(log_messages) - 1)
        single_log = log_messages[n]
        time_spent = hours_per_day * 3600

        print(today_str)
        print(single_log)
        post_log(today_str, single_log, ticket_id, time_spent)

# Main execution
if __name__ == "__main__":
    process_csv('tickets.csv')

