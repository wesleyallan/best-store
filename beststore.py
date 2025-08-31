from flask import Flask, make_response, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import (current_user, LoginManager,
                         login_user, logout_user,
                         login_required)
from dotenv import load_dotenv
from datetime import datetime
import hashlib
import os

load_dotenv('.env.development')

app = Flask(__name__)

database_uri = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


secret_key = os.getenv('SECRET_KEY')
app.secret_key = secret_key

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Você precisa fazer login para acessar esta página.'


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
    senha = db.Column(db.String(256))  # Campo senha adicionado
    cpf = db.Column(db.String(14), unique=True)
    dt_nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20))
    rua = db.Column(db.String(256))
    cidade = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    numero = db.Column(db.String(10))

    def __init__(self, nome, email, senha=None, cpf=None, dt_nascimento=None, telefone=None, rua=None, cidade=None, bairro=None, numero=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.dt_nascimento = dt_nascimento
        self.telefone = telefone
        self.rua = rua
        self.cidade = cidade
        self.bairro = bairro
        self.numero = numero

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


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


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('404.html')


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if 'login' in request.form:

            email = request.form.get('email')
            senha = request.form.get('senha')

            if email and senha:

                senha_hash = hashlib.sha512(
                    str(senha).encode("utf-8")).hexdigest()
                user = Usuario.query.filter_by(
                    email=email, senha=senha_hash).first()

                if user:
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    return render_template("login.html", error="Email ou senha incorretos")

        elif 'cadastro' in request.form:

            nome = request.form.get('nome')
            email = request.form.get('email_cadastro')
            senha = request.form.get('senha_cadastro')

            if nome and email and senha:

                usuario_existente = Usuario.query.filter_by(
                    email=email).first()
                if usuario_existente:
                    return render_template("login.html", error="Email já cadastrado")

                senha_hash = hashlib.sha512(
                    str(senha).encode("utf-8")).hexdigest()

                novo_usuario = Usuario(
                    nome=nome,
                    email=email,
                    senha=senha_hash
                )
                db.session.add(novo_usuario)
                db.session.commit()

                login_user(novo_usuario)
                return redirect(url_for('index'))

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/categoria")
@login_required
def categoria():
    return render_template('categoria.html', categorias=Categoria.query.all(), titulo='Categoria')


@app.route("/categoria/criar", methods=['POST'])
@login_required
def criarcategoria():
    categoria = Categoria(request.form.get(
        'nome'), request.form.get('descricao'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/categoria/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return redirect(url_for('categoria'))

    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        categoria.descricao = request.form.get('descricao')

        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))

    return render_template('ecategoria.html', categoria=categoria, titulo="Categoria")


@app.route("/categoria/deletar/<int:id>")
@login_required
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    if categoria:
        db.session.delete(categoria)
        db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/usuario")
@login_required
def usuario():
    return render_template('usuario.html', usuarios=Usuario.query.all(), titulo='Usuário')


@app.route("/usuario/novo", methods=['POST'])
@login_required
def novousuario():
    dt_nascimento = None
    if request.form.get('dt_nascimento'):
        try:
            dt_nascimento = datetime.strptime(
                request.form.get('dt_nascimento'), '%Y-%m-%d').date()
        except ValueError:
            pass

    senha_hash = None
    if request.form.get('senha'):
        senha_hash = hashlib.sha512(
            str(request.form.get('senha')).encode("utf-8")).hexdigest()

    usuario = Usuario(
        nome=request.form.get('nome'),
        email=request.form.get('email'),
        senha=senha_hash,
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
@login_required
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return usuario.nome
    return "Usuário não encontrado"


@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return redirect(url_for('usuario'))

    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.cpf = request.form.get('cpf')

        if request.form.get('senha'):
            usuario.senha = hashlib.sha512(
                str(request.form.get('senha')).encode("utf-8")).hexdigest()

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
@login_required
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect(url_for('usuario'))


@app.route("/anuncio")
@login_required
def anuncio():

    favoritos_usuario = [f.id_anuncio for f in Favorito.query.filter_by(
        id_usuario=current_user.id).all()]

    return render_template('anuncio.html',
                           anuncios=Anuncio.query.all(),
                           categorias=Categoria.query.all(),
                           favoritos_usuario=favoritos_usuario,
                           titulo='Anúncio')


@app.route("/anuncio/criar", methods=['POST'])
@login_required
def criaranuncio():
    anuncio = Anuncio(
        anunciocol=request.form.get('anunciocol'),
        id_categoria=request.form.get('id_categoria'),
        id_usuario=current_user.id
    )
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))


