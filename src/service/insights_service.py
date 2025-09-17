import pandas as pd
from src.log.logs import LoggerHandler


logger = LoggerHandler(__name__)


def _load_data():
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
    try:
        
        categories = _load_data()
        
        categories_grouped = categories.groupby('category').agg(
            {
                'title': 'count', 
                'price': 'mean'
            }
        ).reset_index()

        categories_grouped["price"] = categories_grouped["price"].round(2)

        logger.INFO("Categories retrieved successfully for insights.")
        return categories_grouped.to_dict(orient='records')
    except Exception as e:
        logger.ERROR(f"Error retrieving categories for insights: {e}")
        return None
    
def get_top_rated_books():
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
        return None
    

def get_price_range(min_price: float, max_price: float):
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
        return None