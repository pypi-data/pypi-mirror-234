import csv
import psutil
import time
import platform
import spwf
import os

filename = os.path.join(spwf.folder_name, "Export Usage.csv")

# Open CSV file for writing
with open(filename, mode='w', newline='') as csv_file:
    # Create CSV writer
    csv_writer = csv.writer(csv_file)
    # Write header row
    csv_writer.writerow(['Time', 'CPU Usage', 'Memory Usage', 'OS'])

    # Loop indefinitely
    while True:
        # Get current time
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Get CPU and memory usage
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        # Write values to CSV
        csv_writer.writerow([current_time, cpu_usage, memory_usage, platform.system()])
        csv_file.flush()  # Force write to disk

        # Wait for one second
        time.sleep(1)