@app.route("/pergunta")
@app.route("/pergunta/<int:id_anuncio>")
@login_required
def pergunta(id_anuncio=None):
    anuncio = None
    if id_anuncio:
        anuncio = Anuncio.query.get_or_404(id_anuncio)

    return render_template('pergunta.html',
                           anuncio=anuncio,
                           anuncios=Anuncio.query.all())


@app.route("/pergunta/nova", methods=['POST'])
@login_required
def novapergunta():
    pergunta = Pergunta(
        id_anuncio=request.form.get('id_anuncio'),
        id_usuario=current_user.id,
        pergunta=request.form.get('pergunta')
    )
    db.session.add(pergunta)
    db.session.commit()

    return redirect(url_for('pergunta', id_anuncio=request.form.get('id_anuncio')))


@app.route("/favoritar/<int:id_anuncio>")
@login_required
def favoritar(id_anuncio):
    favorito_existe = Favorito.query.filter_by(
        id_usuario=current_user.id, id_anuncio=id_anuncio).first()

    if favorito_existe:
        db.session.delete(favorito_existe)
    else:
        favorito = Favorito(id_usuario=current_user.id, id_anuncio=id_anuncio)
        db.session.add(favorito)

    db.session.commit()
    return redirect(url_for('anuncio'))


@app.route("/favoritos")
@login_required
def favoritos():
    favoritos = Favorito.query.filter_by(id_usuario=current_user.id).all()
    return render_template('favoritos.html', favoritos=favoritos)


@app.route("/comprar/<int:id_anuncio>")
@login_required
def comprar(id_anuncio):
    compra = Compra(id_usuario=current_user.id,
                    mt_pagamento="Cartão", frete=10.00)
    db.session.add(compra)
    db.session.flush()

    compra_anuncio = CompraAnuncio(
        id_compra=compra.id, id_anuncio=id_anuncio, quantidade=1)
    db.session.add(compra_anuncio)
    db.session.commit()

    return redirect(url_for('relCompras'))


@app.route("/relatorios/vendas")
@login_required
def relVendas():
    return render_template('relVendas.html')


@app.route("/relatorios/compras")
@login_required
def relCompras():
    return render_template('relCompras.html')


@app.route("/minha-conta", methods=['GET', 'POST'])
@login_required
def minha_conta():
    if request.method == 'POST':
        current_user.nome = request.form.get('nome')
        current_user.email = request.form.get('email')
        current_user.cpf = request.form.get('cpf')

        if request.form.get('senha'):
            current_user.senha = hashlib.sha512(
                str(request.form.get('senha')).encode("utf-8")).hexdigest()

        if request.form.get('dt_nascimento'):
            try:
                current_user.dt_nascimento = datetime.strptime(
                    request.form.get('dt_nascimento'), '%Y-%m-%d').date()
            except ValueError:
                pass

        current_user.telefone = request.form.get('telefone')
        current_user.rua = request.form.get('rua')
        current_user.cidade = request.form.get('cidade')
        current_user.bairro = request.form.get('bairro')
        current_user.numero = request.form.get('numero')

        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('minha_conta'))

    return render_template('minha_conta.html', usuario=current_user, titulo="Minha Conta")


@app.route('/user')
@app.route('/user/<username>')
def user(username):
    response = make_response(render_template("user.html", username=username))
    response.set_cookie("username", username)
    return response


if __name__ == 'beststore':
    db.create_all()
    # Comentar apenas para testar
    app.run()
