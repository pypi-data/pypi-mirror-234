import datetime
import decimal
import uuid
from typing import List
from nsj_rest_lib.entity.entity_base import EntityBase


class DatabaseEntity(EntityBase):

    def __init__(self) -> None:
        super().__init__()

        self.id: uuid.UUID = None
        self.host: str = None
        self.porta: int = None
        self.nome: str = None
        self.homologacao: bool = None
        self.user: str = None 
        self.password: str = None 
        # Atributos de auditoria
        self.criado_em: datetime.datetime = None
        self.criado_por: str = None
        self.atualizado_em: datetime.datetime = None
        self.atualizado_por: str = None
        self.apagado_em: datetime.datetime = None
        self.apagado_por: str = None
        # Atributos de segmentação dos dados
        self.tenant: str = None 

    def get_table_name(self) -> str:
        return "multibanco.database"

    def get_default_order_fields(self) -> List[str]:
        return ['id']
    
    def get_pk_field(self) -> str:
        return 'id'