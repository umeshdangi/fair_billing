Fair Billing Program

This program takes a log file as input and calculates the total session time for each user,
considering the start and end times provided in the log.

Usage:
python fair_billing.py <path_to_log_file>

Example:
python fair_billing.py log_file.txt

The log file should follow the format:
HH:MM:SS USERNAME ACTION

Where:
- HH:MM:SS is the timestamp
- USERNAME is the alphanumeric string representing the user
- ACTION can be "Start" or "End" indicating the start or end of a session

The program will print the report showing each user's name, session count, and total session time in seconds.
