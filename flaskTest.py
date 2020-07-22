#from flask import Flask
#app = Flask(__name__)

#@app.route("/output")
#def output():
#    return render_template("test.html", name="Joe")
    
#if __name__ == "__main__":
#    app.run()

#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
    # serve test template
    return render_template('test.html', name='Joe')

@app.route('/receiver', methods = ['POST'])
def worker():
    # read json + reply
    data = request.get_json()
    result = ''

    for item in data:
        # loop over every row
        result += str(item['make']) + '\n'

    return result

if __name__ == '__main__':
    # run!
    app.run()
