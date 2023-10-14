from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
from datetime import datetime
from website import auth
import base64


views = Blueprint('views', __name__)

url='https://elisandroapicre.azurewebsites.net/produtos'
url1='https://elisandroapicre.azurewebsites.net/utilizadores'
url2='https://elisandroapicre.azurewebsites.net/tipoutilizadores'
url3='https://elisandroapicre.azurewebsites.net/clientes'
url4='https://elisandroapicre.azurewebsites.net/categorias'
url5='https://elisandroapicre.azurewebsites.net/subcategorias'
url6='https://elisandroapicre.azurewebsites.net/inventarios'
url7='https://elisandroapicre.azurewebsites.net/produto_relacionado'
url8='https://elisandroapicre.azurewebsites.net/imagens'
url9='https://elisandroapicre.azurewebsites.net/vendas'
url10='https://elisandroapicre.azurewebsites.net/resposta'
url11='https://elisandroapicre.azurewebsites.net/desafio'




######################################################### Gestão utilizadores ########################################################


@views.route('/utilizadores', methods=["GET"])
def utilizadores():

    util = requests.get(url1)
    tipoutil = requests.get(url2)
    utilizadores = util.json()
    tipoutilizadores = tipoutil.json()

    produtos = requests.get(url)
    categ = requests.get(url4)
    subcateg = requests.get(url5)

    # k=0
    # for j in utilizadores:
    #     for i in tipoutil.json():
    #         if i.get('idTipoUtilizador') == j.get('idtipoUtilizador'):
    #             utilizadores[k]["idtipoUtilizador"]=i.get('nomeTipoUtilizador')
    #     k+=1
                   
    # print("tipoutilizadors",tipoutilizadores)


    if "email" in session:
        return render_template('gestao_util.html', utilizadores=utilizadores, tipoutilizadores=tipoutilizadores, categorias=categ.json(), produtos=produtos.json(), subcategorias=subcateg.json())
    
    
    
    
    return redirect(url_for("auth.login"))


@views.route('/inserir_util', methods=["POST"])
def inserir_util():

    if request.method == "POST":

        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        tipo = request.form.get('tipo')

        dados = {"nomeUtilizador": nome, "emailUtilizador": email,"passwordUtilizador": password, "tipoUtilizador": tipo}

        

        api=requests.post(url1, json=dados)

        print(dados)

    return redirect(url_for("views.utilizadores"))


@views.route('/atualizar_util', methods=['GET', 'POST'])
def atualizar_util():

    if request.method == "POST":

        idUtilizador = request.form.get('id')
        nome = request.form.get('nome')
        email = request.form.get('email')
        tipoUtilizador = request.form.get('tipo')

        dados = {"nomeUtilizador": nome,"emailUtilizador": email,"idtipoUtilizador": int(tipoUtilizador)}

        dados1 = {"idUtilizador":idUtilizador, "nomeUtilizador": nome,"emailUtilizador": email,"idtipoUtilizador": int(tipoUtilizador)}

        print("dados atualizados", dados1)

        
        
        
        api=requests.put(url1+'/'+idUtilizador, json=dados)

    return redirect(url_for("views.utilizadores"))


@views.route('/apagar_util/<int:id>', methods=['GET', 'POST'])
def apagar_util(id):

    api = requests.delete(url1+'/'+str(id))

    flash("Produto apagado com sucesso")

    return redirect(url_for("views.utilizadores"))



############# Gestao tipo utilizadores ##################

#obter

@views.route('/tipoutilizadores', methods=["GET"])
def tipoutilizadores():

    tipoutil = requests.get(url2)


    produtos = requests.get(url)
    categ = requests.get(url4)
    subcateg = requests.get(url5)

    return render_template('gestao_tipoutil.html', tipoutilizadores=tipoutil.json(),categorias=categ.json(), produtos=produtos.json(), subcategorias=subcateg.json())


#Adicionar

@views.route('/inserir_tipoutil', methods=["POST"])
def inserir_tipoutil():

    if request.method == "POST":

        nome = request.form.get('nome')
        codigo = request.form.get('codigo')
 

        dados = {"nomeTipoUtilizador": nome, "codigoTipoUtilizador": codigo}

        api=requests.post(url2, json=dados)

    return redirect(url_for("views.tipoutilizadores"))


