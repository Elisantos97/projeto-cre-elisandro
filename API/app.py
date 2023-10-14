from basedados import app, db, Categorias,Subcategorias,Produtos,Inventarios,Vendas,Carrinho,Produto_relacionado,Galeria_imagens,Tipoutilizadores,Utilizadores,Clientes,Conta_bancaria,Desafio,Resposta,Fotos,Respostafotos
from datetime import datetime
from flask import Flask, jsonify, request, redirect, url_for, render_template, make_response, Blueprint
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO

#api_gestao_utilizadores = Blueprint('api_gestao_utilizadores', __name__)

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://eli_santosdatabase:Benfica#1904@creproject.database.windows.net/apicrev4?driver=ODBC+Driver+17+for+SQL+Server'


db.init_app(app)



@app.route("/",methods=['GET'])
def home():


    return "Bem Vindo à página"





################## Teste #####################################
## criar

@app.route('/utilizadores',methods=['POST'])
def adicionar_utilizadores():
    
    novo_utilizador = request.get_json()

    tipoUtilizador=novo_utilizador.get('tipoUtilizador')
    


    tipoutil = Tipoutilizadores.query.filter_by(nomeTipoUtilizador=tipoUtilizador).first()

    print(tipoutil)


    utilizador = Utilizadores(nomeUtilizador=novo_utilizador.get('nomeUtilizador'), emailUtilizador=novo_utilizador.get('emailUtilizador'), \
                              passwordUtilizador=novo_utilizador.get('passwordUtilizador'), tipoutilizadores=tipoutil,\
                              telefoneUtilizador=novo_utilizador.get('telefoneUtilizador'), telemovelUtilizador=novo_utilizador.get('telemovelUtilizador'),\
                             data_registo_Utilizador=datetime.now(), data_ultima_entrada_Utilizador=datetime.now())
                             
                             


    db.session.add(utilizador)
    db.session.commit()



    return redirect(url_for("obter_utilizadores"))



### Consultar todos

@app.route('/utilizadores', methods=['GET'])
def obter_utilizadores():

    lista_utilizadores=[]

    for utilizador in Utilizadores.query.all():
        lista_utilizadores.append({"idUtilizador":utilizador.idUtilizador, "nomeUtilizador":utilizador.nomeUtilizador, "emailUtilizador":utilizador.emailUtilizador, \
                              "passwordUtilizador":utilizador.passwordUtilizador, "idtipoUtilizador":utilizador.idtipoUtilizador, \
                              "telefoneUtilizador":12345, "telemovelUtilizador":213456, \
                              "data_registo_Utilizador":utilizador.data_registo_Utilizador, "data_ultima_entrada_Utilizador":utilizador.data_ultima_entrada_Utilizador})


    return jsonify(lista_utilizadores)


## Consultar por id


@app.route('/utilizadores/<int:id>',methods=['GET'])
def obter_utilizadores_por_id(id):

        for utilizador in Utilizadores.query.filter_by(idUtilizador=id).all():
            
            
            return jsonify({"idUtilizador":utilizador.idUtilizador, "nomeUtilizador":utilizador.nomeUtilizador, "emailUtilizador":utilizador.emailUtilizador, \
                              "passwordUtilizador":utilizador.passwordUtilizador, "idtipoUtilizador":utilizador.idtipoUtilizador, \
                              "telefoneUtilizador": 123456578, "telemovelUtilizador": 123456, \
                              "data_registo_Utilizador":utilizador.data_registo_Utilizador, "data_ultima_entrada_Utilizador":utilizador.data_ultima_entrada_Utilizador})



## Consultar por id


@app.route('/utilizadores/<tipo>',methods=['GET'])
def obter_utilizadores_por_categoria(tipo):
        
        lista_utilizadores=[]

        for utilizador in Utilizadores.query.filter_by(tipoUtilizador=tipo).all():  ### Ver a melhor forma de lidar com letras maiúsculas
            
            lista_utilizadores.append({"idUtilizador":utilizador.idUtilizador, "nomeUtilizador":utilizador.nomeUtilizador, "emailUtilizador":utilizador.emailUtilizador, \
                              "passwordUtilizador":utilizador.passwordUtilizador, "idtipoUtilizador":utilizador.idtipoUtilizador, \
                              "telefoneUtilizador":utilizador.telefoneUtilizador, "telemovelUtilizador":utilizador.telemovelUtilizador, \
                              "data_registo_Utilizador":utilizador.data_registo_Utilizador, "data_ultima_entrada_Utilizador":utilizador.data_ultima_entrada_Utilizador})
            
        return jsonify(lista_utilizadores)





## Editar por id

@app.route('/utilizadores/<int:id>',methods=['PUT'])
def editar_utilizadores_por_id(id):
    
    utilizador = Utilizadores.query.get(id)

    utilizador_alterado = request.get_json()

    utilizador.nomeUtilizador = utilizador_alterado.get('nomeUtilizador')
    utilizador.emailUtilizador = utilizador_alterado.get('emailUtilizador')
    utilizador.passwordUtilizador = utilizador.passwordUtilizador
    utilizador.idtipoUtilizador = utilizador_alterado.get('idtipoUtilizador')
    utilizador.telefoneUtilizador = 1234
    utilizador.telemovelUtilizador = 12324
    utilizador.data_registo_Utilizador = utilizador.data_registo_Utilizador
    utilizador.data_ultima_entrada_Utilizador = utilizador.data_ultima_entrada_Utilizador

    print(utilizador)



    db.session.commit()


    return redirect(url_for("obter_utilizadores"))

## Editar apenas determinado campo por email

# @app.route('/utilizadores/<int:id>',methods=['PATCH'])
# def update_utilizadores_por_email(id):
    
#     utilizador = Utilizadores.query.filter_by(idUtilizador=id).first()

#     #utilizador.data_ultima_entrada_Utilizador = datetime.now()


#     utilizador.update()

#     # utilizador.verified = True

#     # db.session.commit()
    
