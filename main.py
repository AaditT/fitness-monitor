from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

def getDate():
    x = datetime.datetime.now()
    return str(x.strftime("%x"))

@app.route('/')
def home():


if __name__ == '__main__':
    app.run(debug=True, port=8080)