@views.route('/atualizar_tipoutil', methods=['GET', 'POST'])
def atualizar_tipoutil():

    if request.method == "POST":

        id = request.form.get('id')
        nome = request.form.get('nome')
        codigo = request.form.get('codigo')


        dados = {"nomeTipoUtilizador": nome,"codigoTipoUtilizador": codigo}
        print(dados)
        
        
        api=requests.put(url2+"/"+id, json=dados)

    return redirect(url_for("views.tipoutilizadores"))


@views.route('/apagar_tipoutil/<int:id>', methods=['GET', 'POST'])
def apagar_tipoutil(id):

    api = requests.delete(url2+'/'+str(id))


    return redirect(url_for("views.tipoutilizadores"))



######################################################### Clientes ######################################################

#Gestão utilizadores


@views.route('/clientes', methods=["GET"])
def clientes():

    clientes = requests.get(url3)

    produtos = requests.get(url)
    categ = requests.get(url4)
    subcateg = requests.get(url5)

    return render_template('gestao_clientes.html', clientes=clientes.json(),categorias=categ.json(), produtos=produtos.json(), subcategorias=subcateg.json())#,tipoutilizadores=tipoutil.json())


@views.route('/inserir_cliente', methods=["POST"])
def inserir_cliente():

    if request.method == "POST":
        
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        telefone = request.form.get('telefone')
        telemovel = request.form.get('telemovel')
        nif = request.form.get('nif')
        data_registo_Cliente = datetime.now()

        dados = {"nomeCliente": nome, "emailCliente": email,"passwordCliente": password, "telefoneCliente": telefone, \
                 "telemovelCliente": telemovel, "nifCliente": nif,"data_registo_Cliente": data_registo_Cliente}

        api=requests.post(url3, json=dados)

    return redirect(url_for("views.clientes"))


@views.route('/atualizar_cliente', methods=['GET', 'POST'])
def atualizar_cliente():

    if request.method == "POST":
        
        id = request.form.get('id')
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        telefone = request.form.get('telefone')
        telemovel = request.form.get('telemovel')
        nif = request.form.get('nif')
        data_registo_Cliente = request.form.get('data_registo_Cliente')
        data_ultima_entrada_Cliente = request.form.get('data_ultima_entrada_Cliente')


        dados = {"nomeCliente": nome, "emailCliente": email,"passwordCliente": password, "telefoneCliente": telefone, \
                 "telemovelCliente": telemovel, "nifCliente": nif,"data_registo_Cliente": data_registo_Cliente, "data_ultima_entrada_Cliente": data_ultima_entrada_Cliente}


        api=requests.put(url3+'/'+id, json=dados)

    return redirect(url_for("views.utilizadores"))


@views.route('/apagar_cliente/<int:id>', methods=['GET', 'POST'])
def apagar_cliente(id):

    api = requests.delete(url1+'/'+str(id))

    return redirect(url_for("views.clientes"))


############# CATEGORIAS ##################

#obter

@views.route('/categorias', methods=["GET"])
def categorias():

    produtos = requests.get(url)
    categ = requests.get(url4)
    subcateg = requests.get(url5)

    return render_template('gestao_categorias.html', categorias=categ.json(), produtos=produtos.json(), subcategorias=subcateg.json())


#Adicionar

@views.route('/inserir_categoria', methods=["POST"])
def inserir_categoria():

    if request.method == "POST":

        nome = request.form.get('nome')
 

        dados = {"nomeCategoria": nome}

        api=requests.post(url4, json=dados)

    return redirect(url_for("views.categorias"))


@views.route('/atualizar_categoria', methods=['GET', 'POST'])
def atualizar_categoria():

    if request.method == "POST":

        id = request.form.get('id')
        nome = request.form.get('nome')


        dados = {"nomeCategoria": nome}
        
        api=requests.put(url4+"/"+id, json=dados)

    return redirect(url_for("views.categorias"))


@views.route('/apagar_categoria/<int:id>', methods=['GET', 'POST'])
def apagar_categoria(id):

    api = requests.delete(url4+'/'+str(id))


    return redirect(url_for("views.categorias"))




