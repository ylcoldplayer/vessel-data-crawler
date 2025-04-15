import mysql.connector
from mysql.connector import Error
import pandas as pd
import sqlalchemy

def connect_to_database(host_name, user_name, port, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            port=port,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def download_data_to_csv(connection, query, output_file):
    try:
        # Create a cursor to execute the query
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)

        # Fetch all rows from the query result
        rows = cursor.fetchall()

        # Convert to Pandas DataFrame
        df = pd.DataFrame(rows)

        # Save to a CSV file
        df.to_csv(output_file, index=False)
        print(f"Data successfully saved to {output_file}")

    except Error as e:
        print(f"The error '{e}' occurred during data export")
    finally:
        cursor.close()

if __name__ == '__main__':
    connection = connect_to_database(
        host_name='sh-cynosdbmysql-grp-pvsmsm7y.sql.tencentcdb.com',
        user_name='root',
        port=23620,
        user_password='Cyl@31415',
        db_name='Time_Series'
    )

    import pandas as pd
    import sqlalchemy

    # Database connection details
    query = "SELECT * FROM Time_Series.daily_data;"
    output_file = "daily_data.csv"

    # Download data to CSV if connection is successful
    if connection:
        download_data_to_csv(connection, query, output_file)
        connection.close()
