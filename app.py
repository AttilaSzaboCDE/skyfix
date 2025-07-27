from flask import Flask, render_template


app = Flask(__name__, template_folder='template')

@app.route('/')
def base_monitor():
    return render_template('base_monitor.html')

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
    app.run(debug=True, host='0.0.0.0', port=5001)