#     # print(utilizador.emailUtilizador)

#     return redirect(url_for("obter_utilizadores"))



## Apagar por id

@app.route('/utilizadores/<int:id>',methods=['DELETE'])
def apagar_utilizador_por_id(id):

    utilizador = Utilizadores.query.get(id)
    
    db.session.delete(utilizador)
    db.session.commit()

    return redirect(url_for("obter_utilizadores"))



################################### API TIPO UTILIZADORES ############################################3


@app.route('/tipoutilizadores',methods=['POST'])
def adicionar_tipoutilizadores():
    
    novo_tipo_util = request.get_json()


    tipoutilizador = Tipoutilizadores(nomeTipoUtilizador=novo_tipo_util.get('nomeTipoUtilizador'), codigoTipoUtilizador=novo_tipo_util.get('codigoTipoUtilizador'))
                             
                             


    db.session.add(tipoutilizador)
    db.session.commit()



    return redirect(url_for("obter_tipoutilizadores"))



### Consultar todos

@app.route('/tipoutilizadores', methods=['GET'])
def obter_tipoutilizadores():

    lista_tipoutilizadores=[]

    for tipoutilizador in Tipoutilizadores.query.all():
        lista_tipoutilizadores.append({"idTipoUtilizador":tipoutilizador.idTipoUtilizador, "nomeTipoUtilizador":tipoutilizador.nomeTipoUtilizador, "codigoTipoUtilizador":tipoutilizador.codigoTipoUtilizador})


    return jsonify(lista_tipoutilizadores)


## Consultar por id


@app.route('/tipoutilizadores/<int:id>',methods=['GET'])
def obter_tipoutilizadores_por_id(id):

        for tipoutilizador in Tipoutilizadores.query.filter_by(idTipoUtilizador=id).all():
            
            
            return jsonify({"idTipoUtilizador":tipoutilizador.idTipoUtilizador, "nomeTipoUtilizador":tipoutilizador.nomeTipoUtilizador, "codigoTipoUtilizador":tipoutilizador.codigoTipoUtilizador})



## Consultar por id


@app.route('/tipoutilizadores/<nome>',methods=['GET'])
def obter_tipoutilizadores_por_nome(nome):
        
        lista_tipoutilizadores=[]

        for tipoutilizador in Tipoutilizadores.query.filter_by(nomeTipoUtilizador=nome).all():  ### Ver a melhor forma de lidar com letras maiúsculas
            
            lista_tipoutilizadores.append({"idTipoUtilizador":tipoutilizador.idTipoUtilizador, "nomeTipoUtilizador":tipoutilizador.nomeTipoUtilizador, "codigoTipoUtilizador":tipoutilizador.codigoTipoUtilizador})
            
        return jsonify(lista_tipoutilizadores)





## Editar por id

@app.route('/tipoutilizadores/<int:id>',methods=['PUT'])
def editar_tipoutilizadores_por_id(id):
    
    tipoutilizador = Tipoutilizadores.query.get(id)

    tipoutilizador_alterado = request.get_json()

    tipoutilizador.nomeTipoUtilizador = tipoutilizador_alterado.get('nomeTipoUtilizador')
    tipoutilizador.codigoTipoUtilizador = tipoutilizador_alterado.get('codigoTipoUtilizador')


    db.session.commit()


    return redirect(url_for("obter_tipoutilizadores"))




## Apagar por id

@app.route('/tipoutilizadores/<int:id>',methods=['DELETE'])
def apagar_tipoutilizador_por_id(id):

    tipoutilizador = Tipoutilizadores.query.get(id)
    
    db.session.delete(tipoutilizador)
    db.session.commit()

    return redirect(url_for("obter_tipoutilizadores"))



@app.route('/produtos',methods=['POST'])
def adicionar_produtos():
    
    novo_produto = request.get_json()

    categoriaProduto=novo_produto.get('categoriaProduto')
    subcategoriaProduto=novo_produto.get('subcategoriaProduto')
    


    categoriaproduto = Categorias.query.filter_by(nomeCategoria=categoriaProduto).first()
    subcategoriaproduto = Subcategorias.query.filter_by(nomeSubcategoria=subcategoriaProduto).first()



    produto = Produtos(nomeProduto=novo_produto.get('nomeProduto'), categorias=categoriaproduto, subcategorias=subcategoriaproduto, \
                       descricaoProduto=novo_produto.get('descricaoProduto'), imagemProduto=novo_produto.get('imagemProduto'), \
                        corProduto=novo_produto.get('corProduto'), precoProduto=novo_produto.get('precoProduto'), \
                   tipoProduto=novo_produto.get('tipoProduto'), especieProduto=novo_produto.get('especieProduto'), \
                    materialProduto=novo_produto.get('materialProduto'), tamanhoProduto=novo_produto.get('tamanhoProduto'), \
                        quantidadeProduto=novo_produto.get('quantidadeProduto'), marcaProduto=novo_produto.get('marcaProduto'), referenciaProduto=novo_produto.get('referenciaProduto'))


    db.session.add(produto)
    db.session.commit()

    ultimo_produto = Produtos.query.order_by(Produtos.idProduto.desc()).first()

    for produto in Produtos.query.all():
        if ultimo_produto.referenciaProduto == produto.referenciaProduto and ultimo_produto.idProduto!=produto.idProduto:
            produto_relacionado1=Produto_relacionado(idProduto=ultimo_produto.idProduto, idProduto_relacionado=produto.idProduto)
            produto_relacionado2=Produto_relacionado(idProduto=produto.idProduto, idProduto_relacionado=ultimo_produto.idProduto)


            db.session.add(produto_relacionado1)
            db.session.add(produto_relacionado2)
            db.session.commit()


    return redirect(url_for("obter_produtos"))



### Consultar todos

