## Imports
from datetime import datetime, timedelta
from socket import socket
from xmlrpc.client import boolean ## Sockets de comunicacion
from flask import Flask, jsonify, request, session  ## Import especifico de Flask
from flask_cors import CORS ## Import que permite el CORS origins de Flask
from flask_socketio import SocketIO
from sqlalchemy import false, true ## Modulo Socket Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (create_access_token)
from flask_jwt_extended import JWTManager
from user_database_setup import LocalUser
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager
## importa Endpoints
import user_database_service


## Definicion de la aplicacion
app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":'*'}})
socket = SocketIO(app,cors_allowed_origins="*") ## Definimos Cors
bcrypt=Bcrypt(app)
SECRET_KEY = 'CODENTkey'
app.config['JWT_SECRET_KEY'] = SECRET_KEY # clave secreta para firmar los tokens JWT
jwt_manager = JWTManager(app) # inicialización de JWTManager



@app.route('/user/register', methods=['POST'])
def register():
    r_name=request.get_json()['name']
    r_username=request.get_json()['username']
    r_email=request.get_json()['email']
    r_comp=request.get_json()['password']
    r_gender=request.get_json()['gender']
    r_password=bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    result=""
    
    if user_database_service.if_email_domain(r_email) == False:
        result="Invalid Email"
        print(result)
        return jsonify({'result': result})

    if user_database_service.if_user_exists(r_email):
        result="user already exists"
        print(result)
        return jsonify({'result': result})

    if user_database_service.if_user_number(r_name, r_username) == False:
        result="The Name or username doesnt have number"
        print(result)
        return jsonify({'result': result})

    if len(r_comp) < 5:
        result="Password Length"
        print(result)
        return jsonify({'result': result})
    r_comp = ""
     
    new_user=LocalUser(name=r_name, username=r_username, email=r_email, password=r_password, gender = r_gender , role = 'admin', isactive = True, created=datetime.utcnow())
    added=user_database_service.add_user(new_user)
    if added is True:
        result="user successfully added"
        print(result)
    else:
        result="unable to add"
        print(result)
    return jsonify({'result': result})


@app.route('/user/login', methods=['POST'])
def login():
    username=request.get_json()['username']
    password=request.get_json()['password']
    result=""

    response_user=user_database_service.get_user(username)

    if response_user:
        if bcrypt.check_password_hash(response_user.password, password):
            
            identity={
                'username': response_user.username,
                'name': response_user.name,
                'userrole': response_user.role,
                'isactive': response_user.isactive
            }

            # Crear el token JWT con una duración de 1 hora
            exp_time = datetime.utcnow() + timedelta(hours=1)
            payload = {
                'exp': exp_time,
                'sub': response_user.id,
                'identity': identity
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            
            # Devolver el token JWT en la respuesta
            return jsonify({'token': token, 'exp': exp_time.strftime('%Y-%m-%d %H:%M:%S'), 'identity': identity})
        else:
            result=jsonify({'error': 'Invalid username or password'})
    return result

@app.route('/user/userslist', methods=['GET'])
def users():
    response_user=user_database_service.get_info()
    print(response_user)
    return response_user



@app.route('/actualizar', methods=['POST'])
def actualizar_usuario():
    # Obtener los datos del formulario
    usuario_id = request.form['id']
    name = request.form['name']
    role = request.form['role']
    gender = request.form['gender']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    created = request.form['created']
    isactive = True if request.form.get('isactive') == 'true' else False

    # Actualizar la fila correspondiente en la base de datos
    usuario = session.query(LocalUser).filter_by(id=usuario_id).first()
    usuario.name = name
    usuario.role = role
    usuario.gender = gender
    usuario.username = username
    usuario.email = email
    usuario.password = password
    
## Inicializar el Server
if __name__ == "__main__":
    app.run(host="localhost", port = '3000', debug = False)


