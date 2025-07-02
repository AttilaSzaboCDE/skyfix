from flask import Flask, render_template

app = Flask(__name__, template_folder='template')

@app.route('/')
def monitoring():
    return render_template('monitoring.html')

@app.route('/vm_monitoring')
def vm_monitoring():
    return render_template('vm_monitoring.html')

@app.route('/container_monitoring')
def container_monitoring():
    return render_template('container_monitoring.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/scripts')
def scripts():
    return render_template('scripts.html')


if __name__ == '__main__':
    app.run(debug=True)