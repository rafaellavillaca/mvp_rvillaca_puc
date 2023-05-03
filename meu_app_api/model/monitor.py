from sqlalchemy import Column, String, Integer, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Monitor(Base):
    __tablename__ = 'monitor'

    id = Column("pk_monitor", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    email = Column(String(140))
    habilidade =  Column(String(600))
    disponibilidade = Column(String(16))
    data_insercao = Column(DateTime, default=datetime.now())
    

    def __init__(self, nome:str, email: str,  habilidade:str, disponibilidade:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um monitor

        Arguments:
            nome: nome do voluntario.
            email: email do voluntario
            habilidade: habilidade que o voluntario se disponibiliza a ensinar
            disponibilidade: data e hora que o voluntario tem disponivel
            data_insercao: data de quando o voluntario foi inserido à base
        """
        self.nome = nome
        self.email = email
        self.habilidade = habilidade
        self.disponibilidade = disponibilidade



        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
