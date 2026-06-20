from datetime import datetime
import os


def save_report(stats, suspicious, activities):
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/report_{timestamp}.txt"

    with open(filename, "w") as file:

        file.write("===== LOGSENTINEL SECURITY REPORT =====\n\n")

        file.write(f"Generated On: {datetime.now()}\n\n")

        file.write(f"Total Logs: {stats['total']}\n")
        file.write(f"INFO: {stats['info']}\n")
        file.write(f"WARNING: {stats['warning']}\n")
        file.write(f"ERROR: {stats['error']}\n\n")

        file.write("===== SUSPICIOUS IP ACTIVITY =====\n")

        if suspicious:

            for ip, attempts in suspicious.items():

                risk = "HIGH" if attempts >= 5 else "MEDIUM"

                file.write(
                    f"[{risk}] {ip} -> {attempts} failed attempts\n"
                )

        else:
            file.write("No suspicious IP activity detected.\n")

        file.write("\n\n===== SUSPICIOUS LOG ENTRIES =====\n")

        if activities:

            for activity in activities:
                file.write(activity + "\n")

        else:
            file.write("No suspicious log entries found.\n")

    return filename