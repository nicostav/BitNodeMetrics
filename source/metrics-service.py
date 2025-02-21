import os
from sqlite3 import OperationalError

import psutil
import sqlite3

## Initialize connection db
con = sqlite3.connect("metrics.db")
cur = con.cursor()

## Prepare db
### Create Table
try:
    cur.execute("CREATE TABLE system_metrics("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                "cpu_percent REAL, "
                "disk_full_total INT, "
                "disk_full_used INT, "
                "disk_full_free INT, "
                "disk_full_percent REAL, "
                "disk_folder_used INT, "
                "memory_total INT, "
                "memory_used INT, "
                "memory_free INT, "
                "memory_percent REAL "
                ")")
except OperationalError:
    print("Table already exists")

### Create Index
try:
    cur.execute("CREATE INDEX idx_timestamp ON system_metrics(timestamp)")
except OperationalError:
    print("Index already exists")

def get_folder_size(folder_path):
    total_size = 0

    # Walk trough folder and subfolders
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            # Add to total size
            total_size += os.path.getsize(file_path)
    return total_size

def measure_system_metrics(folder_location):
    ## Measuring cpu
    cpu_percent_usage = psutil.cpu_percent(5)

    ## Measuring complete disk
    disk_full_total = psutil.disk_usage("/").total
    disk_full_used = psutil.disk_usage("/").used
    disk_full_free = psutil.disk_usage("/").free
    disk_full_percent = psutil.disk_usage("/").percent

    ## Measuring btc folder
    disk_folder_used = get_folder_size(folder_location)

    ## Measuring memory usage
    memory_total = psutil.virtual_memory().total
    memory_used = psutil.virtual_memory().used
    memory_free = psutil.virtual_memory().free
    memory_percent = psutil.virtual_memory().percent

    system_measures = [cpu_percent_usage, disk_full_total, disk_full_used, disk_full_free, disk_full_percent,
                       disk_folder_used, memory_total, memory_used, memory_free, memory_percent]

    return system_measures

def write_system_metrics(system_measures_to_write):
    cur.execute(
        "INSERT INTO system_metrics("
        "cpu_percent, "
        "disk_full_total, "
        "disk_full_used, "
        "disk_full_free, "
        "disk_full_percent, "
        "disk_folder_used,"
        "memory_total,"
        "memory_used,"
        "memory_free,"
        "memory_percent)"
        "VALUES(?,?,?,?,?,?,?,?,?,?)", (system_measures_to_write[0],
                                        system_measures_to_write[1],
                                        system_measures_to_write[2],
                                        system_measures_to_write[3],
                                        system_measures_to_write[4],
                                        system_measures_to_write[5],
                                        system_measures_to_write[6],
                                        system_measures_to_write[7],
                                        system_measures_to_write[8],
                                        system_measures_to_write[9],))
    con.commit()
    cur.close()
    con.close()

if __name__ == '__main__':
    measures = measure_system_metrics('/')
    write_system_metrics(measures)