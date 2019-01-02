from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

def getDate():
    x = datetime.datetime.now()
    return str(x.strftime("%x"))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        print(request.form['workout'])
    return render_template('log.html')



if __name__ == '__main__':
    app.run(debug=True, port=8080)
