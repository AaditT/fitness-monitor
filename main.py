from flask import Flask, Markup, render_template, redirect, url_for, request



app = Flask(__name__)

def updateDB():
    global mega_list
    mega_list = []
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
    for i in range(0, len(types)):
        mega_list.append(dict(count=counts[i],date=dates[i],type=types[i]))
    return [mega_list, types, counts, dates]

def getPushups():
    total_types = updateDB()[1]
    total_counts = updateDB()[2]
    total_dates = updateDB()[3]
    pushup_indexes = []
    for ind_type in total_types:
        if ind_type == "push-up":
            pushup_indexes.append(int(total_types.index(ind_type)))
    counts = []
    dates = []
    for index in pushup_indexes:
        counts.append(total_counts[index])
        dates.append(total_dates[index])
    return [dates, counts]

def getCurlups():
    total_types = updateDB()[1]
    total_counts = updateDB()[2]
    total_dates = updateDB()[3]
    curlup_indexes = []
    for ind_type in total_types:
        if ind_type == "curl-up":
            curlup_indexes.append(int(total_types.index(ind_type)))
    counts = []
    dates = []
    for index in curlup_indexes:
        counts.append(total_counts[index])
        dates.append(total_dates[index])
    return [dates, counts]

def getPullups():
    total_types = updateDB()[1]
    total_counts = updateDB()[2]
    total_dates = updateDB()[3]
    pullup_indexes = []
    for ind_type in total_types:
        if ind_type == "pull-up":
            pullup_indexes.append(int(total_types.index(ind_type)))
    counts = []
    dates = []
    for index in pullup_indexes:
        counts.append(total_counts[index])
        dates.append(total_dates[index])
    return [dates, counts]

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


def getDate():
    x = datetime.datetime.now()
    return str(x.strftime("%x"))

@app.route('/')
def home():
    return redirect(url_for('graph'))

@app.route('/table')
def index():
    error=None
    return render_template('index.html',list=updateDB()[0],error=error)


@app.route('/log', methods=['GET', 'POST'])
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
    app.run(debug=True, port=8080)
