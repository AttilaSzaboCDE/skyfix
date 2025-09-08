import secrets
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import SubscriptionClient
from detection import *


app = Flask(__name__, template_folder='template')

app.secret_key = secrets.token_hex(16)


# Globális változó, hogy minden route elérje
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
    results = detection_check(data, selected_sub, tenant_id, client_id, client_secret)
    # print(f"Resource Name: {data}")
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
            # Azure hitelesítés
            credential = ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
            sub_client = SubscriptionClient(credential)
            subs = list(sub_client.subscriptions.list())

            if subs:
                # Globális változóba mentés
                azure_credentials["tenant_id"] = tenant_id
                azure_credentials["client_id"] = client_id
                azure_credentials["client_secret"] = client_secret
                
                # Session bejelentkezés jelzés
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
        # Felhasználó kiválasztotta az előfizetést
        selected_sub = request.form.get('subscription')
        session['selected_subscription'] = selected_sub
        return redirect(url_for('base_monitor'))
     
    return render_template('settings.html', subscriptions=subs, selected_sub=session.get('selected_subscription'))


### Incoming features
@app.route('/add_new_script')
@login_required
def add_new_script():
    return render_template('add_new_script.html')

@app.route('/manage_scripts')
@login_required
def manage_scripts():
    return render_template('manage_scripts.html')

@app.route('/delete_scripts')
@login_required
def delete_scripts():
    return render_template('delete_scripts.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)