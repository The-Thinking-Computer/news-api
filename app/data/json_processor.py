import json
import sqlite3

def process_json_file(json_file_path, db_file_path):
    """
    Process the JSON file and insert each object into an SQL database while avoiding duplicates.

    Args:
        json_file_path (str): The file path of the JSON file containing objects with the specified structure.
        db_file_path (str): The file path of the SQLite database.

    Returns:
        int: The number of new records inserted into the database.
    """
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                      (id TEXT PRIMARY KEY, data TEXT, hash TEXT)''')

    # Read and process the JSON file
    new_records_count = 0
    ##############CHATGPT##############
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
        for obj in json_data:
            if validate_input(obj):
                # Generate digital signature and hash
                signed_data = generate_signature(obj)
                hash_value = generate_hash(signed_data)

                # Check for duplicates in the database
                cursor.execute("SELECT COUNT(*) FROM articles WHERE id=?", (obj['id'],))
                count = cursor.fetchone()[0]
                if count == 0:
                    # Insert new record into the database
                    cursor.execute("INSERT INTO articles (id, data, hash) VALUES (?, ?, ?)", (obj['id'], json.dumps(signed_data), hash_value))
                    new_records_count += 1
    ######################################
    ##THIS PART SHOULD BE REWRITTEN TO USE THE DB CLASSES IN data/db.py ###
    conn.commit()
    conn.close()
    ###########
    return new_records_count

# Example usage:
if __name__ == "__main__":
    json_file_path = 'data.json'
    db_file_path = 'articles.db'
    new_records_count = process_json_file(json_file_path, db_file_path)
    print(f"Number of new records inserted: {new_records_count}")