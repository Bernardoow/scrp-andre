from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://////Users/Leu/Projetos/scrp-andre/Sample.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

'''
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer(), primary_key = True)
    user_name = Column(String(80), unique=True)



u = User()
u.user_name = 'user2'
session.add(u)
session.commit()
'''

class Curso(Base):
	__tablename__ = 'cursos'
	id = Column(Integer(), primary_key = True)
	nome_curso = Column(String(255),)
	area_conhecimento = Column(String(4000))
	descricao = Column(String(4000))
	area_conhecimento_cnpq = Column(String(4000))
	importante = Column(String(4000))
	objetivos = Column(String(4000))
	unidade_id = Column(Integer(), ForeignKey('unidades.id'), nullable=False)

class Unidade(Base):
	__tablename__ = 'unidades'
	id = Column(Integer(), primary_key = True)
	unidade = Column(String(80), unique=True)


#Base.metadata.create_all(engine)



	

