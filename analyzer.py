import re
from collections import Counter


def analyze_log(file_path):

    stats = {
        "total": 0,
        "info": 0,
        "warning": 0,
        "error": 0
    }

    failed_ips = []
    suspicious_activities = []

    suspicious_keywords = [
        "Unauthorized access",
        "Failed login attempt",
        "Access denied",
        "Permission denied",
        "Attack detected",
        "Malware",
        "SQL Injection",
        "XSS Attempt"
    ]

    with open(file_path, "r") as file:

        for line in file:

            stats["total"] += 1

            if "INFO" in line:
                stats["info"] += 1

            elif "WARNING" in line:
                stats["warning"] += 1

            elif "ERROR" in line:
                stats["error"] += 1

            # Extract failed login IPs
            if "Failed login attempt" in line:

                ip_match = re.search(
                    r"\d+\.\d+\.\d+\.\d+",
                    line
                )

                if ip_match:
                    failed_ips.append(ip_match.group())

            # Detect suspicious keywords
            for keyword in suspicious_keywords:

                if keyword.lower() in line.lower():
                    suspicious_activities.append(line.strip())

    suspicious_ips = {}

    counts = Counter(failed_ips)

    for ip, attempts in counts.items():

        if attempts >= 3:
            suspicious_ips[ip] = attempts

    return stats, suspicious_ips, suspicious_activities