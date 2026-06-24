"""
Python Script: log_processor.py (Starter Code)
Instructions:
Complete the functions below to parse the 'logs.txt' file, categorize requests,
filter slow requests, and display unique client IP statistics using Python collections.
"""

def parse_log_line(line):
    """
    Parses a single log line in Common Log Format.
    Example line:
    192.168.1.10 - - [10/Jun/2026:10:15:30 +0000] "GET /api/v1/users HTTP/1.1" 200 45

    Returns a dictionary of parsed parts:
    {
        "ip": "192.168.1.10",
        "method": "GET",
        "path": "/api/v1/users",
        "status": 200,
        "latency": 45
    }
    """
    # TODO: Split the log line and extract the IP, Method, Path, Status Code, and Latency (last element).
    # Tip: Use line.split() and string slicing. Remember to cast status and latency to integers!

    sub_strings = line.split(' ')

    line_dic = { 
        "ip"        : sub_strings[0], 
        "method"    : sub_strings[5][1:], 
        "path"      : sub_strings[6], 
        "status"    : int(sub_strings[-2]),
        "latency"   : int(sub_strings[-1])
        }
    #print("Final parsed line:", line_dic)
    return line_dic

def analyze_logs(file_path):
    """
    Reads the logs file, parses each line, and aggregates metrics using lists, sets, and dicts.
    """
    all_requests = []
    unique_ips = set()
    status_counts = {}
    slow_requests = []

    # TODO: Open the file and process it line by line
    # For each line:
    # 1. Parse it using parse_log_line()
    # 2. Add the parsed request to all_requests (list)
    # 3. Add the client IP to unique_ips (set)
    # 4. Increment the status code counts in status_counts (dict)
    # 5. If latency is greater than 100ms, add to slow_requests (list)

    # Open file, then parse each line!
    with open(file_path, "r") as file:
        for line in file:
            # 1. Parse it using parse_log_line()
            line_dic = parse_log_line(line)
            # 2. Add the parsed request to all_requests (list)
            all_requests.append(line_dic)
            # 3. Add the client IP to unique_ips (set)
            unique_ips.add(line_dic["ip"])
            # 4. Increment the status code counts in status_counts (dict)
            status = line_dic["status"]
            status_count = status_counts.get(status, 0) + 1
            status_counts.update({ status : status_count })
            # 5. If latency is greater than 100ms, add to slow_requests (list)
            if line_dic["latency"] > 100:
                slow_requests.append(line_dic)

    print("=========================================<br>")
    print("SRE LOG ANALYSIS SUMMARY REPORT<br>")
    print("=========================================<br>")
    print(f"Total Requests Processed: {len(all_requests)}<br>")
    print(f"Unique Client IPs: {len(unique_ips)}<br>")
    print(f"HTTP Status Code Breakdown: {status_counts}<br>")
    print(f"Slow Requests (>100ms) Count: {len(slow_requests)}<br>")
    print("-----------------------------------------<br>")
    print("Detailed List of Unique Client IPs:<br>")
    # TODO: Print sorted list of unique client IPs
    ips = [*unique_ips]
    ips.sort()
    for ip in ips:
        print(f"{ip}\n")
    
    print("\n<br>Detailed List of Slow Requests:<br>")
    # TODO: Print the path and latency of each slow request
    for slow in slow_requests:
        print(f"{slow['path'], slow['latency']}<br>")

if __name__ == "__main__":
    import os
    # Find logs.txt relative to this script
    logs_file = os.path.join(os.path.dirname(__file__), "logs.txt")
    if os.path.exists(logs_file):
        analyze_logs(logs_file)
    else:
        print(f"Error: {logs_file} not found. Please run this script in its local folder.")