######################################### GESTAO SUBCATEGORIAS


@views.route('/subcategorias', methods=["GET"])
def subcategorias():

    produtos = requests.get(url)
    subcateg = requests.get(url5)
    Categ = requests.get(url4)
    subcategorias = subcateg.json()
    categorias = Categ.json()


    return render_template('gestao_subcategorias.html', subcategorias=subcategorias, categorias=categorias, produtos=produtos.json())
    
    


@views.route('/inserir_subcategoria', methods=["POST"])
def inserir_subcategoria():

    if request.method == "POST":

        nome = request.form.get('nome')
        categoria = request.form.get('categoria')

        dados = {"nomeSubcategoria": nome, "categoria": categoria}

        api=requests.post(url5, json=dados)


    return redirect(url_for("views.subcategorias"))


@views.route('/atualizar_subcategoria', methods=['GET', 'POST'])
def atualizar_subcategoria():

    if request.method == "POST":

        idSubcategoria = request.form.get('id')
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')

        dados = {"nomeSubcategoria": nome, "idCategoria": int(categoria)}

        dados1 = {"idSubcategoria":idSubcategoria, "nomeSubcategoria": nome, "idCategoria": int(categoria)}

        print("dados atualizados", dados1)

        
        
        
        api=requests.put(url5+'/'+categoria, json=dados)

    return redirect(url_for("views.subcategorias"))


@views.route('/apagar_subcategoria/<int:id>', methods=['GET', 'POST'])
def apagar_subcategoria(id):

    api = requests.delete(url5+'/'+str(id))

    return redirect(url_for("views.subcategorias"))



######################################### GESTAO Produtos #############################


@views.route('/produtos', methods=["GET"])
def produtos():

    prod = requests.get(url)
    subcateg = requests.get(url5)
    categ = requests.get(url4)
    produtos = prod.json()
    subcategorias = subcateg.json()
    categorias = categ.json()


    return render_template('gestao_produtos.html', produtos=produtos, subcategorias=subcategorias, categorias=categorias)


@views.route('/produtos/<int:id>', methods=['GET', 'POST'])
def obter_produto_id(id):

    produto1 = requests.get(url+'/'+str(id))
    produto=produto1.json()

    produtos = requests.get(url)

    subcateg = requests.get(url5)
    categ = requests.get(url4)
    invent = requests.get(url6)
    prod_relacionado=requests.get(url7)
    imagens=requests.get(url8+'/produto/'+str(id))
    vendas = requests.get(url9)
    
    subcategorias = subcateg.json()
    categorias = categ.json()
    inventarios = invent.json()

    lista_inventarios=[]
    soma_inventarios=0
    for inventario in invent.json():
        if produto.get("idProduto")==inventario.get("idproduto"):
            lista_inventarios.append(inventario.get("quantidade"))
    
    soma_inventarios=sum(lista_inventarios)

    lista_vendas=[]
    soma_vendas=0
    for venda in vendas.json():
        print(venda)
        if produto.get("idProduto")==venda.get("idProduto"):
            lista_vendas.append(venda.get("quantidade"))
    
    soma_vendas=sum(lista_vendas)
    print(soma_inventarios)
    print(soma_vendas)

    stock=soma_inventarios-soma_vendas




    return render_template('produto.html', stock=stock, vendas=vendas.json(), imagens=imagens.json(),produto=produto, produtos=produtos.json(), \
                           subcategorias=subcategorias, categorias=categorias, inventarios=inventarios,produtos_relacionados=prod_relacionado.json())
    

####################################################### PRODUTOS POR CATEGORIA #####################################################################

@views.route('/produtos/<nome>', methods=['GET', 'POST'])
def obter_produto_categoria(nome):

    produto = requests.get(url+'/categoria/'+nome)



    

    produtos = requests.get(url)

    subcateg = requests.get(url5)
    categ = requests.get(url4)
    invent = requests.get(url6)
    prod_relacionado=requests.get(url7)
    
    subcategorias = subcateg.json()
    categorias = categ.json()
    inventarios = invent.json()
    

    



    return render_template('prod_categoria.html', produto=produto.json(), produtos=produtos.json(), subcategorias=subcategorias, categorias=categorias, inventarios=inventarios,produtos_relacionados=prod_relacionado.json(), nomecategoria=nome)



