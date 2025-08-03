from flask import Flask, render_template, request
import threading
import datetime
from detection import *


app = Flask(__name__, template_folder='template')


@app.route('/')
def base_monitor():
    return render_template('base_monitor.html', alerts=alert_list)

@app.route('/alert', methods=['POST'])
def handle_alert():
    data = request.json
    results = detection_check(data)
    print(f"Resource Name: {results}")
    return "OK", 200


@app.route('/add_new_script')
def add_new_script():
    return render_template('add_new_script.html')

@app.route('/manage_scripts')
def manage_scripts():
    return render_template('manage_scripts.html')

@app.route('/delete_scripts')
def delete_scripts():
    return render_template('delete_scripts.html')




if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)