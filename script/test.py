import mysql.connector
from mysql.connector import Error

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

if __name__ == '__main__':
    # connection = connect_to_database(
    #     host_name='sh-cdb-aale09ms.sql.tencentcdb.com',
    #     user_name='root',
    #     port=26059,
    #     user_password='xemjyn-kanqoq-gImho4',
    #     db_name='Time_Series'
    # )

    import mysql.connector
    from mysql.connector import errorcode

    # Initialize variables to None for proper cleanup later
    cnx = None
    cursor = None

    try:
        # Attempt to connect to the MySQL server
        cnx = mysql.connector.connect(
            host="sh-cdb-aale09ms.sql.tencentcdb.com",
            port=26059,
            user="root",
            password="xemjyn-kanqoq-gImho4"
            # You can optionally specify a database if needed
        )
        cursor = cnx.cursor()
        print("成功")
        # Your SQL operations go here...
        db_name = 'Time_Series'
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        cursor.execute(create_db_query)
        print(f"Database '{db_name}' created successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password.")
        else:
            print(f"MySQL Error: {err}")

    except Exception as ex:
        print(f"An error occurred: {ex}")

    finally:
        # Ensure resources are cleaned up safely
        if cursor is not None:
            cursor.close()
        if cnx is not None:
            cnx.close()
