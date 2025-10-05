from datetime import datetime
import sqlite3
from threading import Lock

db_lock = Lock()

database_name = "/data/skyfix_database.db"

def get_connection():
    return sqlite3.connect(database_name)

def insert_alert(resourcename, alert_service_type, alert_reason, timestamp):
    with db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO alerts_list (service_name, service_type, issue_type, timestamp) VALUES (?, ?, ?, ?)",
            (resourcename, alert_service_type, alert_reason, timestamp)
        )
        conn.commit()
        conn.close()

def insert_other_issue(service_name, alert_service_type, description, timestamp, status):
    with db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO other_issues_list (service_name, service_type, description, timestamp, status) VALUES (?, ?, ?, ?, ?)",
            (service_name, alert_service_type, description, timestamp, status)
        )
        conn.commit()
        conn.close()

def insert_script_log(service_name, alert_service_type, script_name, timestamp, status):
    with db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scripts_log_list (service_name, service_type, script_name, timestamp, status) VALUES (?, ?, ?, ?, ?)",
            (service_name, alert_service_type, script_name, timestamp, status)
        )
        conn.commit()
        conn.close()

##############################################

def get_alerts_sql(date_from, date_to):
    with db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT service_name, service_type, issue_type, timestamp FROM alerts_list "
            "WHERE DATE(timestamp) BETWEEN ? AND ?",
            (date_from, date_to)
        )
        rows = cur.fetchall()
        conn.close()
        return rows

def get_other_issues(date_from, date_to):
    with db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT service_name, service_type, description, timestamp, status FROM other_issues_list "
                    "WHERE DATE(timestamp) BETWEEN ? AND ?", (date_from, date_to))
        rows = cur.fetchall()
        conn.close()
        return rows

def get_script_logs(date_from, date_to):
    with db_lock:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT service_name, service_type, script_name, timestamp, status FROM scripts_log_list "
                    "WHERE DATE(timestamp) BETWEEN ? AND ?", (date_from, date_to))
        rows = cur.fetchall()
        conn.close()
        return rows

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT service_type, LOWER(status), COUNT(*)
        FROM scripts_log_list
        GROUP BY service_type, LOWER(status)
    """)
    results = cursor.fetchall()
    conn.close()

    stats = {}
    for service_type, status, count in results:
        if service_type not in stats:
            stats[service_type] = {"success": 0, "failed": 0}
        if status == "success":
            stats[service_type]["success"] = count
        else:
            stats[service_type]["failed"] = count

    total_success = sum(v["success"] for v in stats.values())
    total_failed = sum(v["failed"] for v in stats.values())
    stats["summary"] = {"success": total_success, "failed": total_failed}

    return stats

# Create a connection
conn = sqlite3.connect(database_name)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS alerts_list
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT,
                service_type TEXT,
                issue_type TEXT,
                timestamp TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS other_issues_list
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              service_name TEXT,
              service_type TEXT,
              description TEXT,
              timestamp TEXT,
              status TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS scripts_log_list
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               service_name TEXT,
               service_type TEXT,
               script_name TEXT,
               timestamp TEXT,
               status TEXT)''')

conn.commit()
conn.close()
