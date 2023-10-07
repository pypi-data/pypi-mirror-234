from nsj_rest_lib.dao.dao_base import DAOBase
from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.exception import NotFoundException
from nsj_multi_database_lib.settings import log_time


class UsuarioDAO():
    def __init__(self, db: DBAdapter2):
        self._db = db

    @log_time('Coletar senha do usuário')
    def get_by_email(self, email):
        sql = """
            select login, senha
            from ns.usuarios
            where email ilike :email;
        """

        # Running query
        resp = self._db.execute_query(
            sql,
            email=email
        )

        if len(resp) <= 0:
            raise NotFoundException(
                f'Não foi encontrado um usuário vinculado à Conta Nasajon')
        
        return resp[0]