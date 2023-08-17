from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('output.html')

@app.route('/major')
def major():
    return render_template('major.html')

@app.route('/minor')
def minor():
    return render_template('minor.html')

@app.route('/minor2')
def minor2():
    return render_template('minor2.html')

if __name__ == '__main__':
    app.run(port="5000", debug = True)