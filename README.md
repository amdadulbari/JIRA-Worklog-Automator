# JIRA Work Log Automation

This Python script automates the process of posting work logs to JIRA tickets. It reads a CSV file containing ticket IDs, log details, and other relevant information, and then posts logs to JIRA based on this data.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library
- `python-dateutil` library

You can install the required libraries using pip:
```bash
pip install requests python-dotenv python-dateutil
```
## Setup
### Environment Variables:

Create a .env file in the same directory as the script.
Add your JIRA credentials and URL to the .env file like this:
```
JIRA_USERNAME=your_jira_username
JIRA_PASSWORD=your_jira_password
JIRA_URL=https://your_jira_domain.atlassian.net
```
### CSV File:

Prepare a CSV file named tickets.csv with the following columns:

**ticket-id**: JIRA ticket ID.  
**log_detail_file_name**: Path to a file containing log messages.  
**hour-per-day**: Hours to log per day.  
**start-date**: Start date for the logs
(format YYYY-MM-DD).  
**end-date**: End date for the logs (format YYYY-MM-DD).

**Log Details File**:

Create a log details file for each ticket as specified in the CSV. This file should contain different log messages, one per line.

### Offday Configuration (optional):

Optionally, create an offday.conf file listing dates (YYYY-MM-DD format) when no logs should be posted.

## Usage
Run the script with the following command:

```
python main.py 
```