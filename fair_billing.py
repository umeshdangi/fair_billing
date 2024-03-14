import sys
from collections import defaultdict
from datetime import datetime

def process_log_file(file_path):
    """
    Process the log file and calculate total session time for each user.

    Args:
        file_path (str): Path to the log file.

    Returns:
        list: A list of tuples containing username, session count, and total session time.
    """
    user_sessions = defaultdict(list)
    earliest_start = None
    latest_end = None

    try:
        with open(file_path, 'r') as file:
            for line in file:
                components = line.strip().split()
                if len(components) != 3:
                    continue

                timestamp_str, username, action = components

                # Try to convert timestamp to datetime, handle invalid timestamp
                try:
                    timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
                except ValueError:
                    print(f"Invalid timestamp '{timestamp_str}' on line: {line.strip()}. Skipping...")
                    continue

                if action == "Start" and (earliest_start is None or timestamp < earliest_start):
                    earliest_start = timestamp
                elif action == "End" and (latest_end is None or timestamp > latest_end):
                    latest_end = timestamp

                user_sessions[username].append((timestamp, action))

    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    results = []
    for username, sessions in user_sessions.items():
        total_time = 0
        session_count = 0
        for i in range(0, len(sessions), 2):
            if i + 1 < len(sessions):
                start_time, end_time = sessions[i][0], sessions[i + 1][0]
                total_time += (end_time - start_time).seconds
                session_count += 1
        if len(sessions) % 2 != 0:
            last_session_start = sessions[-1][0]
            total_time += (latest_end - last_session_start).seconds

        results.append((username, session_count, total_time))

    return results


def print_report(report):
    """
    Print the report with formatted output.

    Args:
        report (list): List of tuples containing username, session count, and total session time.
    """
    print("User      Sessions  Total Time (seconds)")
    print("---------------------------------------")
    for username, session_count, total_time in report:
        print(f"{username:<10} {session_count:<9} {total_time:<20}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fair_billing.py <path_to_log_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    report = process_log_file(file_path)

    print_report(report)
