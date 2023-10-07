from typing import List

from nsj_rest_lib.dao.dao_base import DAOBase
from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.exception import NotFoundException

from nsj_multi_database_lib.crypt_util import decrypt
from nsj_multi_database_lib.settings import log_time


class DatabaseDAO(DAOBase):
    def __init__(self, db: DBAdapter2, entity_class: EntityBase):
        super().__init__(db, entity_class)

    @log_time("Coletar banco ERP do tenant")
    def get_by_tenant(self, tenant):
        sql = """
            select host, porta, nome, "user", password, force_table_credentials
            from multibanco.database
            where tenant = :tenant;
        """

        # Running query
        resp = self._db.execute_query(sql, tenant=tenant)

        if len(resp) <= 0:
            raise NotFoundException(
                f"Não foi encontrado uma configuração de banco vinculada ao tenant"
            )

        return resp[0]

    def list_all(self) -> List[EntityBase]:
        databases = []

        limit = 20
        fields = ["id", "host", "porta", "nome", "tenant", '"user"', "password"]
        response = self.list(
            after=None, limit=limit, fields=fields, order_fields=None, filters=None
        )
        databases += response

        while True:
            if len(response) == limit:
                last_id = getattr(response[-1], response[-1].get_pk_column_name())
                response = self.list(
                    after=last_id,
                    limit=limit,
                    fields=fields,
                    order_fields=None,
                    filters=None,
                )
                databases += response
                continue
            else:
                break

        # Decrypt user and password
        for database in databases:
            if database.user is not None:
                database.user = decrypt(database.user)
            if database.password is not None:
                database.password = decrypt(database.password)

        return databases