#######################################################
@views.route('/produtos', methods=["POST"])
def inserir_produto():

    if request.method == "POST":


        nomeProduto = request.form.get('nome')
        categoriaProduto = request.form.get('categoria')
        subcategoriaProduto = request.form.get('subcategoria')
        descricaoProduto = request.form.get('descricao')
        imagemProduto= request.form.get('imagemProduto')
        corProduto = request.form.get('cor')
        precoProduto = request.form.get('preco')
        tipoProduto = request.form.get('tipo')
        especieProduto = request.form.get('especie')
        materialProduto= request.form.get('material')
        tamanhoProduto = request.form.get('tamanho')
        quantidadeProduto = request.form.get('quantidade')
        marcaProduto= request.form.get('marca')
        referenciaProduto= request.form.get('referencia')



        dados1 = {"nomeProduto": nomeProduto,"categoriaProduto": categoriaProduto, "subcategoriaProduto": subcategoriaProduto, \
                    "descricaoProduto": descricaoProduto, "imagemProduto": imagemProduto,"corProduto": corProduto, \
                    "precoProduto": precoProduto, "tipoProduto": tipoProduto, "especieProduto": especieProduto, \
                        "materialProduto": materialProduto, "tamanhoProduto": tamanhoProduto, "quantidadeProduto": quantidadeProduto, \
                            "marcaProduto": marcaProduto, "referenciaProduto": referenciaProduto}


        dados={}
        for i in dados1.keys():
            if dados1[i] != '':
                dados[i]=dados1[i]

        api=requests.post(url, json=dados)

    

        
    #print(dados)

    return redirect(url_for("views.obter_produto_categoria", nome=categoriaProduto))


@views.route('/atualizar_produto', methods=["POST", "GET"])
def atualizar_produto():

    if request.method == "POST":

        idProduto = request.form.get('id')
        nomeProduto = request.form.get('nome')
        categoriaProduto = request.form.get('categoria')
        subcategoriaProduto = request.form.get('subcategoria')
        descricaoProduto = request.form.get('descricao')
        imagemProduto= request.form.get('imagemProduto')
        corProduto = request.form.get('cor')
        precoProduto = request.form.get('preco')
        tipoProduto = request.form.get('tipo')
        especieProduto = request.form.get('especie')
        materialProduto= request.form.get('material')
        tamanhoProduto = request.form.get('tamanho')
        quantidadeProduto = request.form.get('quantidade')
        marcaProduto= request.form.get('marca')
        referenciaProduto= request.form.get('referencia')


        dados1 = {"nomeProduto": nomeProduto,"categoriaProduto": categoriaProduto, "subcategoriaProduto": subcategoriaProduto, \
                    "descricaoProduto": descricaoProduto, "imagemProduto": imagemProduto,"corProduto": corProduto, \
                    "precoProduto": precoProduto, "tipoProduto": tipoProduto, "especieProduto": especieProduto, \
                        "materialProduto": materialProduto, "tamanhoProduto": tamanhoProduto, "quantidadeProduto": quantidadeProduto, \
                            "marcaProduto": marcaProduto, "referenciaProduto": referenciaProduto}
        
        # dados={}
        # for i in dados1.keys():
        #     if dados1[i] != '':
        #         dados[i]=dados1[i]


        api=requests.put(url+'/'+idProduto, json=dados1)

        


    return redirect(url_for("views.produtos"))




@views.route('/apagar_produto/<int:id>', methods=['GET', 'POST'])
def apagar_produto(id):

    prod = requests.get(url+'/'+str(id))
    categ = requests.get(url4)

    produto=prod.json()
    categorias=categ.json()

    idcategoria = produto.get("idcategoria")

    for categoria in categorias:
        if categoria.get("idCategoria")==idcategoria:
            nome=categoria.get("nomeCategoria")


    api = requests.delete(url+'/'+str(id))

    return redirect(url_for("views.obter_produto_categoria", nome=nome))



######### editar quantidade #################################

