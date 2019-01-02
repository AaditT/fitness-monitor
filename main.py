from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

def updateDB():
    types = []
    counts = []
    dates = []
    tFile = open("type.txt", 'r')
    for line in tFile.readlines():
        types.append(str(line.rstrip()))
    cFile = open("count.txt", 'r')
    for line in cFile.readlines():
        counts.append(str(line.rstrip()))
    dFile = open("date.txt", 'r')
    for line in dFile.readlines():
        dates.append(str(line.rstrip()))
    return [counts, dates, types]

def getDate():
    x = datetime.datetime.now()
    return str(x.strftime("%x"))

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    updateDB()
    return render_template('index.html',counts=updateDB()[0],dates=updateDB()[1],types=updateDB()[2])

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        workout_type = str(request.form['workout'])
        workout_date = str(request.form['start'])
        workout_count = str(request.form['count'])
        tFile = open("type.txt", 'a')
        tFile.write(workout_type+"\n")
        dFile = open("date.txt", 'a')
        dFile.write(workout_date+"\n")
        cFile = open("count.txt", 'a')
        cFile.write(workout_count+"\n")
        return redirect(url_for('index'))
    return render_template('log.html')



if __name__ == '__main__':
    app.run(debug=True, port=8080)
