<h1 align="center">
  <img src="./hi.gif" alt="Mão acenando" width="30px">
  BestStore - Sistema de E-commerce
</h1>

<p align="center">
  🛒🚀 Uma plataforma completa de e-commerce para gerenciar anúncios, usuários, categorias e vendas online
</p>

<p align="center">
  <a href="#-sobre">📋 Sobre</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-funcionalidades">✨ Funcionalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-execução">⚙ Execução</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-tecnologias">🚀 Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-ferramentas">🔧 Ferramentas</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-autor">👤 Autor</a>
</p>

<br />

<p align="center">
  <a href="https://twitter.com/Wesley_AllanS" target="_blank">
    <img alt="Twitter: Wesley_AllanS" src="https://img.shields.io/twitter/follow/Wesley_AllanS.svg?style=social" />
  </a>
</p>

## 📋 Sobre

O BestStore é uma aplicação web completa de e-commerce desenvolvida em Flask. Com uma arquitetura robusta e interface intuitiva, a plataforma oferece todas as funcionalidades essenciais para um marketplace online moderno.

## ✨ Funcionalidades

### 👥 Gestão de Usuários

- Cadastro e autenticação de usuários
- Sistema de login/logout seguro
- Perfis completos com dados pessoais e endereço
- Gerenciamento de contas

### 🏷️ Sistema de Categorias

- Criação e organização de categorias de produtos

### 📢 Gestão de Anúncios

- Criação e publicação de anúncios
- Vinculação com categorias e usuários

### ⭐ Sistema de Favoritos

- Favoritar anúncios de interesse
- Lista personalizada de favoritos por usuário

### 💬 Interação Social

- Sistema de perguntas e respostas em anúncios

### 🛒 Sistema de Compras

- Processamento de pedidos
- Histórico de compras

### 📊 Relatórios

- Relatórios de vendas
- Relatórios de compras

## ⚙ Execução

### 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/)

### 🚀 Instalação

Para executar o projeto localmente, siga os passos abaixo:

1. Clone o repositório:

```bash
git clone https://github.com/wesleyallan/best-store
```

2. Entre no diretório do projeto:

```bash
cd best-store
```

3. Crie um ambiente virtual Python:

```bash
python -m venv venv
```

4. Ative o ambiente virtual:

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

5. Instale as dependências:

```bash
pip install -r requirements.txt
```

6. Configurar variável de ambiente `FLASK_APP`:

```bash
# Linux/Mac
export FLASK_APP=beststore

# Windows (Command Prompt)
set FLASK_APP=beststore

# Windows (PowerShell)
$env:FLASK_APP="beststore"
```

7. Inicie o banco de dados:

```bash
docker compose -p beststore-database -f infra/database/compose.yaml up -d
```

8. Inicie a aplicação:

```bash
flask run
```

O projeto estará disponível em `http://localhost:5000`

## 🚀 Tecnologias

Este projeto foi desenvolvido utilizando as seguintes tecnologias:

- [Flask](https://flask.palletsprojects.com/) - Framework web Python
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - ORM para banco de dados
- [Flask-Login](https://flask-login.readthedocs.io/) - Gerenciamento de sessões de usuário
- [MySQL](https://www.mysql.com/) - Sistema de gerenciamento de banco de dados
- [Docker](https://www.docker.com/) - Containerização do banco de dados
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Gerenciamento de variáveis de ambiente
- [Jinja2](https://jinja.palletsprojects.com/) - Engine de templates
- [HTML/CSS](https://developer.mozilla.org/pt-BR/docs/Web/HTML) - Estrutura e estilo da interface

## 🔧 Ferramentas

Ferramentas utilizadas no desenvolvimento:

- [Visual Studio Code](https://code.visualstudio.com/) - Editor de código
- [Git](https://git-scm.com/) - Sistema de controle de versão
- [Docker Desktop](https://www.docker.com/products/docker-desktop) - Gerenciamento de containers
- [MySQL Workbench](https://www.mysql.com/products/workbench/) - Administração do banco de dados

## 👤 Autor

**Wesley Silva**

- Website: [wesleyallan.dev](https://wesleyallan.dev)
- Twitter: [@Wesley_AllanS](https://twitter.com/Wesley_AllanS)
- Github: [@wesleyallan](https://github.com/wesleyallan)
- LinkedIn: [@wesleyallan](https://linkedin.com/in/wesleyallan)

## ⭐️ Apoie o Projeto

Se este projeto te ajudou, considere dar uma estrela! Isso ajuda a manter o projeto ativo e incentiva novas contribuições.

---

<br/>
<p align="center">
  Desenvolvido com ❤️ por Wesley Silva
</p>