@app.route('/produtos', methods=['GET'])
def obter_produtos():

    lista_produtos=[]

    for produto in Produtos.query.all():
        lista_produtos.append({"idProduto":produto.idProduto, "nomeProduto":produto.nomeProduto, "idcategoria":produto.idcategoria, "idsubcategoria":produto.idsubcategoria, "descricaoProduto":produto.descricaoProduto, \
                              "imagemProduto":produto.imagemProduto, "corProduto":produto.corProduto, "precoProduto":produto.precoProduto, "tipoProduto":produto.tipoProduto, \
                                "especieProduto":produto.especieProduto, "materialProduto":produto.materialProduto, "tamanhoProduto":produto.tamanhoProduto, \
                                    "quantidadeProduto":produto.quantidadeProduto, "marcaProduto":produto.marcaProduto, "referenciaProduto":produto.referenciaProduto})



    return jsonify(lista_produtos)


# ## Consultar por id


@app.route('/produtos/<int:id>',methods=['GET'])
def obter_produtos_por_id(id):

        for produto in Produtos.query.filter_by(idProduto=id).all():
            
            return jsonify({"idProduto":produto.idProduto, "nomeProduto":produto.nomeProduto, "idcategoria":produto.idcategoria, "idsubcategoria":produto.idsubcategoria, "descricaoProduto":produto.descricaoProduto, \
                              "imagemProduto":produto.imagemProduto, "corProduto":produto.corProduto, "precoProduto":produto.precoProduto, "tipoProduto":produto.tipoProduto, \
                                "especieProduto":produto.especieProduto, "materialProduto":produto.materialProduto, "tamanhoProduto":produto.tamanhoProduto, \
                                    "quantidadeProduto":produto.quantidadeProduto, "marcaProduto":produto.marcaProduto, "referenciaProduto":produto.referenciaProduto})



# ## Consultar por subcategoria


@app.route('/produtos/subcategoria/<nome>',methods=['GET'])
def obter_produtos_por_subcategoria(nome):
        
        lista_produtos=[]

        subcategoria = Subcategorias.query.filter_by(nomeSubcategoria=nome).first()

        for produto in Produtos.query.filter_by(idsubcategoria=subcategoria.idSubcategoria).all():  ### Ver a melhor forma de lidar com letras maiúsculas
            
            lista_produtos.append({"idProduto":produto.idProduto, "nomeProduto":produto.nomeProduto, "idcategoria":produto.idcategoria, "idsubcategoria":produto.idsubcategoria, "descricaoProduto":produto.descricaoProduto, \
                              "imagemProduto":produto.imagemProduto, "corProduto":produto.corProduto, "precoProduto":produto.precoProduto, "tipoProduto":produto.tipoProduto, \
                                "especieProduto":produto.especieProduto, "materialProduto":produto.materialProduto, "tamanhoProduto":produto.tamanhoProduto, \
                                    "quantidadeProduto":produto.quantidadeProduto, "marcaProduto":produto.marcaProduto, "referenciaProduto":produto.referenciaProduto})

        return jsonify(lista_produtos)

@app.route('/produtos/<nome>',methods=['GET'])
def obter_produtos_por_nome(nome):
        
        lista_produtos=[]

        for produto in Produtos.query.filter_by(nomeProduto=nome).all():  ### Ver a melhor forma de lidar com letras maiúsculas
            
            lista_produtos.append({"idProduto":produto.idProduto, "nomeProduto":produto.nomeProduto, "idcategoria":produto.idcategoria, "idsubcategoria":produto.idsubcategoria, "descricaoProduto":produto.descricaoProduto, \
                              "imagemProduto":produto.imagemProduto, "corProduto":produto.corProduto, "precoProduto":produto.precoProduto, "tipoProduto":produto.tipoProduto, \
                                "especieProduto":produto.especieProduto, "materialProduto":produto.materialProduto, "tamanhoProduto":produto.tamanhoProduto, \
                                    "quantidadeProduto":produto.quantidadeProduto, "marcaProduto":produto.marcaProduto, "referenciaProduto":produto.referenciaProduto})

        return jsonify(lista_produtos)


# ## Consultar por categoria


@app.route('/produtos/categoria/<nome>',methods=['GET'])
def obter_produtos_por_categoria(nome):
        
        lista_produtos=[]

        categoria = Categorias.query.filter_by(nomeCategoria=nome).first()

        for produto in Produtos.query.filter_by(idcategoria=categoria.idCategoria).all():  ### Ver a melhor forma de lidar com letras maiúsculas
            
            lista_produtos.append({"idProduto":produto.idProduto, "nomeProduto":produto.nomeProduto, "idcategoria":produto.idcategoria, "idsubcategoria":produto.idsubcategoria, "descricaoProduto":produto.descricaoProduto, \
                              "imagemProduto":produto.imagemProduto, "corProduto":produto.corProduto, "precoProduto":produto.precoProduto, "tipoProduto":produto.tipoProduto, \
                                "especieProduto":produto.especieProduto, "materialProduto":produto.materialProduto, "tamanhoProduto":produto.tamanhoProduto, \
                                    "quantidadeProduto":produto.quantidadeProduto, "marcaProduto":produto.marcaProduto, "referenciaProduto":produto.referenciaProduto})

        return jsonify(lista_produtos)

# ## Editar por id

@app.route('/produtos/<int:id>',methods=['PUT'])
def editar_produtos_por_id(id):
    
    produto = Produtos.query.get(id)

    produto_alterado = request.get_json()

    produto.nomeProduto = produto_alterado.get('nomeProduto')
    produto.idcategoria = produto_alterado.get('idcategoria')
    produto.idsubcategoria = produto_alterado.get('idsubcategoria')
    produto.descricaoProduto = produto_alterado.get('descricaoProduto')
    produto.imagemProduto = produto_alterado.get('imagemProduto')
    produto.corProduto = produto_alterado.get('corProduto')
    produto.precoProduto = produto_alterado.get('precoProduto')
    produto.tipoProduto = produto_alterado.get('tipoProduto')
    produto.especieProduto = produto_alterado.get('especieProduto')
    produto.materialProduto = produto_alterado.get('materialProduto')
    produto.tamanhoProduto = produto_alterado.get('tamanhoProduto')
    produto.quantidadeProduto = produto_alterado.get('quantidadeProduto')
    produto.marcaProduto = produto_alterado.get('marcaProduto')
    produto.referenciaProduto = produto_alterado.get('referenciaProduto')


    db.session.commit()

    print(produto_alterado)


    return redirect(url_for("obter_produtos"))


