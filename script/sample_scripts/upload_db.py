import mysql.connector
import pandas as pd

if __name__ == '__main__':
    # CSV file path
    CSV_FILE = "daily_data.csv"
    DB_NAME = "Time_Series"

    # Connect to MySQL server
    conn = mysql.connector.connect(
                host="sh-cdb-aale09ms.sql.tencentcdb.com",
                port=26059,
                user="root",
                password="xemjyn-kanqoq-gImho4"
                # You can optionally specify a database if needed
        )
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    # Load CSV to infer column names and data types
    df = pd.read_csv(CSV_FILE)

    # Generate CREATE TABLE SQL statement
    table_name = "daily_data"
    columns = ", ".join([f"`{col}` TEXT" for col in df.columns])  # Assuming all columns are text initially

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns}
    );
    """
    cursor.execute(create_table_query)

    # Insert data into the table
    for _, row in df.iterrows():
        placeholders = ", ".join(["%s"] * len(row))
        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(row))

    # Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()

    print("Data uploaded successfully!")
