from flask import Flask, Markup, render_template, redirect, url_for, request

global pushup_counts
global pushup_dates
global curlup_counts
global curlup_dates
global pullup_counts
global pullup_dates

pushup_counts = []
pushup_dates = []
curlup_counts = []
curlup_dates = []
pullup_counts = []
pullup_counts = []

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

@app.route('/pushup')
def pushup():
    updateDB()
    bar_labels=getPushups()[0]
    bar_values=getPushups()[1]
    return render_template('bar_chart.html', title='Push-up Monitor', max=150, labels=bar_labels, values=bar_values)

@app.route('/curlup')
def curlup():
    updateDB()
    bar_labels=getCurlups()[0]
    bar_values=getCurlups()[1]
    return render_template('bar_chart.html', title='Curl-up Monitor', max=150, labels=bar_labels, values=bar_values)

@app.route('/pullup')
def pullup():
    updateDB()
    bar_labels=getPullups()[0]
    bar_values=getPullups()[1]
    return render_template('bar_chart.html', title='Pull-up Monitor', max=150, labels=bar_labels, values=bar_values)

def getDate():
    x = datetime.datetime.now()
    return str(x.strftime("%x"))

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
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
                pushup_dates.append(workout_date)
                pushup_counts.append(workout_count)
            elif workout_type == "curl-up":
                curlup_dates.append(workout_date)
                curlup_counts.append(workout_count)
            elif workout_type == "pull-up":
                pullup_dates.append(workout_date)
                pullup_counts.append(workout_count)
            error = None
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
