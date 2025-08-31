from flask import Flask, make_response, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv('.env.development')

app = Flask(__name__)

database_uri = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
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
    id_categoria = db.Column(db.Integer, db.ForeignKey(
        "categoria.id"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        "usuario.id"), nullable=False)

    categoria = db.relationship('Categoria', backref='anuncios')
    usuario = db.relationship('Usuario', backref='anuncios')

    def __init__(self, anunciocol, id_categoria, id_usuario):
        self.anunciocol = anunciocol
        self.id_categoria = id_categoria
        self.id_usuario = id_usuario


class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        "usuario.id"), nullable=False)
    id_anuncio = db.Column(db.Integer, db.ForeignKey(
        "anuncio.id"), nullable=False)

    usuario = db.relationship('Usuario', backref='favoritos')
    anuncio = db.relationship('Anuncio', backref='favoritos')

    def __init__(self, id_usuario, id_anuncio):
        self.id_usuario = id_usuario
        self.id_anuncio = id_anuncio


class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column(db.Integer, primary_key=True)
    id_anuncio = db.Column(db.Integer, db.ForeignKey(
        "anuncio.id"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        "usuario.id"), nullable=False)
    pergunta = db.Column(db.Text, nullable=False)

    anuncio = db.relationship('Anuncio', backref='perguntas')
    usuario = db.relationship('Usuario', backref='perguntas')

    def __init__(self, id_anuncio, id_usuario, pergunta):
        self.id_anuncio = id_anuncio
        self.id_usuario = id_usuario
        self.pergunta = pergunta


class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        "usuario.id"), nullable=False)
    mt_pagamento = db.Column(db.String(50))
    frete = db.Column(db.Float)
    dt_hora = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='compras')

    def __init__(self, id_usuario, mt_pagamento=None, frete=None, dt_hora=None):
        self.id_usuario = id_usuario
        self.mt_pagamento = mt_pagamento
        self.frete = frete
        if dt_hora:
            self.dt_hora = dt_hora


class CompraAnuncio(db.Model):
    __tablename__ = "compra_anuncio"
    id = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey(
        "compra.id"), nullable=False)
    id_anuncio = db.Column(db.Integer, db.ForeignKey(
        "anuncio.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    compra = db.relationship('Compra', backref='itens')
    anuncio = db.relationship('Anuncio', backref='compras_anuncio')

    def __init__(self, id_compra, id_anuncio, quantidade=1):
        self.id_compra = id_compra
        self.id_anuncio = id_anuncio
        self.quantidade = quantidade


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('404.html')


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


@app.route("/categoria")
def categoria():
    return render_template('categoria.html', categorias=Categoria.query.all(), titulo='Categoria')


@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('descricao'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/usuario")
def usuario():
    return render_template('usuario.html', usuarios=Usuario.query.all(), titulo='Usuário')


@app.route("/usuario/novo", methods=['POST'])
def novousuario():
    dt_nascimento = None
    if request.form.get('dt_nascimento'):
        try:
            dt_nascimento = datetime.strptime(
                request.form.get('dt_nascimento'), '%Y-%m-%d').date()
        except ValueError:
            pass

    usuario = Usuario(
        nome=request.form.get('nome'),
        email=request.form.get('email'),
        cpf=request.form.get('cpf'),
        dt_nascimento=dt_nascimento,
        telefone=request.form.get('telefone'),
        rua=request.form.get('rua'),
        cidade=request.form.get('cidade'),
        bairro=request.form.get('bairro'),
        numero=request.form.get('numero')
    )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))


@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return usuario.nome
    return "Usuário não encontrado"


@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return redirect(url_for('usuario'))

    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.cpf = request.form.get('cpf')

        if request.form.get('dt_nascimento'):
            try:
                usuario.dt_nascimento = datetime.strptime(
                    request.form.get('dt_nascimento'), '%Y-%m-%d').date()
            except ValueError:
                pass

        usuario.telefone = request.form.get('telefone')
        usuario.rua = request.form.get('rua')
        usuario.cidade = request.form.get('cidade')
        usuario.bairro = request.form.get('bairro')
        usuario.numero = request.form.get('numero')

        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))

    return render_template('eusuario.html', usuario=usuario, titulo="Usuário")


@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect(url_for('usuario'))


@app.route("/anuncio")
def anuncio():
    return render_template('anuncio.html',
                           anuncios=Anuncio.query.all(),
                           categorias=Categoria.query.all(),
                           usuarios=Usuario.query.all(),
                           titulo='Anúncio')


@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio():
    anuncio = Anuncio(
        anunciocol=request.form.get('anunciocol'),
        id_categoria=request.form.get('id_categoria'),
        id_usuario=request.form.get('id_usuario')
    )
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))


@app.route("/pergunta")
@app.route("/pergunta/<int:id_anuncio>")
def pergunta(id_anuncio=None):
    anuncio = None
    if id_anuncio:
        anuncio = Anuncio.query.get_or_404(id_anuncio)

    return render_template('pergunta.html',
                           anuncio=anuncio,
                           anuncios=Anuncio.query.all(),
                           usuarios=Usuario.query.all())


@app.route("/pergunta/nova", methods=['POST'])
def novapergunta():
    pergunta = Pergunta(
        id_anuncio=request.form.get('id_anuncio'),
        id_usuario=request.form.get('id_usuario'),
        pergunta=request.form.get('pergunta')
    )
    db.session.add(pergunta)
    db.session.commit()

    return redirect(url_for('pergunta', id_anuncio=request.form.get('id_anuncio')))


@app.route("/favoritar/<int:id_anuncio>")
def favoritar(id_anuncio):
    usuario_id = 1
    favorito_existe = Favorito.query.filter_by(
        id_usuario=usuario_id, id_anuncio=id_anuncio).first()

    if not favorito_existe:
        favorito = Favorito(id_usuario=usuario_id, id_anuncio=id_anuncio)
        db.session.add(favorito)
        db.session.commit()

    return redirect(url_for('anuncio'))


@app.route("/favoritos")
def favoritos():
    usuario_id = 1
    favoritos = Favorito.query.filter_by(id_usuario=usuario_id).all()
    return render_template('favoritos.html', favoritos=favoritos)


@app.route("/comprar/<int:id_anuncio>")
def comprar(id_anuncio):
    usuario_id = 1

    compra = Compra(id_usuario=usuario_id, mt_pagamento="Cartão", frete=10.00)
    db.session.add(compra)
    db.session.flush()

    compra_anuncio = CompraAnuncio(
        id_compra=compra.id, id_anuncio=id_anuncio, quantidade=1)
    db.session.add(compra_anuncio)
    db.session.commit()

    return f"<h4>Compra realizada com sucesso! ID: {compra.id}</h4>"


@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html')


@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html')


@app.route('/user')
@app.route('/user/<username>')
def user(username):
    response = make_response(render_template("user.html", username=username))
    response.set_cookie("username", username)
    return response


if __name__ == 'beststore':
    print("Banco de dados inicializado!")
    db.create_all()