@views.route('/quantidadeproduto/<int:id>', methods=['GET', 'POST'])
def quantidadeproduto(id):

    produto = requests.get(url+'/'+str(id))
    prod=produto.json()



    somaquantidade = prod.get("quantidadeProduto")+10

    quantidade = {"quantidadeProduto": somaquantidade}

    api = requests.patch(url+'/'+str(id), json=quantidade)

    return redirect(url_for("views.produtos"))





######################################### GESTAO INVENTARIOS #############################


@views.route('/inventarios', methods=["GET"])
def inventarios():

    inventarios = requests.get(url6)


    return inventarios.json()


@views.route('/inventarios/<int:id>', methods=['GET', 'POST'])
def obter_inventario(id):

    inventario = requests.get(url6+'/'+str(id))


    return inventario.json()
    
    
@views.route('/inventarios', methods=["POST"])
def inserir_inventario():

    if request.method == "POST":


        quantidade = request.form.get('quantidade')
        fornecedor = request.form.get('fornecedor')
        produto = request.form.get('id')
 



        dados = {"quantidade": quantidade,"fornecedor": fornecedor, "produto": produto}

        api=requests.post(url6, json=dados)

    return redirect(url_for("views.obter_produto_id", id=produto))


@views.route('/atualizar_inventario', methods=['GET', 'POST'])
def atualizar_inventario():

    if request.method == "POST":

        idInventario = request.form.get('id')
        quantidade = request.form.get('quantidade')
        fornecedor = request.form.get('fornecedor')
        produto = request.form.get('produto')

        dados = {"quantidade": quantidade,"fornecedor": fornecedor, "idproduto": int(produto),"idInventario":idInventario}
        print(dados)
  
        
        api=requests.put(url6+'/'+idInventario, json=dados)

    return redirect(url_for("views.obter_produto_id", id=produto))


@views.route('/apagar_inventario/<int:id>', methods=['GET', 'POST'])
def apagar_inventario(id):

    api = requests.delete(url6+'/'+str(id))

    return redirect(url_for("views.obter_produto_id", id=id))




######################################### GESTAO Imagens #############################


@views.route('/imagens', methods=["GET"])
def imagens():

    imagens = requests.get(url8)


    return imagens.json()


@views.route('/imagens/<int:id>', methods=['GET', 'POST'])
def obter_imagem(id):

    imagem = requests.get(url8+'/'+str(id))


    return imagem.json()
    
    
@views.route('/imagens', methods=["POST"])
def inserir_imagem():

    if request.method == "POST":


        imagem = request.form.get('imagemProduto')
        produto = request.form.get('idproduto')
 



        dados = {"imagem": imagem, "idproduto": int(produto)}
        print(dados)

        api=requests.post(url8, json=dados)

    return redirect(url_for("views.obter_produto_id", id=produto))


@views.route('/apagar_imagem/<int:id>', methods=['GET', 'POST'])
def apagar_imagem(id):

    imagem = requests.get(url8+'/'+str(id))
    img=imagem.json()
    idproduto = img.get('idproduto')

    api = requests.delete(url8+'/'+str(id))
    

    return redirect(url_for("views.obter_produto_id", id=idproduto))




############################################################################################


@views.route('/resposta', methods=['GET'])
def obter_resposta():

    respostas = requests.get(url10)

    resposta=respostas.json()

    lista_resposta=[]

    for resposta in resposta:

        lista_resposta.append(resposta)
        

        


    return render_template("respostas.html",lista_resposta=lista_resposta) 


############################################################################################


@views.route('/desafio', methods=['GET'])
def obter_desafio():

    desafios = requests.get(url11)


    return render_template("desafios.html",desafios=desafios.json()) 



@views.route('/adicionar_desafios', methods=["POST"])
def adicionar_desafios():


    imagem = request.form.get('imagemProduto')
    opcao1 = request.form.get('opcao1')
    opcao2 = request.form.get('opcao2')
    opcao3 = request.form.get('opcao3')
    opcao4 = request.form.get('opcao4')
    data=request.form.get('data')

    print(type(data), data)

    dados = {"imagemProduto": imagem, "opcao1": opcao1,"opcao2": opcao2, "opcao3": opcao3, "opcao4": opcao4, "dataDesafio": str(data)}

    

    api=requests.post(url11, json=dados)

    return redirect(url_for("views.obter_desafio"))