# ## Apagar por id


@app.route('/produtos/<int:id>',methods=['PATCH'])
def editar_quantidade(id):



    produto_alterado = request.get_json()


    produto = Produtos.query.get(id)

    produto.quantidadeProduto = produto_alterado.get('quantidadeProduto')
    

    produto.verified = True
    db.session.commit()

   
    return redirect(url_for("obter_produtos"))



@app.route('/produtos/<int:id>',methods=['DELETE'])
def apagar_produto_por_id(id):

    produto = Produtos.query.get(id)

    for prod_relacionado in Produto_relacionado.query.all():

        if prod_relacionado.idProduto == id or prod_relacionado.idProduto_relacionado == id:

            db.session.delete(prod_relacionado)
            db.session.commit()
             


    
    
    db.session.delete(produto)
    db.session.commit()



    return redirect(url_for("obter_produtos"))



################################### API CATEGORIAS ############################################3


@app.route('/categorias',methods=['POST'])
def adicionar_categorias():
    
    nova_categoria = request.get_json()


    categoria = Categorias(nomeCategoria=nova_categoria.get('nomeCategoria'))
                             
                             
    db.session.add(categoria)
    db.session.commit()



    return redirect(url_for("obter_categorias"))



# ### Consultar todos

@app.route('/categorias', methods=['GET'])
def obter_categorias():

    lista_categorias=[]

    for categoria in Categorias.query.all():
        lista_categorias.append({"idCategoria":categoria.idCategoria, "nomeCategoria":categoria.nomeCategoria})


    return jsonify(lista_categorias)


## Consultar por id


@app.route('/categorias/<int:id>',methods=['GET'])
def obter_categorias_por_id(id):

        for categoria in Categorias.query.filter_by(idCategoria=id).all():
            
            
            return jsonify({"idCategoria":categoria.idCategoria, "nomeCategoria":categoria.nomeCategoria})



## Consultar por id


@app.route('/categorias/<nome>',methods=['GET'])
def obter_categorias_por_nome(nome):
        
        lista_categorias=[]

        for categoria in Categorias.query.filter_by(nomeCategoria=nome).all():  ### Ver a melhor forma de lidar com letras maiúsculas
            
            lista_categorias.append({"idCategoria":categoria.idCategoria, "nomeCategoria":categoria.nomeCategoria})
            
        return jsonify(lista_categorias)





# ## Editar por id

@app.route('/categorias/<int:id>',methods=['PUT'])
def editar_categorias_por_id(id):
    
    categoria = Categorias.query.get(id)

    categoria_alterada = request.get_json()

    categoria.nomeCategoria = categoria_alterada.get('nomeCategoria')

    db.session.commit()


    return redirect(url_for("obter_categorias"))




# ## Apagar por id

@app.route('/categorias/<int:id>',methods=['DELETE'])
def apagar_categoria_por_id(id):

    categoria = Categorias.query.get(id)
    
    db.session.delete(categoria)
    db.session.commit()

    return redirect(url_for("obter_categorias"))


# ################################### API SUBCATEGORIAS ############################################3


@app.route('/subcategorias',methods=['POST'])
def adicionar_subcategorias():
    
    nova_subcategoria = request.get_json()

    nomecategoria=nova_subcategoria.get('categoria')
    


    subcateg = Categorias.query.filter_by(nomeCategoria=nomecategoria).first()



    subcategoria = Subcategorias(nomeSubcategoria=nova_subcategoria.get('nomeSubcategoria'), categorias = subcateg)

    db.session.add(subcategoria)
    db.session.commit()



    return redirect(url_for("obter_subcategorias"))



### Consultar todos

@app.route('/subcategorias', methods=['GET'])
def obter_subcategorias():

    lista_subcategorias=[]

    for subcategoria in Subcategorias.query.all():
        lista_subcategorias.append({"idSubcategoria":subcategoria.idSubcategoria, "nomeSubcategoria":subcategoria.nomeSubcategoria, "idCategoria":subcategoria.idCategoria})


    return jsonify(lista_subcategorias)


## Consultar por id


@app.route('/subcategorias/<int:id>',methods=['GET'])
def obter_subcategorias_por_id(id):

        for subcategoria in Subcategorias.query.filter_by(idSubcategoria=id).all():
            
            
            return jsonify({"idSubcategoria":subcategoria.idSubcategoria, "nomeSubcategoria":subcategoria.nomeSubcategoria, "idCategoria":subcategoria.idCategoria})



## Consultar por id


# @app.route('/subcategorias/<categ>',methods=['GET'])
# def obter_subcategorias_por_categoria(categ):
        
#         lista_subcategorias=[]

#         for subcategoria in Subcategorias.query.filter_by(tipoUtilizador=categ).all():  ### Ver a melhor forma de lidar com letras maiúsculas
            
#             lista_subcategorias.append({"idSubcategoria":subcategoria.idSubcategoria, "nomeSubcategoria":subcategoria.nomeSubcategoria, "idCategoria":subcategoria.idCategoria})
            
#         return jsonify(lista_subcategorias)





## Editar por id

@app.route('/subcategorias/<int:id>',methods=['PUT'])
def editar_subcategorias_por_id(id):
    
    subcategoria = Subcategorias.query.get(id)

    subcategoria_alterada = request.get_json()

    subcategoria.nomeSubcategoria = subcategoria_alterada.get('nomeSubcategoria')
    subcategoria.idCategoria = subcategoria_alterada.get('idCategoria')


    db.session.commit()

    return redirect(url_for("obter_subcategorias"))



## Apagar por id

