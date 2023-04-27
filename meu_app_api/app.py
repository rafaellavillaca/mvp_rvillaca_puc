from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import pandas as pd
from model import Session, Monitor, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)

CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
monitor_tag = Tag(name="Monitor", description="Adição, visualização e remoção de monitor à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um monitor cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/monitor', tags=[monitor_tag],
          responses={"200": MonitorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_monitor(form: MonitorSchema):
    """Adiciona um novo Monitor à base de dados

    Retorna uma representação dos monitores e comentários associados.
    """

    monitor = Monitor(
        nome=form.nome,
        email=form.email,
        habilidade=form.habilidade,
        disponibilidade =  form.disponibilidade)


    logger.debug(f"Adicionando Monitor com email: '{monitor.email}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando monitor
        session.add(monitor)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado monitor email: '{monitor.email}'")
        return apresenta_monitor(monitor), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Monitor com o mesmo email já salvo na base :/"
        logger.warning(f"Erro ao adicionar Monitor '{monitor.email}', {error_msg}")
        print(e)
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar monitor '{monitor.email}', {error_msg}")
        print(e)
        return {"message": error_msg}, 400


@app.get('/monitores', tags=[monitor_tag],
         responses={"200": ListagemMonitoresSchema, "404": ErrorSchema})
def get_monitores():
    """Faz a busca por todos os Monitores cadastrados

    Retorna uma representação da listagem de monitores.
    """
    logger.debug(f"Coletando monitores ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    monitores = session.query(Monitor).all()

    if not monitores:
        # se não há monitores cadastrados
        return {"monitores": []}, 200
    else:
        logger.debug(f"%d monitores encontrados" % len(monitores))
        # retorna a representação de monitor
        print(monitores)
        return apresenta_monitores(monitores), 200


@app.get('/monitor', tags=[monitor_tag],
         responses={"200": MonitorViewSchema, "404": ErrorSchema})
def get_monitor(query: MonitorBuscaSchema):
    """Faz a busca por um Monitor a partir do email do monitor

    Retorna uma representação dos monitores e comentários associados.
    """
    monitor_email = query.email
    logger.debug(f"Coletando dados sobre monitor #{monitor_email}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    monitor = session.query(Monitor).filter(Monitor.email == monitor_email).first()

    if not monitor:
        # se o monitor não foi encontrado
        error_msg = "Monitor não encontrado na base :/"
        logger.warning(f"Erro ao buscar monitor '{monitor_email}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Monitor encontrado: '{monitor.email}'")
        # retorna a representação de monitor
        return apresenta_monitor(monitor), 200


@app.delete('/monitor', tags=[monitor_tag],
            responses={"200": MonitorDelSchema, "404": ErrorSchema})
def del_monitor(query: MonitorBuscaSchema):
    """Deleta um Monitor a partir do nome de monitor informado

    Retorna uma mensagem de confirmação da remoção.
    """
    monitor_email = unquote(unquote(query.email))
    print(monitor_email)
    logger.debug(f"Deletando dados sobre monitor #{monitor_email}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Monitor).filter(Monitor.email == monitor_email).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado monitor #{monitor_email}")
        return {"message": "monitor removido", "email": monitor_email}
    else:
        # se o monitor não foi encontrado
        error_msg = "Monitor não encontrado na base :/"
        logger.warning(f"Erro ao deletar monitor #'{monitor_email}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": MonitorViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um monitores cadastrado na base identificado pelo email

    Retorna uma representação dos monitores e comentários associados.
    """
    monitor_id  = form.monitor_id
    logger.debug(f"Adicionando comentários ao monitor #{monitor_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo monitor
    monitor = session.query(Monitor).filter(Monitor.id == monitor_id).first()

    if not monitor:
        # se monitor não encontrado
        error_msg = "Monitor não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao monitor '{monitor_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao monitor
    monitor.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao monitor #{monitor_id}")

    # retorna a representação de monitor
    return apresenta_monitor(monitor), 200
