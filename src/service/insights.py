import pandas as pd
from collections import Counter



def _get_data_from_csv(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    Args:
        file_path (str): The path to the CSV file.
    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)

        # Remover caracteres não numéricos (como Â£) e converter para float
        df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True).astype(float)

        return df

    except Exception as e:
        print(f"❌ Error loading data from {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    

def overview_statistics():
    """
    Generate overview statistics from the DataFrame.
    Args:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        dict: A dictionary containing overview statistics.
    """
    df = _get_data_from_csv("./src/data/books_data.csv")
    if df.empty:
        return {"error": "No data available"}

    total_books = len(df)

    print(df.dtypes)

    # Arrumar o erro de string must be integer
    
    average_price = sum(book["price"] for book in df) / total_books if total_books > 0 else 0
    
    ratings = [book["rating"] for book in df]
    rating_distribution = dict(Counter(ratings)) # Count occurrences of each rating


    return {
        "total_books": total_books,
        "average_price": average_price,
        "rating_distribution": rating_distribution
    }