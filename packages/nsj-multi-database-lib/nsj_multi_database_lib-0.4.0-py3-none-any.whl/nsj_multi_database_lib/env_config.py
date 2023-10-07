import os


class EnvConfig:
    _instance = None

    def __init__(self):
        self.multi_database_host = os.environ["MULTI_DATABASE_HOST"]
        self.multi_database_name = os.environ["MULTI_DATABASE_NAME"]
        self.multi_database_user = os.environ["MULTI_DATABASE_USER"]
        self.multi_database_password = os.environ["MULTI_DATABASE_PASS"]
        self.multi_database_port = os.environ["MULTI_DATABASE_PORT"]
        self.default_external_database_user = os.environ[
            "DEFAULT_EXTERNAL_DATABASE_USER"
        ]
        self.default_external_database_password = os.getenv(
            "DEFAULT_EXTERNAL_DATABASE_PASSWORD"
        )
        if self.default_external_database_password is None:
            self.default_external_database_password = os.getenv(
                "DEFAULT_EXTERNAL_DATABASE_PASS"
            )
        if self.default_external_database_password is None:
            raise Exception(
                "Faltando definir variável de ambiente DEFAULT_EXTERNAL_DATABASE_PASSWORD (para uso dda biblioteca de multi banco)"
            )

    @staticmethod
    def instance():
        if EnvConfig._instance == None:
            EnvConfig._instance = EnvConfig()

        return EnvConfig._instance
