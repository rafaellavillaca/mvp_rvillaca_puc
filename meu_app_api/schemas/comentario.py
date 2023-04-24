from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    monitor_id: int = 1
    texto: str = "Sessoes de 30 min"
