from functools import wraps
from flask import g, request

from nsj_gcf_utils.rest_error_util import format_json_error

from nsj_multi_database_lib.exception import ParameterNotFound
from nsj_multi_database_lib.injector_factory import InjectorFactory
from nsj_multi_database_lib.settings import get_logger

from nsj_multi_database_lib.crypt_util import decrypt


def multi_database():
    """TODO"""

    def __get_db_username(db_name: str, erp_login: str):
        return db_name.lower() + "_" + erp_login.lower()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with InjectorFactory() as factory:
                    database_dao = factory.database_dao()

                    # Recuperando o tenant da query string, ou do corpo da requisição
                    tenant = request.args.get("tenant")
                    if tenant is None:
                        if (
                            request.headers.get("Content-type").lower()
                            == "application/json"
                        ):
                            body = request.json
                            tenant = body["tenant"]

                    if tenant is None:
                        raise ParameterNotFound("tenant")

                    tenant = int(tenant)

                    # Recuperando os dados do banco pelo tenant
                    database = database_dao.get_by_tenant(tenant)

                    # Definindo dados de conexão com o DB no contexto da aplicação
                    g.external_database = {
                        "host": database["host"],
                        "port": database["porta"],
                        "name": database["nome"],
                        "user": None,
                        "password": None,
                    }

                if (
                    not database["force_table_credentials"]
                    and hasattr(g, "profile")
                    and "authentication_type" in g.profile
                    and g.profile["authentication_type"] == "access_token"
                ):
                    with InjectorFactory(
                        use_external_db_with_default_credentials=True
                    ) as factory:
                        usuario_dao = factory.usuario_dao()

                        usuario = usuario_dao.get_by_email(g.profile["email"])

                        user = __get_db_username(
                            g.external_database["name"], usuario["login"]
                        )
                        password = usuario["senha"]
                elif database["user"] is not None and database["password"] is not None:
                    # Decypt user and password
                    user = decrypt(database["user"])
                    password = decrypt(database["password"])
                else:
                    raise Exception(f"Usuário não configurado no banco do multibancos")

                # Gravando usuario e senha na variável g do Flask
                g.external_database["user"] = user
                g.external_database["password"] = password

                return func(*args, **kwargs)
            except ParameterNotFound as e:
                if request.method.upper() == "GET":
                    msg = f"Faltando parâmetro obrigatório na requisição: {e}."
                else:
                    msg = (
                        f"Faltando propriedade obrigatória no corpo da requisição: {e}."
                    )

                get_logger().warning(msg)
                return (
                    format_json_error(msg),
                    400,
                    {"Content-Type": "application/json; charset=utf-8"},
                )
            except Exception as e:
                msg = f"Erro desconhecido: {e}."
                get_logger().exception(msg, e)
                return (
                    format_json_error(msg),
                    500,
                    {"Content-Type": "application/json; charset=utf-8"},
                )

        return wrapper

    return decorator
