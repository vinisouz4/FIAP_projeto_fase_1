import pandas as pd



def get_data_from_csv(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    Args:
        file_path (str): The path to the CSV file.
    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)

        # Convert dataframe to dictionary
        data_dict = df.to_dict(orient='records')

        print(f"✅ Data loaded successfully from {file_path}")
        
        return data_dict
    
    except Exception as e:    
        print(f"❌ Error loading data from {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    

def get_data_by_id(file_path, book_id):
    """
    Retrieve a specific record from the CSV file by its ID.
    Args:
        file_path (str): The path to the CSV file.
        book_id (int): The ID of the record to retrieve.
    Returns:
        dict: The record with the specified ID, or None if not found.
    """
    try:
        df = pd.read_csv(file_path)
        
        record = df[df['id'] == book_id]

        if not record.empty:
            print(f"✅ Record with ID {book_id} found.")
            return record.to_dict(orient='records')[0]
        else:
            print(f"❌ No record found with ID {book_id}.")
            return None
    
    except Exception as e:
        print(f"❌ Error retrieving record with ID {book_id} from {file_path}: {e}")
        return None
    

def get_data_by_category_title(file_path: str, category: str = None, title: str = None):
    """
        Retrieve records from the CSV file that match a specific category title.
        Args:
            file_path (str): The path to the CSV file.
            category (str): The category title to filter records by.
            title (str): The book title to filter records by.
    """
    try:
        df = pd.read_csv(file_path)

        if category:
            df = df[df['category'] == category]

        if title:
            df = df[df['title'].str.contains(title, case=False, na=False)]

        if not df.empty:
            print(f"✅ Records found for category '{category}' and title '{title}'.")
            return df.to_dict(orient='records')
        else:
            print(f"❌ No records found for category '{category}' and title '{title}'.")
            return []

    except Exception as e:
        print(f"❌ Error retrieving records from {file_path}: {e}")
        return []