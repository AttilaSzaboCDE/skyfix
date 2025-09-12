from sqlite3 import connect

# Database name
database_name = "skyfix_database.db"

# Create a connection 
conn = connect(database_name)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS alerts_list
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               service_name TEXT,
               issue_type TEXT,
               timestamp TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS other_issues_list
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               script_id TEXT,
               description TEXT,
               status TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS scripts_log_list
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               script_id TEXT,
               service_name TEXT,
               status TEXT)''')

conn.commit()
conn.close()