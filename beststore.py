from flask import Flask, make_response
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv('.env.development')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(500))
    nome = db.Column(db.String(256), nullable=False)

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/login')
def login():
  cookie = request.cookies.get("username")
  if cookie:
    return render_template("user.html", username=cookie)
  else:
    return render_template("login.html")

@app.route('/user')
@app.route('/user/<username>')
def user(username):
  response.set_cookie("username", username)
  return render_template("user.html", username=username)

@app.route('/teste')
@app.route('/teste/<info>')
def teste(info):
  return f"<h1>teste: {escape(info)}</h1>"