@app.route('/subcategorias/<int:id>',methods=['DELETE'])
def apagar_subcategoria_por_id(id):

    subcategoria = Subcategorias.query.get(id)
    
    db.session.delete(subcategoria)
    db.session.commit()

    return redirect(url_for("obter_subcategorias"))




################################### API INVENTARIOS ############################################3
@app.route('/inventarios',methods=['POST'])
def adicionar_inventarios():
    
    novo_inventario = request.get_json()

    Produto=novo_inventario.get('produto')

    produto = Produtos.query.filter_by(idProduto=Produto).first()


    inventario = Inventarios(quantidade=novo_inventario.get('quantidade'), dataEntrada=datetime.now(), fornecedor=novo_inventario.get('fornecedor'), produtos=produto)


    db.session.add(inventario)
    db.session.commit()


    return redirect(url_for("obter_inventarios"))



### Consultar todos

@app.route('/inventarios', methods=['GET'])
def obter_inventarios():

    lista_inventarios=[]

    for inventario in Inventarios.query.all():
        lista_inventarios.append({"idInventario":inventario.idInventario, "quantidade":inventario.quantidade, "dataEntrada":inventario.dataEntrada, \
                              "fornecedor":inventario.fornecedor, "idproduto":inventario.idproduto})


    return jsonify(lista_inventarios)


# # ## Consultar por id


@app.route('/inventarios/<int:id>',methods=['GET'])
def obter_inventario_por_id(id):

        for inventario in Inventarios.query.filter_by(idInventario=id).all():
            
            return jsonify({"idInventario":inventario.idInventario, "quantidade":inventario.quantidade, "dataEntrada":inventario.dataEntrada, \
                              "fornecedor":inventario.fornecedor, "idproduto":inventario.idproduto})


## Editar por inventário

@app.route('/inventarios/<int:id>',methods=['PUT'])
def editar_inventario_por_id(id):
    
    inventario = Inventarios.query.get(id)

    inventario_alterado = request.get_json()


    inventario.fornecedor = inventario_alterado.get('fornecedor')
    inventario.quantidade = inventario_alterado.get('quantidade')
    inventario.idproduto=inventario_alterado.get('idproduto')
    inventario.dataEntrada=datetime.now()

    db.session.commit()

    return redirect(url_for("obter_inventarios"))



## Apagar por inventário

@app.route('/inventarios/<int:id>',methods=['DELETE'])
def apagar_inventario_por_id(id):

    inventario = Inventarios.query.get(id)
    
    db.session.delete(inventario)
    db.session.commit()

    return redirect(url_for("obter_inventarios"))


################################### API VENDAS ############################################3
@app.route('/vendas',methods=['POST'])
def adicionar_venda():
    
    nova_venda = request.get_json()

    venda = Vendas(idProduto=nova_venda.get('idProduto'), idCliente=nova_venda.get('idCliente'), quantidade=nova_venda.get('quantidade'), \
                   precototal=nova_venda.get('precototal'), iva=nova_venda.get('iva'), dataVenda=datetime.now(), \
                    nomeEntrega=nova_venda.get('nomeEntrega'), moradaEntrega=nova_venda.get('moradaEntrega'), nifEntrega=nova_venda.get('nifEntrega'), \
                        codigopostalEntrega=nova_venda.get('codigopostalEntrega'), cidadeEntrega=nova_venda.get('cidadeEntrega'))


    db.session.add(venda)
    db.session.commit()


    return redirect(url_for("obter_vendas"))



### Consultar todos

@app.route('/vendas', methods=['GET'])
def obter_vendas():

    lista_vendas=[]

    for venda in Vendas.query.all():
        lista_vendas.append({"idVenda":venda.idVenda, "idProduto":venda.idProduto, "idCliente":venda.idCliente, "quantidade":venda.quantidade, \
                              "precototal":venda.precototal, "iva":venda.iva, "dataVenda":venda.dataVenda, "nomeEntrega":venda.nomeEntrega, \
                                "moradaEntrega":venda.moradaEntrega, "nifEntrega":venda.nifEntrega, "codigopostalEntrega":venda.codigopostalEntrega, "cidadeEntrega":venda.cidadeEntrega})


    return jsonify(lista_vendas)


# # ## Consultar por id


@app.route('/vendas/<int:id>',methods=['GET'])
def obter_venda_por_id(id):

        for venda in Vendas.query.filter_by(idVenda=id).all():


            print(venda.iva + 11.5)
            
            return jsonify({"idVenda":venda.idVenda, "idProduto":venda.idProduto, "idCliente":venda.idCliente, "quantidade":venda.quantidade, \
                              "precototal":venda.precototal, "iva":venda.iva, "dataVenda":venda.dataVenda, "nomeEntrega":venda.nomeEntrega, \
                                "moradaEntrega":venda.moradaEntrega, "nifEntrega":venda.nifEntrega, "codigopostalEntrega":venda.codigopostalEntrega, "cidadeEntrega":venda.cidadeEntrega})



@app.route('/vendas/cliente/<int:id>',methods=['GET'])
def obter_venda_por_idCliente(id):
        
    lista_venda=[]

    for venda in Vendas.query.filter_by(idCliente=id).all():
        lista_venda.append({"idVenda":venda.idVenda, "idProduto":venda.idProduto, "idCliente":venda.idCliente, "quantidade":venda.quantidade, \
                              "precototal":venda.precototal, "iva":venda.iva, "dataVenda":venda.dataVenda, "nomeEntrega":venda.nomeEntrega, \
                                "moradaEntrega":venda.moradaEntrega, "nifEntrega":venda.nifEntrega, "codigopostalEntrega":venda.codigopostalEntrega, "cidadeEntrega":venda.cidadeEntrega})

        
    return jsonify(lista_venda)


