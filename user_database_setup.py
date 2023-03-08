import os
import sys
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LocalUser(Base):
    __tablename__ = 'local_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    role = Column(String(250), nullable=False)
    gender = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String, nullable=False)
    created = Column(String, nullable=False)
    isactive = Column(Boolean, nullable = False)
    
    def serialize(self):
        return {
            
            'name': self.name,
            'role': self.role,
            'gender': self.gender,
            'username': self.username,
            'email': self.email,
            'created': self.created,
            'autorizado': self.isactive
        }
	
	



engine=create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
