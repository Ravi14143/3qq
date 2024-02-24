import sqlite3

def display_tables_data():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('qr_code_db.sqlite')

        # Create a cursor object
        cursor = conn.cursor()

        # Display qr_codes table data
        cursor.execute("SELECT * FROM qr_codes")
        qr_codes_data = cursor.fetchall()
        print("qr_codes table data:")
        for row in qr_codes_data:
            print(row)

        # Display qr_keys table data
        cursor.execute("SELECT * FROM qr_keys")
        qr_keys_data = cursor.fetchall()
        print("\nqr_keys table data:")
        for row in qr_keys_data:
            print(row)

        # Display user_data table data
        cursor.execute("SELECT * FROM user_data")
        user_data = cursor.fetchall()
        print("\nuser_data table data:")
        for row in user_data:
            print(row)

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    display_tables_data()