################################### API CARRINHO ############################################3
@app.route('/carrinho',methods=['POST'])
def adicionar_carrinho():
    
    nova_carrinho = request.get_json()

    carrinho = Carrinho(idProduto=nova_carrinho.get('idProduto'), idCliente=nova_carrinho.get('idCliente'), quantidade=nova_carrinho.get('quantidade'), \
                   precoUnitario=nova_carrinho.get('precoUnitario'), precoTotal=nova_carrinho.get('precoTotal'))


    db.session.add(carrinho)
    db.session.commit()


    return redirect(url_for("obter_carrinho"))



### Consultar todos

@app.route('/carrinho', methods=['GET'])
def obter_carrinho():

    lista_carrinho=[]

    for carrinho in Carrinho.query.all():
        lista_carrinho.append({"idCarrinho":carrinho.idCarrinho, "idProduto":carrinho.idProduto, "idCliente":carrinho.idCliente, "quantidade":carrinho.quantidade, \
                              "precoUnitario":carrinho.precoUnitario, "precoTotal":carrinho.precoTotal})


    return jsonify(lista_carrinho)


# # ## Consultar por id


@app.route('/carrinho/<int:id>',methods=['GET'])
def obter_carrinho_por_id(id):

    for carrinho in Carrinho.query.filter_by(idCarrinho=id).all():

        
        return jsonify({"idCarrinho":carrinho.idCarrinho, "idProduto":carrinho.idProduto, "idCliente":carrinho.idCliente, "quantidade":carrinho.quantidade, \
                            "precoUnitario":carrinho.precoUnitario, "precoTotal":carrinho.precoTotal})
        

@app.route('/carrinho/cliente/<int:id>',methods=['GET'])
def obter_carrinho_por_idCliente(id):
        
    lista_carrinho=[]

    for carrinho in Carrinho.query.filter_by(idCliente=id).all():
        lista_carrinho.append({"idCarrinho":carrinho.idCarrinho, "idProduto":carrinho.idProduto, "idCliente":carrinho.idCliente, "quantidade":carrinho.quantidade, \
                            "precoUnitario":carrinho.precoUnitario, "precoTotal":carrinho.precoTotal})

        
    return jsonify(lista_carrinho)
        


@app.route('/carrinho/<int:id>',methods=['DELETE'])
def apagar_carrinho_por_id(id):

    carrinho = Carrinho.query.get(id)
    
    db.session.delete(carrinho)
    db.session.commit()

    return redirect(url_for("obter_carrinho"))




################################### API PRODUTO_RELACIONADO ############################################3
@app.route('/produto_relacionado',methods=['POST'])
def adicionar_produto_relacionado():
    
    nova_relacao = request.get_json()

    relacao = Produto_relacionado(idProduto=nova_relacao.get('idProduto'), idProduto_relacionado=nova_relacao.get('idProduto_relacionado'))


    db.session.add(relacao)
    db.session.commit()


    return redirect(url_for("obter_produto_relacionado"))



### Consultar todos

@app.route('/produto_relacionado', methods=['GET'])
def obter_produto_relacionado():

    lista_relacao=[]

    for relacao in Produto_relacionado.query.all():
        lista_relacao.append({"idTabela":relacao.idTabela, "idProduto":relacao.idProduto, "idProduto_relacionado":relacao.idProduto_relacionado})


    return jsonify(lista_relacao)


# # ## Consultar por id


@app.route('/produto_relacionado/<int:id>',methods=['GET'])
def obter_produto_relacionado_por_id(id):

        for relacao in Produto_relacionado.query.filter_by(idTabela=id).all():

            
            return jsonify({"idTabela":relacao.idTabela, "idProduto":relacao.idProduto, "idProduto_relacionado":relacao.idProduto_relacionado})
        

@app.route('/produto_relacionado/produto/<int:id>',methods=['GET'])
def obter_produto_relacionado_por_idproduto(id):
        

        lista_prod_relcionado=[]

        try:

            produto = Produtos.query.filter_by(idProduto=id).first()

            for prod_relacionado in Produto_relacionado.query.filter_by(idProduto=produto.idProduto).all():  ### Ver a melhor forma de lidar com letras maiúsculas
                
                lista_prod_relcionado.append({"idTabela":prod_relacionado.idTabela, "idProduto":prod_relacionado.idProduto, "idProduto_relacionado":prod_relacionado.idProduto_relacionado})

        except:
             pass

        return jsonify(lista_prod_relcionado)



@app.route('/produto_relacionado/<int:id>',methods=['DELETE'])
def apagar_produto_relacionado_id(id):

    relacao = Produto_relacionado.query.get(id)
    
    db.session.delete(relacao)
    db.session.commit()

    return redirect(url_for("obter_produto_relacionado"))




################################### API IMAGENS ############################################3
@app.route('/imagens',methods=['POST'])
def adicionar_imagens():
    
    nova_imagem = request.get_json()

    Produto=nova_imagem.get('idproduto')

    produto = Produtos.query.filter_by(idProduto=Produto).first()


    imagem = Galeria_imagens(imagem=nova_imagem.get('imagem'), produtos=produto)


    db.session.add(imagem)
    db.session.commit()


    return redirect(url_for("obter_imagens"))



### Consultar todos

@app.route('/imagens', methods=['GET'])
def obter_imagens():

    lista_imagens=[]

    for imagem in Galeria_imagens.query.all():
        lista_imagens.append({"idGaleria":imagem.idGaleria, "imagem":imagem.imagem, "idproduto":imagem.idproduto})


    return jsonify(lista_imagens)


# # ## Consultar por id


@app.route('/imagens/<int:id>',methods=['GET'])
def obter_imagem_por_id(id):

        for imagem in Galeria_imagens.query.filter_by(idGaleria=id).all():
            
            return jsonify({"idGaleria":imagem.idGaleria, "imagem":imagem.imagem, "idproduto":imagem.idproduto})
        

@app.route('/imagens/produto/<int:id>',methods=['GET'])
def obter_imagens_por_produto(id):
        
        lista_imagens=[]

        try:

            produto = Produtos.query.filter_by(idProduto=id).first()

            for imagem in Galeria_imagens.query.filter_by(idproduto=produto.idProduto).all():  ### Ver a melhor forma de lidar com letras maiúsculas
                
                lista_imagens.append({"idGaleria":imagem.idGaleria, "imagem":imagem.imagem, "idproduto":imagem.idproduto})

        except:
             pass

        return jsonify(lista_imagens)


