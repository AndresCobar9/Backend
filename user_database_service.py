import re
import string
from flask import jsonify, request
from sqlalchemy import create_engine, false, null
from sqlalchemy import exc

from sqlalchemy.orm import sessionmaker
from user_database_setup import Base, LocalUser

engine=create_engine('sqlite:///users.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)

def get_info():
        session=DBSession()
        users = session.query(LocalUser).all()
        
        
        return jsonify(users=[user.serialize() for user in users])

def get_user(r_username):
        session=DBSession()
        q=session.query(LocalUser).filter(r_username == LocalUser.username).first()
        session.close()
        if q:
                resulted_user=LocalUser(id=q.id, username=q.username, name=q.name, email=q.email, password=q.password, created=q.created, role=q.role, isactive=q.isactive)
                return resulted_user
        else:
                return None


def update_user(user_id):
    # Inicia una nueva sesión de la base de datos
    session = DBSession()

    # Busca el usuario que deseas actualizar
    user = session.query(LocalUser).filter(LocalUser.id == user_id).first()

    # Si no se encuentra el usuario, devuelve un error 404
    if not user:
        return {'message': 'User not found'}, 404

    # Actualiza las columnas del usuario
    user.name = request.json.get('name', user.name)
    user.role = request.json.get('role', user.role)
    user.gender = request.json.get('gender', user.gender)
    user.username = request.json.get('username', user.username)
    user.email = request.json.get('email', user.email)
    user.password = request.json.get('password', user.password)
    user.isactive = request.json.get('isactive', user.isactive)
    

    # Confirma los cambios en la sesión
    session.commit()

    # Devuelve el usuario actualizado
    return {'message': 'User updated', 'user': user.to_dict()}


def if_email_domain(email):
    x = re.findall("@hotmail.com|@outlook.com|@yahoo.com|@gmail.com", email)
    print(x)
    if x == [] :
        return False
    else:
        return True


def if_user_exists(r_email):
        session=DBSession()
        q=session.query(LocalUser).filter(r_email == LocalUser.email).first()
        session.close()
        if q is None:
                return False
        else:
                return True

def if_user_number(name, lastname):
    x = re.findall("[^a-zA-Z\s]", name)
    x1 = re.findall("[^a-zA-Z\s]", lastname)
    print(x)
    y = []
    if x != y:
        return False
    elif x1 != y:
        return False
    else:
        return True


def add_user(new_user):
        try:
                session=DBSession()
                session.add(new_user)
                session.flush()
                session.commit()
                session.close()
                return True
        except exc.SQLAlchemyError as e:
                return False

