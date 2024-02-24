import sqlite3

def create_database_and_tables():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('qr_code_db.sqlite')

        # Create a cursor object
        cursor = conn.cursor()

        # Create qr_codes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qr_codes (
                qr_code_id INTEGER PRIMARY KEY,
                qr_code_image_url VARCHAR(255),
                qr_code_url VARCHAR(255) UNIQUE   
            )
        """)
        print("qr_codes table created successfully")

        # Insert data into qr_codes table
        cursor.executemany("""
            INSERT OR IGNORE INTO qr_codes (qr_code_id, qr_code_image_url, qr_code_url) 
            VALUES (?, ?, ?)
        """, [
            (1, 'image/1.png', 'https://3qq.pythonanywhere.com/1'),
            (2, 'image/2.png', 'https://3qq.pythonanywhere.com/2'),
            (3, 'image/3.png', 'https://3qq.pythonanywhere.com/3'),
            (4, 'image/4.png', 'https://3qq.pythonanywhere.com/4'),
            (5, 'image/5.png', 'https://3qq.pythonanywhere.com/5'),
            (6, 'image/6.png', 'https://3qq.pythonanywhere.com/6'),
            (7, 'image/7.png', 'https://3qq.pythonanywhere.com/7'),
            (8, 'image/8.png', 'https://3qq.pythonanywhere.com/8'),
            (9, 'image/9.png', 'https://3qq.pythonanywhere.com/9'),
            (10, 'image/10.png', 'https://3qq.pythonanywhere.com/10')
        ])
        conn.commit()

        # Create qr_keys table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qr_keys (
                id INT AUTO_INCREMENT PRIMARY KEY,
                qr_code_id INT UNIQUE,
                qr_code_url VARCHAR(255),
                `key` VARCHAR(255) UNIQUE,
                FOREIGN KEY (qr_code_url) REFERENCES qr_codes(qr_code_url)
            )
        """)
        print("qr_keys table created successfully")

        # Create user_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                qr_code_id INT,
                password VARCHAR(255),
                email VARCHAR(100),
                name  VARCHAR(36),
                gender TEXT,
                age INT,
                redirectlink VARCHAR(255),
                FOREIGN KEY (qr_code_id) REFERENCES qr_codes(qr_code_id)
            )
        """)
        print("user_data table created successfully")

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_database_and_tables()