@app.route('/imagens/<int:id>',methods=['DELETE'])
def apagar_imagem_por_id(id):

    imagem = Galeria_imagens.query.get(id)
    
    db.session.delete(imagem)
    db.session.commit()

    return redirect(url_for("obter_imagens"))



@app.route('/soma_produto/<int:id>', methods=['GET'])
def soma_produto(id):
    count = Carrinho.query.filter_by(idCliente=id).count()

    # Return the count as JSON response
    response_data = {'count': count}
    return str(count)


@app.route('/clientes',methods=['POST'])
def adicionar_clientes():
    
    novo_cliente = request.get_json()

    print(novo_cliente)


    cliente = Clientes(nomeCliente=novo_cliente.get('nomeCliente'), emailCliente=novo_cliente.get('emailCliente'), \
                              passwordCliente=novo_cliente.get('passwordCliente'), \
                              telefoneCliente=novo_cliente.get('telefoneCliente'), telemovelCliente=novo_cliente.get('telemovelCliente'),\
                             data_registo_Cliente=datetime.now(), data_ultima_entrada_Cliente=datetime.now(), nifCliente=novo_cliente.get('nifCliente'), \
                                moradaCliente=novo_cliente.get('moradaCliente'),codigopostalCliente=novo_cliente.get('codigopostalCliente'), \
                                    cidadeCliente=novo_cliente.get('cidadeCliente'))
                             
                             


    db.session.add(cliente)
    db.session.commit()



    return redirect(url_for("obter_clientes"))



### Consultar todos

@app.route('/clientes', methods=['GET'])
def obter_clientes():

    lista_clientes=[]

    for cliente in Clientes.query.all():
        lista_clientes.append({"idCliente":cliente.idCliente, "nomeCliente":cliente.nomeCliente, "emailCliente":cliente.emailCliente, \
                              "passwordCliente":cliente.passwordCliente, "telefoneCliente":cliente.telefoneCliente, \
                              "telemovelCliente":cliente.telemovelCliente, "nifCliente":cliente.nifCliente,\
                              "data_registo_Cliente":cliente.data_registo_Cliente, "data_ultima_entrada_Cliente":cliente.data_ultima_entrada_Cliente, \
                                "moradaCliente":cliente.moradaCliente, "codigopostalCliente":cliente.codigopostalCliente, "cidadeCliente":cliente.cidadeCliente})


    return jsonify(lista_clientes)


## Consultar por id


@app.route('/clientes/<int:id>',methods=['GET'])
def obter_clientes_por_id(id):

        for cliente in Clientes.query.filter_by(idCliente=id).all():
            
            
            return jsonify({"idCliente":cliente.idCliente, "nomeCliente":cliente.nomeCliente, "emailCliente":cliente.emailCliente, \
                              "passwordCliente":cliente.passwordCliente, "telefoneCliente":cliente.telefoneCliente, \
                              "telemovelCliente":cliente.telemovelCliente, "nifCliente":cliente.nifCliente,\
                              "data_registo_Cliente":cliente.data_registo_Cliente, "data_ultima_entrada_Cliente":cliente.data_ultima_entrada_Cliente, \
                                "moradaCliente":cliente.moradaCliente, "codigopostalCliente":cliente.codigopostalCliente, "cidadeCliente":cliente.cidadeCliente})



## Editar por id

@app.route('/clientes/<int:id>',methods=['PUT'])
def editar_clientes_por_id(id):
    
    cliente = Clientes.query.filter_by(idCliente=id).first()

    cliente_alterado = request.get_json()

    cliente.nomeCliente = cliente_alterado.get('nomeCliente')
    cliente.emailCliente = cliente_alterado.get('emailCliente')
    cliente.passwordCliente = cliente.passwordCliente
    cliente.telefoneCliente = cliente_alterado.get('telefoneCliente')
    cliente.telemovelCliente = cliente_alterado.get('telemovelCliente')
    cliente.nifCliente = cliente_alterado.get('nifCliente')
    cliente.data_registo_Cliente = cliente_alterado.get('data_registo_Cliente')
    cliente.data_ultima_entrada_Cliente = cliente_alterado.get('data_ultima_entrada_Cliente')
    cliente.moradaCliente = cliente_alterado.get('moradaCliente')
    cliente.codigopostalCliente = cliente_alterado.get('codigopostalCliente')
    cliente.cidadeCliente = cliente_alterado.get('cidadeCliente')



    db.session.commit()


    return redirect(url_for("obter_clientes"))





## Apagar por id

@app.route('/clientes/<int:id>',methods=['DELETE'])
def apagar_cliente_por_id(id):

    cliente = Clientes.query.get(id)
    
    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("obter_clientes"))



@app.route('/alterar/<int:id>',methods=['PATCH'])
def alterar_password(id):
    
    
    cliente = Clientes.query.get(id)

    password = request.get_json()


    cliente.passwordCliente=password.get("passwordCliente")

 

    cliente.verified = True
    db.session.commit()
    return redirect(url_for("obter_clientes"))



################################### API CONTA BANCARIA ############################################3
@app.route('/conta',methods=['POST'])
def conta():
    
    nova_conta = request.get_json()

    conta = Conta_bancaria(numeroCartao=nova_conta.get('numeroCartao'), ccv=nova_conta.get('ccv'),saldo=nova_conta.get('saldo'))


    db.session.add(conta)
    db.session.commit()


    return redirect(url_for("obter_conta"))



### Consultar todos

@app.route('/conta', methods=['GET'])
def obter_conta():

    lista_conta=[]

    for conta in Conta_bancaria.query.all():
        lista_conta.append({"idConta_bancaria":conta.idConta_bancaria, "numeroCartao":conta.numeroCartao, "ccv":conta.ccv, "saldo":conta.saldo})


    return jsonify(lista_conta)


