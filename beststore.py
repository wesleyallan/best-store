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

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    dt_nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20))
    rua = db.Column(db.String(256))
    cidade = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    numero = db.Column(db.String(10))

    def __init__(self, nome, email, cpf, dt_nascimento=None, telefone=None, rua=None, cidade=None, bairro=None, numero=None):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.dt_nascimento = dt_nascimento
        self.telefone = telefone
        self.rua = rua
        self.cidade = cidade
        self.bairro = bairro
        self.numero = numero

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column(db.Integer, primary_key=True)
    anunciocol = db.Column(db.String(500))
    id_categoria = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    categoria = db.relationship('Categoria', backref='anuncios')
    usuario = db.relationship('Usuario', backref='anuncios')

    def __init__(self, anunciocol, id_categoria, id_usuario):
        self.anunciocol = anunciocol
        self.id_categoria = id_categoria
        self.id_usuario = id_usuario

class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    id_anuncio = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)

    usuario = db.relationship('Usuario', backref='favoritos')
    anuncio = db.relationship('Anuncio', backref='favoritos')

    def __init__(self, id_usuario, id_anuncio):
        self.id_usuario = id_usuario
        self.id_anuncio = id_anuncio

class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column(db.Integer, primary_key=True)
    id_anuncio = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    pergunta = db.Column(db.Text, nullable=False)

    anuncio = db.relationship('Anuncio', backref='perguntas')
    usuario = db.relationship('Usuario', backref='perguntas')

    def __init__(self, id_anuncio, id_usuario, pergunta):
        self.id_anuncio = id_anuncio
        self.id_usuario = id_usuario
        self.pergunta = pergunta

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
