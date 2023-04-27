from pydantic import BaseModel
from typing import List
from model.monitor import Monitor
from schemas import ComentarioSchema

class MonitorSchema(BaseModel):
    """ Define como um novo monitor a ser inserido deve ser representado
    """
    nome: str = "Maria Silva"
    email: str = "mariasilva@gmail.com"
    habilidade: str = "python"
    disponibilidade: str = "MM/DD/YYYY HH:MM"

class MonitorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no email do Monitor.
    """
    email: str = "mariasilva@gmail.com"


class ListagemMonitoresSchema(BaseModel):
    """ Define como uma listagem de monitores será retornada.
    """
    monitores:List[MonitorSchema]


def apresenta_monitores(monitores: List[Monitor]):
    """ Retorna uma representação do monitor seguindo o schema definido em
        MonitorViewSchema.
    """
    result = []
    for monitor in monitores:
        result.append({
            "nome": monitor.nome,
            "email": monitor.email,
            "habilidade": monitor.habilidade,
            "disponibilidade": monitor.disponibilidade,

        })

    return {"monitores": result}


class MonitorViewSchema(BaseModel):
    """ Define como um monitor será retornado: monitor + comentários.
    """
    id: int = 1
    nome: str = "Maria Silva"
    email: str = "mariasilva@gmail.com"
    habilidade: str = "python"
    disponibilidade: str = "MM/DD/YYYY HH:MM"
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class MonitorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    email: str    
    message: str
    nome: str


def apresenta_monitor(monitor: Monitor):
    """ Retorna uma representação do monitor seguindo o schema definido em
        MonitorViewSchema.
    """
    return {
        "id": monitor.id,
        "nome": monitor.nome,
        "email": monitor.email,
        "habilidade": monitor.habilidade,
        "disponibilidade": monitor.disponibilidade,
        "total_cometarios": len(monitor.comentarios),
        "comentarios": [{"texto": c.texto} for c in monitor.comentarios]
    }
