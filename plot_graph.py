import matplotlib.pyplot as plt
import csv
import re
def extract_sections_from_text(text):
    results = []
    # Find all sections that start with ****** ... ******** and extract the table in each
    for match in re.finditer(
        r"(\*{6,}\s+.*?\s+\*{6,})[\s\S]+?\| *Payload Size *\| *Average Latency \[µs\] *\|([\s\S]+?)\n\s*\nFinished!",
        text
    ):
        section_header = re.sub(r"[\*\s]+", "", match.group(1))
        table_body = match.group(2)
        rows = re.findall(r"\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|", table_body)
        # Remove separator row if present
        rows = [row for row in rows if not (row[0].strip().startswith('-') and row[1].strip().startswith('-'))]
        results.append((section_header, rows))
    return results

def write_tables_to_csv(results):
    for header, table in results:
        filename = f"{header}.csv"
        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Payload Size", "Average Latency [µs]"])
            for payload, latency in table:
                writer.writerow([payload.strip(), latency.strip()])

def process_report_file(report_path):
    with open(report_path, encoding="utf-8") as f:
        text = f.read()
    results = extract_sections_from_text(text)
    write_tables_to_csv(results)

process_report_file("report.txt")


# Helper function to read payload sizes and latencies from a CSV file
def read_csv_data(filepath):
    payload_sizes = []
    latencies = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            payload_sizes.append(row["Payload Size"])
            latencies.append(float(row["Average Latency [µs]"]))
    return payload_sizes, latencies

# Read data from CSV files
mq_payloads, message_queue = read_csv_data("MESSAGEQUEUE.csv")
us_payloads, unix_socket = read_csv_data("UNIXDOMAINSOCKET.csv")
ix_payloads, iceoryx = read_csv_data("ICEORYX.csv")
ixc_payloads, iceoryx_c_api = read_csv_data("ICEORYXCAPI.csv")

# Convert payload sizes to KB for plotting
def payload_to_kb(payload_list):
    kb_list = []
    for p in payload_list:
        if "MB" in p:
            kb_list.append(float(p.split()[0]) * 1000)
        elif "KB" in p or "kB" in p:
            kb_list.append(float(p.split()[0]))
        else:
            kb_list.append(float(p.split()[0]) / 1000)
    return kb_list

payload_sizes_kb = payload_to_kb(mq_payloads)
payload_sizes_fixed = mq_payloads  # Use the labels from the CSV

selected_ticks = list(range(len(payload_sizes_fixed)))  # Show all ticks

# # Plot
# plt.figure(figsize=(12, 6))
# plt.plot(payload_sizes_kb, message_queue, label="Message Queue", marker='o')
# plt.plot(payload_to_kb(us_payloads), unix_socket, label="UNIX Domain Socket", marker='s')
# plt.plot(payload_to_kb(ix_payloads), iceoryx, label="Iceoryx", marker='^')
# plt.plot(payload_to_kb(ixc_payloads), iceoryx_c_api, label="Iceoryx C API", marker='v')

# # Labels, legend, and grid
# plt.title("IPC Latency vs Payload Size")
# plt.xlabel("Payload Size")
# plt.ylabel("Average Latency (µs)")
# plt.xticks([payload_sizes_kb[i] for i in selected_ticks],
#            [payload_sizes_fixed[i] for i in selected_ticks], rotation=45)
# plt.yscale('log')
# plt.grid(True, which="both", linestyle="--", linewidth=0.5)
# plt.legend()
# plt.tight_layout()
# plt.show()

# Plot only the last six values
plt.figure(figsize=(12, 6))
plt.plot(payload_sizes_kb[-6:], message_queue[-6:], label="Message Queue", marker='o')
plt.plot(payload_to_kb(us_payloads)[-6:], unix_socket[-6:], label="UNIX Domain Socket", marker='s')
plt.plot(payload_to_kb(ix_payloads)[-6:], iceoryx[-6:], label="Iceoryx", marker='^')
plt.plot(payload_to_kb(ixc_payloads)[-6:], iceoryx_c_api[-6:], label="Iceoryx C API", marker='v')

# Labels, legend, and grid
plt.title("IPC Latency vs Payload Size (Last Six Values)")
plt.xlabel("Payload Size")
plt.ylabel("Average Latency (µs)")
plt.xticks([payload_sizes_kb[i] for i in selected_ticks[-6:]],
           [payload_sizes_fixed[i] for i in selected_ticks[-6:]], rotation=45)
plt.yscale('log')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()