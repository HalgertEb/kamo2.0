from flask import Flask, render_template

app = Flask(__name__,
    static_folder='../frontend/static',
    template_folder='../frontend/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)  