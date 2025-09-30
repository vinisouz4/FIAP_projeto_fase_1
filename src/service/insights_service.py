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

    
def overview_statistics():
    """
    Generate overview statistics from the DataFrame.
    Args:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        dict: A dictionary containing overview statistics.
    """
    df = _load_data()
    if df.empty:
        return {"error": "No data available"}

    total_books = len(df)
    
    average_price = df["price"].mean() if not df.empty else 0
    
    rating_distribution = df["rating"].value_counts().to_dict()

    logger.INFO("Overview calculated")

    return {
        "total_books": total_books,
        "average_price": round(average_price, 2),
        "rating_distribution": rating_distribution
    }

def get_categories_insights():

    """
    Recupera insights sobre categorias de livros.
    Retorno:
        - List[dict]: Lista de dicionários, cada um representando uma categoria com
            total de livros e preço médio
    """

    try:
        
        categories = _load_data()
        
        categories_grouped = categories.groupby('category').agg(
            {
                'title': 'count', 
                'price': 'mean'
            }
        ).reset_index()

        categories_grouped["price"] = categories_grouped["price"].round(2)

        categories_grouped.rename(
            columns={
                'title': 'total_category', 
                'price': 'average_price'
            }, 
            inplace=True
        )

        logger.INFO("Categories retrieved successfully for insights.")
        return categories_grouped.to_dict(orient='records')
    except Exception as e:
        logger.ERROR(f"Error retrieving categories for insights: {e}")
        return []
    
def get_top_rated_books():

    """
    Recupera os livros com as melhores avaliações.
    Retorno:
        - List[dict]: Lista de dicionários, cada um representando um livro
            com as melhores avaliações
    """

    try:
        df = _load_data()
        
        top_rated = df.sort_values(
            by='rating', 
            ascending=False
        )

        top_rated.drop(
            columns=["image_url"], 
            inplace=True
        )
        
        logger.INFO("Top rated books retrieved successfully.")
        
        return top_rated.to_dict(orient='records')
    except Exception as e:
        logger.ERROR(f"Error retrieving top rated books: {e}")
        return []
    

def get_price_range(min_price: float, max_price: float):

    """
    Recupera os livros dentro de uma faixa de preço específica.
    Parâmetros:
        - min_price (float): Preço mínimo
        - max_price (float): Preço máximo
    Retorno:
        - List[dict]: Lista de dicionários, cada um representando um livro
            dentro da faixa de preço
    """

    try:
        df = _load_data()
        
        filtered_books = df[
            (df['price'] >= min_price) & 
            (df['price'] <= max_price)
        ].sort_values(by='price', ascending=True)

        filtered_books.drop(
            columns=["image_url"], 
            inplace=True
        )
        
        logger.INFO(f"Books filtered by price range {min_price} - {max_price} successfully.")
        
        return filtered_books.to_dict(orient='records')
    except Exception as e:
        logger.ERROR(f"Error filtering books by price range: {e}")
        return []
    

def get_best_value():
    
    """
    Recupera os livros com a melhor relação custo-benefício (preço/avaliação).
    Retorno:
        - List[dict]: Lista de dicionários, cada um representando um livro
            com a melhor relação custo-benefício
    """

    try:
        df = _load_data()

        df["value_ratio"] = (df["price"] / df["rating"]).round(2)
        best_value = df.sort_values(
            by='value_ratio',
            ascending=True
        )

        best_value.drop(
            columns=["image_url", "stock"],
            inplace=True
        )

        logger.INFO("Best value books retrieved successfully.")

        return best_value.to_dict(orient='records')
    except Exception as e:
        logger.ERROR(f"Error retrieving best value books: {e}")
        return []
    

def get_group_by_price():

    """
    Agrupa os livros por faixa de preço -> Cheap, Medium ou Expensive.
    Retorno:
        - dict: Dicionário com faixas de preço como chaves e listas de livros como valores
    """

    try:
        df = _load_data()
        
        bins = [0, 20, 50, float('inf')]
        labels = ["cheap", "medium", "expensive"]
        
        df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels, right=False)
        
        df_grouped = df["price_range"].value_counts().reset_index()
        df_grouped.columns = ["price_range", "count"]

        logger.INFO("Books grouped by price range successfully.")
        
        return df_grouped.to_dict(orient="records")
    except Exception as e:
        logger.ERROR(f"Error grouping books by price range: {e}")
        return []