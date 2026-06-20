import matplotlib.pyplot as plt


def show_charts(stats, suspicious):

    # Pie Chart for log distribution
    labels = ['INFO', 'WARNING', 'ERROR']
    sizes = [
        stats['info'],
        stats['warning'],
        stats['error']
    ]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Log Distribution")
    plt.show()

    # Bar Chart for suspicious IPs
    if suspicious:

        ips = list(suspicious.keys())
        attempts = list(suspicious.values())

        plt.figure(figsize=(8, 5))
        plt.bar(ips, attempts)
        plt.xlabel("IP Address")
        plt.ylabel("Failed Attempts")
        plt.title("Suspicious IP Activity")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.show()