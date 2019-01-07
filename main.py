from flask import Flask, Markup, render_template, redirect, url_for, request
from flask_basicauth import BasicAuth
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'YOUR_USERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'YOUR_PASSWORD'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

@app.route('/index')
def graph():

    pushup_counts = []
    cFile = open("workoutdb/pushup_count.txt", 'r')
    for line in cFile.readlines():
        pushup_counts.append(str(line.rstrip()))
    pushup_dates = []
    dFile = open("workoutdb/pushup_date.txt", 'r')
    for line in dFile.readlines():
        pushup_dates.append(str(line.rstrip()))

    pullup_counts = []
    eFile = open("workoutdb/pullup_count.txt", 'r')
    for line in eFile.readlines():
        pullup_counts.append(str(line.rstrip()))
    pullup_dates = []
    fFile = open("workoutdb/pullup_date.txt", 'r')
    for line in fFile.readlines():
        pullup_dates.append(str(line.rstrip()))

    curlup_counts = []
    gFile = open("workoutdb/curlup_count.txt", 'r')
    for line in gFile.readlines():
        curlup_counts.append(str(line.rstrip()))
    curlup_dates = []
    hFile = open("workoutdb/curlup_date.txt", 'r')
    for line in hFile.readlines():
        curlup_dates.append(str(line.rstrip()))


    bar_labels=pushup_dates
    bar_values=pushup_counts
    return render_template('bar_chart.html', title='Push-up Monitor', max=150, pushup_counts=pushup_counts,pushup_dates=pushup_dates,pullup_counts=pullup_counts,pullup_dates=pullup_dates,curlup_counts=curlup_counts,curlup_dates=curlup_dates)

@app.route('/')
def home():
    return redirect(url_for('graph'))


@app.route('/log', methods=['GET', 'POST'])
@basic_auth.required
def log():
    if request.method == 'POST':
        error = None
        workout_type = str(request.form['workout'])
        workout_date = str(request.form['start'])
        workout_count = str(request.form['count'])
        if not workout_type or not workout_date or not workout_count:
            error = "Please fill out all entries!"
            return render_template('log.html', error=error)
        else:
            if workout_type == "push-up":
                pFile = open("workoutdb/pushup_count.txt", 'a')
                pFile.write(workout_count+"\n")
                cFile = open("workoutdb/pushup_date.txt", 'a')
                cFile.write(workout_date+"\n")
            elif workout_type == "curl-up":
                pFile = open("workoutdb/curlup_count.txt", 'a')
                pFile.write(workout_count+"\n")
                cFile = open("workoutdb/curlup_date.txt", 'a')
                cFile.write(workout_date+"\n")
            elif workout_type == "pull-up":
                pFile = open("workoutdb/pullup_count.txt", 'a')
                pFile.write(workout_count+"\n")
                cFile = open("workoutdb/pullup_date.txt", 'a')
                cFile.write(workout_date+"\n")
            error = None
            tFile = open("type.txt", 'a')
            tFile.write(workout_type+"\n")
            dFile = open("date.txt", 'a')
            dFile.write(workout_date+"\n")
            cFile = open("count.txt", 'a')
            cFile.write(workout_count+"\n")
            return redirect(url_for('graph'))
    return render_template('log.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=8080)