# # ## Consultar por id


@app.route('/conta/<int:id>',methods=['GET'])
def obter_conta_por_id(id):

    for conta in Conta_bancaria.query.filter_by(idConta_bancaria=id).all():

        
        return jsonify({"idConta_bancaria":conta.idConta_bancaria, "numeroCartao":conta.numeroCartao, "ccv":conta.ccv, "saldo":conta.saldo})
        
        


@app.route('/conta/<int:id>',methods=['DELETE'])
def apagar_conta_por_id(id):

    conta = Conta_bancaria.query.get(id)
    
    db.session.delete(conta)
    db.session.commit()

    return redirect(url_for("obter_conta"))


################################### Desafio ############################################
@app.route('/desafio',methods=['POST'])
def desafio():
    
    novo_desafio = request.get_json()

    desafio = Desafio(imagemProduto=novo_desafio.get('imagemProduto'),opcao1=novo_desafio.get('opcao1'), \
                      opcao2=novo_desafio.get('opcao2'), opcao3=novo_desafio.get('opcao3'),opcao4=novo_desafio.get('opcao4'), dataDesafio=novo_desafio.get('dataDesafio'))


    db.session.add(desafio)
    db.session.commit()


    return redirect(url_for("obter_desafio"))



### Consultar todos

@app.route('/desafio', methods=['GET'])
def obter_desafio():

    lista_desafios=[]

    for desafio in Desafio.query.all():
        lista_desafios.append({"idDesafio":desafio.idDesafio, "imagemProduto":desafio.imagemProduto, "opcao1":desafio.opcao1, \
                               "opcao2":desafio.opcao2, "opcao3":desafio.opcao3, "opcao4":desafio.opcao4, "dataDesafio":desafio.dataDesafio})


    return jsonify(lista_desafios)


@app.route('/desafio/<int:id>',methods=['GET'])
def obter_desafio_por_id(id):

        for desafio in Desafio.query.filter_by(idDesafio=id).all():
            
            
            return jsonify({"idDesafio":desafio.idDesafio, "imagemProduto":desafio.imagemProduto, "opcao1":desafio.opcao1, \
                               "opcao2":desafio.opcao2, "opcao3":desafio.opcao3, "opcao4":desafio.opcao4, "dataDesafio":desafio.dataDesafio})



################################### Respostas ############################################


@app.route('/resposta',methods=['POST'])
def resposta():
    
    nova_resposta = request.get_json()

    resposta = Resposta(respostaCliente=nova_resposta.get('respostaCliente'), emailCliente=nova_resposta.get('emailCliente'),idDesafio=nova_resposta.get('idDesafio'), nota=nova_resposta.get('nota'), imagemProduto=nova_resposta.get('imagemProduto'))


    db.session.add(resposta)
    db.session.commit()


    return redirect(url_for("obter_resposta"))



### Consultar todos

@app.route('/resposta', methods=['GET'])
def obter_resposta():

    lista_respostas=[]

    for resposta in Resposta.query.all():
        lista_respostas.append({"idResposta":resposta.idResposta, "respostaCliente":resposta.respostaCliente, "emailCliente":resposta.emailCliente, "idDesafio":resposta.idDesafio, "nota":resposta.nota,"imagemProduto":resposta.imagemProduto})


    return jsonify(lista_respostas)


@app.route('/resposta/<int:id>',methods=['GET'])
def obter_resposta_por_id(id):

        for resposta in Resposta.query.filter_by(idResposta=id).all():
            
            
            return jsonify({"idResposta":resposta.idResposta, "respostaCliente":resposta.respostaCliente, "emailCliente":resposta.emailCliente, "idDesafio":resposta.idDesafio, "nota":resposta.nota, "imagemProduto":resposta.imagemProduto})
        


################################### Desafio ############################################
@app.route('/foto',methods=['POST'])
def foto():
    
    nova_foto = request.get_json()

    fotos = Fotos(foto=nova_foto.get('foto'),idCliente=nova_foto.get('idCliente'))


    db.session.add(fotos)
    db.session.commit()


    return redirect(url_for("obter_fotos"))



### Consultar todos

@app.route('/foto', methods=['GET'])
def obter_fotos():

    lista_fotos=[]

    for fotos in Fotos.query.all():
        lista_fotos.append({"idFoto":fotos.idFoto, "foto":fotos.foto, "idCliente":fotos.idCliente})


    return jsonify(lista_fotos)


@app.route('/foto/<int:id>',methods=['GET'])
def obter_foto_por_id(id):

        for fotos in Fotos.query.filter_by(idFoto=id).all():
            
            
            return jsonify({"idFoto":fotos.idFoto, "foto":fotos.foto, "idCliente":fotos.idCliente})



################################### fotos ############################################


@app.route('/respostafotos',methods=['POST'])
def respostafotos():
    
    nova_foto = request.get_json()

    resposta = Respostafotos(idCliente=nova_foto.get('idCliente'), resposta=nova_foto.get('resposta'),idFoto=nova_foto.get('idFoto'))


    db.session.add(resposta)
    db.session.commit()


    return redirect(url_for("obter_respostafotos"))



### Consultar todos

@app.route('/respostafotos', methods=['GET'])
def obter_respostafotos():

    lista_respostas=[]

    for respostas in Respostafotos.query.all():
        lista_respostas.append({"idRespostafotos":respostas.idRespostafotos, "idCliente":respostas.idCliente, "resposta":respostas.resposta, "idFoto":respostas.idFoto})


    return jsonify(lista_respostas)


@app.route('/respostafotos/<int:id>',methods=['GET'])
def obter_respostafotos_por_id(id):

        for respostas in Respostafotos.query.filter_by(idResposta=id).all():
            
            
            return jsonify({"idRespostafotos":respostas.idRespostafotos, "idCliente":respostas.idCliente, "resposta":respostas.resposta, "idFoto":respostas.idFoto})
        



if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')