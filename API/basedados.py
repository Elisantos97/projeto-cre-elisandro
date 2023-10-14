from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://eli_santosdatabase:Benfica#1904@creproject.database.windows.net/apicrev4?driver=ODBC+Driver+17+for+SQL+Server'
db = SQLAlchemy(app)

app.app_context().push()


class Tipoutilizadores(db.Model):
    idTipoUtilizador = db.Column(db.Integer, primary_key=True)
    nomeTipoUtilizador = db.Column(db.String(80), nullable=False)
    codigoTipoUtilizador = db.Column(db.String(80), default="")
    utilizadores = db.relationship('Utilizadores', backref='tipoutilizadores')


class Utilizadores(db.Model):
    idUtilizador = db.Column(db.Integer, primary_key=True)
    nomeUtilizador = db.Column(db.String(80), nullable=False)
    emailUtilizador = db.Column(db.String(20), unique=True, nullable=False)
    passwordUtilizador = db.Column(db.String(80), nullable=False)
    data_registo_Utilizador = db.Column(db.DateTime,default="")
    data_ultima_entrada_Utilizador = db.Column(db.DateTime,default="")
    telefoneUtilizador = db.Column(db.String(80),default="")
    telemovelUtilizador = db.Column(db.String(80),default="")
    idtipoUtilizador = db.Column(db.Integer, db.ForeignKey('tipoutilizadores.idTipoUtilizador'))


class Clientes(db.Model):
    idCliente = db.Column(db.Integer, primary_key=True)
    nomeCliente = db.Column(db.String(80), nullable=False)
    emailCliente = db.Column(db.String(20), unique=True, nullable=False)
    passwordCliente = db.Column(db.String(80), nullable=False)
    data_registo_Cliente = db.Column(db.DateTime,default="")
    data_ultima_entrada_Cliente = db.Column(db.DateTime,default="")
    telefoneCliente = db.Column(db.String(80),default="")
    telemovelCliente = db.Column(db.String(80),default="")
    nifCliente = db.Column(db.String(80),default="")
    moradaCliente = db.Column(db.String(80),default="")
    codigopostalCliente = db.Column(db.String(80),default="")
    cidadeCliente = db.Column(db.String(80),default="")



class Categorias(db.Model):
    idCategoria = db.Column(db.Integer, primary_key=True)
    nomeCategoria = db.Column(db.String(80), unique=True, nullable=False)
    produtos = db.relationship('Produtos', backref='categorias')
    subcategorias = db.relationship('Subcategorias', backref='categorias')

class Subcategorias(db.Model):
    idSubcategoria = db.Column(db.Integer, primary_key=True)
    nomeSubcategoria = db.Column(db.String(80), unique=True, nullable=False)
    produtos = db.relationship('Produtos', backref='subcategorias')
    idCategoria = db.Column(db.Integer, db.ForeignKey('categorias.idCategoria'))

class Produtos(db.Model):
    idProduto = db.Column(db.Integer, primary_key=True)
    nomeProduto = db.Column(db.String(20),default="")
    descricaoProduto = db.Column(db.String(80), default="")
    imagemProduto = db.Column(db.String, default="")
    corProduto = db.Column(db.String(20), default="")
    precoProduto = db.Column(db.Float)
    tipoProduto = db.Column(db.String(20), default="")  ### Interior ou exterior
    especieProduto = db.Column(db.String(20), default="")
    materialProduto = db.Column(db.String, default="")
    tamanhoProduto = db.Column(db.String, default="")
    quantidadeProduto = db.Column(db.Integer)
    marcaProduto = db.Column(db.String, default="")
    referenciaProduto = db.Column(db.String, default="")
    idcategoria = db.Column(db.Integer, db.ForeignKey('categorias.idCategoria'))
    idsubcategoria = db.Column(db.Integer, db.ForeignKey('subcategorias.idSubcategoria'))
    inventarios = db.relationship('Inventarios', backref='produtos')
    galeria_imagens = db.relationship('Galeria_imagens', backref='produtos')


class Inventarios(db.Model):
    idInventario = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    dataEntrada = db.Column(db.DateTime)
    fornecedor = db.Column(db.String(20),default="")
    idproduto = db.Column(db.Integer, db.ForeignKey('produtos.idProduto'))


class Vendas(db.Model):
    idVenda = db.Column(db.Integer, primary_key=True)
    idProduto = db.Column(db.Integer, nullable=False)
    idCliente= db.Column(db.Integer, nullable=False)
    quantidade= db.Column(db.Integer, nullable=False)
    precototal= db.Column(db.Float, nullable=False)
    iva = db.Column(db.Integer,default="")
    dataVenda = db.Column(db.DateTime)
    nomeEntrega = db.Column(db.String(80),default="")
    moradaEntrega = db.Column(db.String(80),default="")
    nifEntrega = db.Column(db.String(20),default="")
    codigopostalEntrega = db.Column(db.String(80),default="")
    cidadeEntrega = db.Column(db.String(80),default="")

class Carrinho(db.Model):
    idCarrinho = db.Column(db.Integer, primary_key=True)
    idProduto = db.Column(db.Integer, nullable=False)
    idCliente= db.Column(db.Integer, nullable=False)
    quantidade= db.Column(db.Integer, nullable=False)
    precoUnitario = db.Column(db.Float, nullable=False)
    precoTotal= db.Column(db.Float, nullable=False)
    

class Produto_relacionado(db.Model):
    idTabela = db.Column(db.Integer, primary_key=True)
    idProduto = db.Column(db.Integer, nullable=False)
    idProduto_relacionado = db.Column(db.Integer)

class Galeria_imagens(db.Model):
    idGaleria = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String)
    idproduto = db.Column(db.Integer, db.ForeignKey('produtos.idProduto'))



class Conta_bancaria(db.Model):
    idConta_bancaria = db.Column(db.Integer, primary_key=True)
    numeroCartao = db.Column(db.String(80), unique=True, nullable=False)
    ccv = db.Column(db.Integer)
    saldo = db.Column(db.Float)


class Desafio(db.Model):
    idDesafio = db.Column(db.Integer, primary_key=True)
    imagemProduto = db.Column(db.String)
    opcao1=db.Column(db.String)
    opcao2=db.Column(db.String)
    opcao3=db.Column(db.String)
    opcao4=db.Column(db.String)
    dataDesafio=db.Column(db.String)


class Resposta(db.Model):
    idResposta = db.Column(db.Integer, primary_key=True)
    respostaCliente = db.Column(db.String)
    emailCliente= db.Column(db.Integer, nullable=False)
    idDesafio= db.Column(db.Integer, nullable=False)
    nota=db.Column(db.String)
    imagemProduto = db.Column(db.String)



class Fotos(db.Model):
    idFoto = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.String)
    idCliente= db.Column(db.Integer)


class Respostafotos(db.Model):
    idRespostafotos = db.Column(db.Integer, primary_key=True)
    idCliente = db.Column(db.Integer)
    resposta= db.Column(db.String)
    idFoto=db.Column(db.Integer)