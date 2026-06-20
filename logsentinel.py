import tkinter as tk
from tkinter import filedialog, messagebox

from analyzer import analyze_log
from charts import show_charts
from report_generator import save_report

selected_file = ""
last_stats = None
last_suspicious = None
last_activities = None


def upload_file():
    global selected_file

    selected_file = filedialog.askopenfilename(
        filetypes=[("Log Files", "*.log *.txt")]
    )

    if selected_file:
        file_label.config(text=selected_file)
        status_bar.config(text="Log file loaded successfully")


def export_report():
    global last_stats, last_suspicious, last_activities

    if not last_stats:
        messagebox.showerror(
            "Error",
            "Please analyze a log file first."
        )
        return

    filename = save_report(
        last_stats,
        last_suspicious,
        last_activities
    )

    messagebox.showinfo(
        "Success",
        f"Report saved successfully!\n\n{filename}"
    )

    status_bar.config(text="Report exported successfully")


def analyze():
    global last_stats, last_suspicious, last_activities

    if not selected_file:
        messagebox.showerror(
            "Error",
            "Please upload a log file."
        )
        return

    stats, suspicious, activities = analyze_log(selected_file)

    last_stats = stats
    last_suspicious = suspicious
    last_activities = activities

    result_box.delete("1.0", tk.END)

    result_box.insert(
        tk.END,
        "===== LOG ANALYSIS REPORT =====\n\n"
    )

    result_box.insert(
        tk.END,
        f"📄 Total Logs: {stats['total']}\n"
    )

    result_box.insert(
        tk.END,
        f"ℹ INFO: {stats['info']}\n"
    )

    result_box.insert(
        tk.END,
        f"⚠ WARNING: {stats['warning']}\n"
    )

    result_box.insert(
        tk.END,
        f"❌ ERROR: {stats['error']}\n\n"
    )

    result_box.insert(
        tk.END,
        "🚨 Suspicious IP Activity\n"
    )

    result_box.insert(
        tk.END,
        "-" * 35 + "\n"
    )

    if suspicious:
        for ip, attempts in suspicious.items():

            risk = "HIGH" if attempts >= 5 else "MEDIUM"

            result_box.insert(
                tk.END,
                f"[{risk}] {ip} → {attempts} failed attempts\n"
            )

    else:
        result_box.insert(
            tk.END,
            "No suspicious activity detected.\n"
        )

    result_box.insert(
        tk.END,
        "\n🔎 Suspicious Log Entries\n"
    )

    result_box.insert(
        tk.END,
        "-" * 35 + "\n"
    )

    if activities:

        for activity in activities:
            result_box.insert(
                tk.END,
                f"{activity}\n"
            )

    else:
        result_box.insert(
            tk.END,
            "No suspicious log entries found.\n"
        )

    show_charts(stats, suspicious)

    status_bar.config(
        text="Analysis completed successfully"
    )


# Main Window
root = tk.Tk()
root.title("LogSentinel")
root.geometry("800x600")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

# Title
title = tk.Label(
    root,
    text="🛡 LogSentinel",
    font=("Arial", 22, "bold"),
    bg="#1e1e1e",
    fg="#00ff99"
)
title.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Cybersecurity Log Analyzer",
    font=("Arial", 12),
    bg="#1e1e1e",
    fg="white"
)
subtitle.pack()

# Buttons Frame
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=20)

upload_btn = tk.Button(
    button_frame,
    text="📂 Upload Log File",
    command=upload_file,
    width=20,
    bg="#00ff99",
    fg="black",
    font=("Arial", 10, "bold")
)
upload_btn.grid(row=0, column=0, padx=10)

analyze_btn = tk.Button(
    button_frame,
    text="🔍 Analyze Logs",
    command=analyze,
    width=20,
    bg="#00ff99",
    fg="black",
    font=("Arial", 10, "bold")
)
analyze_btn.grid(row=0, column=1, padx=10)

export_btn = tk.Button(
    button_frame,
    text="📄 Export Report",
    command=export_report,
    width=20,
    bg="#00ff99",
    fg="black",
    font=("Arial", 10, "bold")
)
export_btn.grid(row=0, column=2, padx=10)

# File Label
file_label = tk.Label(
    root,
    text="No file selected",
    bg="#1e1e1e",
    fg="white"
)
file_label.pack()

# Results Area with Scrollbar
result_frame = tk.Frame(root, bg="#1e1e1e")
result_frame.pack(pady=20)

scrollbar = tk.Scrollbar(result_frame)

result_box = tk.Text(
    result_frame,
    width=90,
    height=22,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white",
    font=("Consolas", 11),
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=result_box.yview)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_box.pack(side=tk.LEFT)

# Status Bar
status_bar = tk.Label(
    root,
    text="Ready",
    bd=1,
    relief=tk.SUNKEN,
    anchor=tk.W,
    bg="#111111",
    fg="white"
)

status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()