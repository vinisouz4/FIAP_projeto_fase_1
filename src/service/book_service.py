import pandas as pd

from src.log.logs import LoggerHandler

logger = LoggerHandler(__name__)


def _load_data():

    """
    Carrega os dados do CSV e realiza o pré-processamento necessário.
    Retorno:
        - pd.DataFrame: DataFrame com os dados dos livros
    """

    try:
        df = pd.read_csv("./src/data/books_data.csv")

        df['price'] = df['price'].str.replace(r"[^\d.]", "", regex=True).astype(float)

        logger.INFO("Data loaded successfully.")
        return df
    except Exception as e:
        logger.ERROR(f"Error loading data: {e}")
        return pd.DataFrame()  # retorna DataFrame vazio em caso de erro

def get_categories():
    try:
        
        categories = pd.read_csv("./src/data/categories_data.csv")
        
        categories.drop(columns=['link'], inplace=True)

        return categories.to_dict(orient='records')
    except Exception as e:
        logger.ERROR(f"Error retrieving categories: {e}")
        return []
    
def get_all_books():

    """
    Recupera todos os registros de livros do CSV.
    Retorno:
        - List[dict]: Lista de dicionários, cada um representando um livro
    """

    try:
        df = _load_data()
        
        return df.to_dict(orient='records')
    except Exception as e:
        logger.ERROR(f"Error retrieving all books: {e}")
        return []
    
def get_book_id(book_id):

    """
    Recupera um registro de livro específico pelo ID.
    Parâmetros:
        - book_id (str): ID do livro a ser recuperado
    Retorno:
        - dict: Dicionário representando o livro, ou None se não encontrado
    """

    try:
        df = _load_data()
        
        record = df[df['id'] == str(book_id)]
        
        if not record.empty:
            logger.INFO(f"Record with ID {book_id} found.")
            return record.to_dict(orient='records')[0]
        else:
            logger.WARNING(f"No record found with ID {book_id}.")
            return None
    except Exception as e:
        logger.ERROR(f"Error retrieving record with ID {book_id}: {e}")
        return None
    
def search_books(title: str = None, category: str = None):

    """
    Pesquisa livros por título e/ou categoria.
    Parâmetros:
        - title (str, opcional): Título ou parte do título do livro
        - category (str, opcional): Categoria do livro
    Retorno:
        - List[dict]: Lista de dicionários representando os livros encontrados
    """

    try:
        df = _load_data()

        if title:
            df = df[df['title'].str.lower().str.contains(title.lower().strip(), na=False)]
        
        elif category:
            df = df[df['category'].str.lower().str.strip() == 'travel']

        elif title and category:
            df = df[
                (df['title'].str.lower().str.contains(title.lower().strip(), na=False)) &
                (df['category'].str.lower().str.strip() == category.lower().strip())
            ]

        if not df.empty:
            logger.INFO(f"Records found for title='{title}' and category='{category}'.")
            logger.INFO(f"Filtered DataFrame: {df}")
            return df.to_dict(orient='records')
        else:
            logger.WARNING(f"No records found for title='{title}' and category='{category}'.")
            return []

    except Exception as e:
        logger.ERROR(f"Error searching records: {e}")
        return []
