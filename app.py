from flask import Flask, redirect, request, render_template,session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to store user details in the database
def store_user_details(name, email, password, gender, age, qr_code_id,redirectlink):
    conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_data (qr_code_id, name, email, password, gender, age, redirectlink) VALUES (?, ?, ?, ?, ?, ?,?)",
                       (qr_code_id, name, email, hash_password(password), gender, age, redirectlink))
        conn.commit()
    except sqlite3.Error as e:
        print("Error occurred while inserting user data:", e)
    finally:
        conn.close()

# Function to store the mapping of keys with QR codes
def store_key_mapping(qr_code_id, qr_code_url, key):
    conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO qr_keys (qr_code_id, qr_code_url, `key`) VALUES (?, ?, ?)", (qr_code_id, qr_code_url, key))
        conn.commit()
    except sqlite3.Error as e:
        print("Error occurred while inserting key mapping:", e)
    finally:
        conn.close()


# Function to authenticate user login
def authenticate_user(email, password):
    conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE email = ?", (email,))
    user = cursor.fetchone()
    print(user)
    conn.close()
    if user and user[2] == hash_password(password):
        return user
    return None

# Function to fetch user data
def get_user_data(email):
    conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE email = ?", (email,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# User login route
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)
        if user:
            session['logged_in'] = True
            session['email'] = email
            return redirect('/options')
        else:
            return "Invalid email/password combination. Please try again."
    return render_template('user_login.html')

# Options route after user login
@app.route('/options')
def options():
    if session.get('logged_in'):
        email = session['email']
        user_data = get_user_data(email)
        return render_template('options.html', user_data=user_data)
    else:
        return redirect('/user_login')

# Edit user details route
@app.route('/edit_user_details', methods=['GET','POST'])
def edit_user_details():
    if session.get('logged_in'):
        email = session['email']
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        redirectlink = request.form['redirectlink']
        password = request.form['password']
        # Update user details in the database
        conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_data SET name=?, gender=?, age=? , redirectlink=?, password=? WHERE email=?", (name, gender, age,redirectlink, password, email))
        conn.commit()
        conn.close()
        return redirect('/options')
    else:
        return redirect('/user_login')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect('/user_login')


# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect('/admin_panel')
        else:
            return "Invalid credentials. Please try again."
    return render_template('admin_login.html')

# Admin panel route
@app.route('/admin_panel')
def admin_panel():
    if session.get('logged_in'):
        return render_template('admin_panel.html')
    else:
        return redirect('/admin_login')

# Logout route
@app.route('/adminlogout')
def logout():
    session.pop('logged_in', None)
    return redirect('/admin_login')

# Display database route
@app.route('/display_database')
def display_database():
    if session.get('logged_in'):
        try:
            conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
            cursor = conn.cursor()

            # Fetch data from qr_codes table
            cursor.execute("SELECT * FROM qr_codes")
            qr_codes_data = cursor.fetchall()

            # Fetch data from keys table
            cursor.execute("SELECT * FROM qr_keys")
            keys_data = cursor.fetchall()

            # Fetch data from user_data table
            cursor.execute("SELECT * FROM user_data")
            user_data = cursor.fetchall()

            # Close connection
            conn.close()

            return render_template('display_database.html', qr_codes_data=qr_codes_data, keys_data=keys_data, user_data=user_data)
        except sqlite3.Error as e:
            return f"Error occurred: {e}"
    else:
        return redirect('/admin_login')



# Delete user route
@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if session.get('logged_in'):
        if request.method == 'POST':
            # Process form data to delete user
            user_id = request.form['user_id']

            try:
                conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
                cursor = conn.cursor()
                # Delete user data
                cursor.execute("DELETE FROM user_data WHERE qr_code_id = ?", (user_id,))
                # Delete corresponding key
                cursor.execute("DELETE FROM qr_keys WHERE qr_code_id = ?", (user_id,))
                conn.commit()
                conn.close()
                return "User and corresponding key deleted successfully."
            except sqlite3.Error as e:
                return f"Error occurred: {e}"
        else:
            # Fetch user data for selection
            try:
                conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
                cursor = conn.cursor()
                cursor.execute("SELECT qr_code_id, name FROM user_data")
                user_data = cursor.fetchall()
                conn.close()
                return render_template('delete_user.html', user_data=user_data)
            except sqlite3.Error as e:
                return f"Error occurred: {e}"
    else:
        return redirect('/admin_login')



# Add QR code route
@app.route('/add_qr_code', methods=['GET', 'POST'])
def add_qr_code():
    if session.get('logged_in'):
        if request.method == 'POST':
            # Process form data to add QR code
            qr_code_id = request.form['qr_code_id']
            qr_code_image_url = request.form['qr_code_image_url']
            qr_code_url = request.form['qr_code_url']

            try:
                conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO qr_codes (qr_code_id, qr_code_image_url, qr_code_url) VALUES (?, ?, ?)",
                               (qr_code_id, qr_code_image_url, qr_code_url))
                conn.commit()
                conn.close()
                return "QR Code added successfully."
            except sqlite3.Error as e:
                return f"Error occurred: {e}"
        return render_template('add_qr_code.html')
    else:
        return redirect('/admin_login')


@app.route('/<int:qr_code_id>')
def handle_qr_code(qr_code_id):
    conn = sqlite3.connect('/home/3qq/qr_code_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE qr_code_id = ?", (qr_code_id,))
    redirect_link = cursor.fetchone()
    conn.close()

    if redirect_link:
        return redirect(redirect_link[7])
    else:
        return redirect(f"/enter_details/{qr_code_id}")

# Enter user details
@app.route('/enter_details/<int:qr_code_id>', methods=['GET', 'POST'])
def enter_details(qr_code_id):
    if request.method == 'POST':
        key = request.form['key']  # Take the key from user input
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        age = request.form['age']
        redirectlink=request.form['redirectlink']

        try:
            store_user_details(name, email, password, gender, age, qr_code_id,redirectlink)
            store_key_mapping(qr_code_id, f'https://3qq.pythonanywhere.com/{qr_code_id}', key)  # Store key
            return """
            <script>
                alert('Details saved successfully!');
                window.location = '/user_login';  // Redirect to home page or any other desired page
            </script>
            """
        except sqlite3.Error as e:
            return f"Error occurred: {e}"

    return """
    <style>
        form {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        input[type="text"],
        input[type="email"],
        input[type="password"],
        input[type="number"],
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
    <form method="post">
        <label for="name">Name:</label>
        <input type="text" name="name" id="name" required>

        <label for="email">Email:</label>
        <input type="email" name="email" id="email" required>

        <label for="password">Password:</label>
        <input type="password" name="password" id="password" required>

        <label for="gender">Gender:</label>
        <input type="text" name="gender" id="gender" required>

        <label for="age">Age:</label>
        <input type="number" name="age" id="age" required>

        <label for="key">Key:</label>
        <input type="text" name="key" id="key" required>

        <label for="redirectlink">Redirect Link:</label>
        <input type="text" name="redirectlink" id="redirectlink" required>

        <input type="submit" value="Submit">
    </form>
    """


if __name__ == '__main__':
    app.run(debug=True)