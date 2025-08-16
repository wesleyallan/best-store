from flask import Flask, make_response
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/login')
def login():
  return render_template("login.html")
