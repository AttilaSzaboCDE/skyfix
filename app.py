from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def monitoring():
    return render_template('monitoring.html')

@app.route('/vm_monitoring')
def vm_monitoring():
    return render_template('vm_monitoring.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/vnet_monitoring')
def vnet_monitoring():
    return render_template('vnet_monitoring.html')

@app.route('/stor_monitoring')
def stor_monitoring():
    return render_template('stor_monitoring.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/scripts')
def scripts():
    return render_template('scripts.html')


if __name__ == '__main__':
    app.run(debug=True)