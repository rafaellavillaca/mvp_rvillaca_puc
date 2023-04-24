from sqlalchemy import Column, String, Integer, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Monitor(Base):
    __tablename__ = 'monitor'

    id = Column("pk_monitor", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    email = Column(String(140))
    habilidade =  Column(String(600))
    dia = Column(String(10))
    hora = Column(String(5))
    data_insercao = Column(DateTime, default=datetime.now())
    
    # Definição do relacionamento entre o monitor e o comentário.
    # Essa relação é implicita, não está salva na tabela 'monitor',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, email: str,  habilidade:str, dia:str, hora:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um monitor

        Arguments:
            nome: nome do voluntario.
            email: email do voluntario
            habilidade: habilidade que o voluntario se disponibiliza a ensinar
            dia: data que o voluntario tem disponivel
            hora: data que o voluntario tem disponivel
            data_insercao: data de quando o voluntario foi inserido à base
        """
        self.nome = nome
        self.email = email
        self.habilidade = habilidade
        self.dia= dia
        self.hora = hora


        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao monitor
        """
        self.comentarios.append(comentario)

