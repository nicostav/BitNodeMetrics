# All Imports
import os
import sqlite3
from pathlib import Path
import psutil
from contextlib import closing


## Prepare db
def prepare_db(cursor):
    ### Create Table
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='system_metrics';"
    )
    table_exists = cursor.fetchone()
    if table_exists is None:
        cursor.execute(
            "CREATE TABLE system_metrics("
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
            ")"
        )

    ### Create Index
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_timestamp';"
    )
    index_exists = cursor.fetchone()
    if None == index_exists:
        cursor.execute("CREATE INDEX idx_timestamp ON system_metrics(timestamp)")


# Get the recursive size of a folder
def get_folder_size(folder_path):
    return sum(
        file.stat().st_size
        for file in Path(folder_path).rglob('*')
        if file.is_file()
    )


# Measure all system metrics sent to db
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

    system_measures = [
        cpu_percent_usage,
        disk_full_total,
        disk_full_used,
        disk_full_free,
        disk_full_percent,
        disk_folder_used,
        memory_total,
        memory_used,
        memory_free,
        memory_percent,
    ]

    return system_measures


# Write system metrics into db
def write_system_metrics(cursor, system_measures_to_write):
    cursor.execute(
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
        "VALUES(?,?,?,?,?,?,?,?,?,?)",
        (
            system_measures_to_write[0],
            system_measures_to_write[1],
            system_measures_to_write[2],
            system_measures_to_write[3],
            system_measures_to_write[4],
            system_measures_to_write[5],
            system_measures_to_write[6],
            system_measures_to_write[7],
            system_measures_to_write[8],
            system_measures_to_write[9],
        ),
    )


# Main
if __name__ == "__main__":
    measures = measure_system_metrics("/home/coder/Dokumente")
    with sqlite3.connect("metrics.db") as conn:
        with closing(conn.cursor()) as cur:
            prepare_db(cur)
            write_system_metrics(cur, measures)
