import secrets
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import SubscriptionClient
from detection import *
from database.skyfix_db import get_other_issues, get_script_logs, get_alerts_sql, get_stats



app = Flask(__name__, template_folder='template')
app.secret_key = secrets.token_hex(16)

# Variables
azure_credentials = {
    "tenant_id": None,
    "client_id": None,
    "client_secret": None
}

tenant_id = None
client_id = None
client_secret = None

def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  # Flask kompatibilitás miatt
    return wrapper

@app.route('/')
@login_required
def base_monitor():
    return render_template('base_monitor.html', alerts=alert_list, runnings=running_list, results=results_list, missing_list=missing_list)

@app.route('/alert', methods=['POST'])
def handle_alert():
    data = request.json
    detection_check(data, selected_sub, tenant_id, client_id, client_secret)
    # print(data)
    return "OK", 200

@app.route("/login", methods=["GET", "POST"])
def login():
    global azure_credentials, client_id, client_secret, tenant_id
    global subs

    if request.method == "POST":
        tenant_id = request.form.get("directoryid")
        client_id = request.form.get("applicationid")
        client_secret = request.form.get("clientsecretval")   
        try:
            # Azure authentication
            credential = ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
            sub_client = SubscriptionClient(credential)
            subs = list(sub_client.subscriptions.list())
            if subs:
                # Global variables settings
                azure_credentials["tenant_id"] = tenant_id
                azure_credentials["client_id"] = client_id
                azure_credentials["client_secret"] = client_secret
                # Session login alert
                session["logged_in"] = True
                return redirect(url_for("base_monitor"))
            else:
                return render_template("login.html", error="There are no subscriptions!")
        except Exception as e:
            return render_template("login.html", error=f"Error: your credentials are not correct!")
    return render_template("login.html")

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    global selected_sub
    if request.method == 'POST':
        # Choose the subscription
        selected_sub = request.form.get('subscription')
        session['selected_subscription'] = selected_sub
        return redirect(url_for('base_monitor'))
    return render_template('settings.html', subscriptions=subs, selected_sub=session.get('selected_subscription'))

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    ## variables
    tables = ["alerts_list", "other_issues_list", "script_logs_list"]
    selected_table = None
    date_from = None
    date_to = None
    database_list = []
    table_columns = []

    if request.method == "POST":
        selected_table = request.form.get("table")
        date_from = request.form.get("date_from")
        date_to = request.form.get("date_to")
        if selected_table == "alerts_list":
            table_columns = ["Service name", "Service type","Issue type", "Time"]
            database_list = get_alerts_sql(date_from, date_to)
        elif selected_table == "other_issues_list":
            table_columns = ["Service name", "Service type","Description", "Time", "Status"]
            database_list = get_other_issues(date_from, date_to)
        elif selected_table == "script_logs_list":
            table_columns = ["Service name", "Service type","Script name", "Time", "Status"]
            database_list = get_script_logs(date_from, date_to)
    return render_template('history.html', db_results=database_list, tables=tables, selected_table=selected_table, table_columns=table_columns, date_from=date_from, date_to=date_to)

@app.route("/stats")
def stats():
    return jsonify(get_stats())

@app.route('/vizualization')
@login_required
def vizualization():
    return render_template('vizualization.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)
