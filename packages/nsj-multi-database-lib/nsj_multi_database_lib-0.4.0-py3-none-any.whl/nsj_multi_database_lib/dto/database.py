import datetime
import decimal
import uuid

from nsj_rest_lib.decorator.dto import DTO
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.descriptor.dto_field_validators import DTOFieldValidators
from nsj_rest_lib.dto.dto_base import DTOBase


@DTO()
class DatabaseDTO(DTOBase):

    id: uuid.UUID = DTOField(
        resume=True, pk=True, not_null=True, validator=DTOFieldValidators().validate_uuid)
    host: str = DTOField(resume=True, not_null=True, min=1, max=180)
    porta: int = DTOField(resume=True, not_null=True)
    nome: str = DTOField(resume=True, not_null=True, min=1, max=100)
    homologacao: bool = DTOField(resume=True, not_null=True, default_value=False)
    # Atributos de auditoria
    criado_em: datetime.datetime = DTOField(
        resume=True,
        default_value=datetime.datetime.now
    )
    criado_por: str = DTOField(
        resume=True, not_null=False, strip=True, min=1, max=150, validator=DTOFieldValidators().validate_email)
    atualizado_em: datetime.datetime = DTOField(
        resume=True,
        default_value=datetime.datetime.now
    )
    atualizado_por: str = DTOField(
        resume=True, not_null=False, strip=True, min=1, max=150, validator=DTOFieldValidators().validate_email)
    apagado_em: datetime.datetime = DTOField()
    apagado_por: str = DTOField(
        strip=True, min=1, max=150, validator=DTOFieldValidators().validate_email)
    # Atributos de segmentação dos dados
    tenant: int = DTOField(resume=True, not_null=True, partition_data=True)
