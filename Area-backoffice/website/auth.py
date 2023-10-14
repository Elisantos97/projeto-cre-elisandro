from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import  requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
#from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

url ='https://elisandroapicre.azurewebsites.net/utilizadores'
url3='https://elisandroapicre.azurewebsites.net/clientes'
url1='https://elisandroapicre.azurewebsites.net/produtos'
url4='https://elisandroapicre.azurewebsites.net/categorias'
url5='https://elisandroapicre.azurewebsites.net/subcategorias'


@auth.route('/')
def home():
    
    produtos = requests.get(url1)
    categorias = requests.get(url4)
    subcategorias = requests.get(url5)

    if "email" in session:
        email = session["email"]

        return render_template('home.html', session1=session, email=email, produtos=produtos.json(), categorias=categorias.json(), subcategorias=subcategorias.json())
    return redirect(url_for("auth.login"))


@auth.route('/login', methods=["POST", "GET"])
def login():

    #session["email"]="elisandro@cv"

    

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        

        api=requests.get(url)


        user_exist=False

        for user in api.json():
            
            if user['emailUtilizador'] == email:
                user_exist = user
                break
            else:                        # se calhar esse else não é preciso
                user_exist = False   

        if user_exist:

            if user_exist['passwordUtilizador']==password:  #check_password_hash(user_exist['passwordUtilizador'], password):
                flash('login feito com sucesso!', category='success')

                session["email"]=email
            
                requests.patch(url+'/'+email, json={})
                return redirect(url_for('auth.home'))
            else:
                flash('Palavra passe errada!', category='error')

        else:

            flash('Esta conta não existe!', category='error')

    else:
        if "email" in session:
            return redirect(url_for('auth.home'))
  
    return render_template('login.html')


# @auth.route("/signup", methods=["POST", "GET"])
# def signup():

#     if "email" in session:
#         email = session["email"]
#         return render_template('home.html')

#     else:

#         if request.method == "POST":
            
#             nome = request.form.get('nome')
#             email = request.form.get('email')
#             password = request.form.get('password')
#             password2 = request.form.get('password2')
#             tipo_util = request.form.get('tipo_util')
#             policy= request.form.get('policy')

#             api=requests.get(url)

#             user_exist=False

#             for user in api.json():
#                 if user['emailUtilizador'] == email:
#                     user_exist = True
#                     break
#                 else:                        # se calhar esse else não é preciso
#                     user_exist = False

#             dados={"nomeUtilizador": nome, "emailUtilizador": email,"passwordUtilizador": password, "idtipoUtilizador": tipo_util} #generate_password_hash(password, method='sha256'), \
                   

#             if user_exist:
#                 flash('este email já foi usado!', category='error')

#             else:

#                 if len(email)<7:
#                     flash('Email tem de ter pelo menos 7 caracteres!', category='error')
#                 elif len(password)<6:
#                     flash('password tem de ter pelo menos 6 caracteres!', category='error')
#                 elif password!=password2:
#                     flash('password tem de ser iguais!', category='error')
#                 elif policy == None:
#                     flash(' Tem de aceitar termos e condições', category='error')
#                 else:
#                     api=requests.post(url, json=dados)
#                     flash('A conta fui criada com sucesso', category='success')

#                     return redirect(url_for('auth.home'))

#         return render_template('sign_up.html')
    
@auth.route('/logout')
def logout():
    session.pop("email", None)
    return redirect(url_for('auth.login'))

