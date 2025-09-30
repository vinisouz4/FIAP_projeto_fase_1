from supabase import create_client, Client

from src.log.logs import LoggerHandler
from src.core.configs import Settings



class Supabase():
    def __init__(self):
        logger = LoggerHandler(__name__)
        settings = Settings()


    def _create_client(self) -> Client:
        """
        Método para criar o cliente de conexão do Supabase

        Retorno:
            - Client: Cliente do Supabase
        """
        try:
            client = create_client(
                self.settings.SUPABASE_URL,
                self.settings.SUPABASE_API_KEY
            )

            self.logger.INFO("Cliente criado")
            return client
        
        except Exception as e:
            self.logger.ERROR(f"Erro ao criar cliente Supabase: {e}")
            return None
        
    def select(self, table_name: str):
        """
        Retorna os dados da tabela consultada.

        Parametro:
            - table_name: nome da tabela que deseja realizar o select

        Retorno:
            - Retorna um dataframe
        """

        client = self._create_client()
       
        if not client:
            return None

        try:
            response = client.table(table_name).select("*").execute()
            return response.data
        except Exception as e:
            self.logger.ERROR(f"Erro ao realizar select na tabela {table_name}: {e}")
            return None
