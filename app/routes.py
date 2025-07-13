from app import app
from flask import Flask
from flask import render_template
from forms.newtrip import NewTripForm

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/hello")
def hello_world():
    form = NewTripForm()
    return render_template('hello.html', form=form)