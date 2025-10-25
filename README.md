
# 🔐 Flask QR Code Authentication System

This project is a **Flask web application** that manages user authentication, QR code registration, and admin control — all backed by an **SQLite** database.  
It provides both **user** and **admin** interfaces for managing user data and QR code mappings, along with redirect functionality for QR-based links.

---

## 🧩 Features

- 👤 **User System**
  - Register with QR code, email, and password
  - Secure login (SHA-256 password hashing)
  - Edit personal details and redirect link
  - Automatic redirection based on QR code ID

- 🧑‍💼 **Admin Panel**
  - Admin login with credentials
  - Add new QR codes
  - Delete users and associated keys
  - View database contents (QR codes, users, keys)

- 🔑 **QR Code Integration**
  - Each QR code ID maps to a user and redirect link
  - New users can register directly from a QR URL

---

## ⚙️ Tech Stack

- **Python 3.9+**
- **Flask** — Web framework
- **SQLite3** — Local database
- **hashlib** — Password hashing
- **HTML Templates (Jinja2)** — For rendering pages

---

## 🏗️ Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd flask-qr-auth
````

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Suggested `requirements.txt`

```txt
flask
sqlite3
```

*(Note: `sqlite3` is included with Python by default — no separate installation required.)*

---

## 🚀 Run the App

```bash
python app.py
```

Then visit: 👉 [http://localhost:5000](http://localhost:5000)

---

## 🗃️ Database Schema (`qr_code_db.sqlite`)

### 1. `qr_codes`

| Column            | Type         | Description      |
| ----------------- | ------------ | ---------------- |
| qr_code_id        | INTEGER (PK) | Unique ID        |
| qr_code_image_url | TEXT         | Link to QR image |
| qr_code_url       | TEXT         | Encoded QR URL   |

### 2. `qr_keys`

| Column      | Type         | Description          |
| ----------- | ------------ | -------------------- |
| qr_code_id  | INTEGER (FK) | Linked to `qr_codes` |
| qr_code_url | TEXT         | URL                  |
| key         | TEXT         | Unique key           |

### 3. `user_data`

| Column       | Type         | Description                        |
| ------------ | ------------ | ---------------------------------- |
| qr_code_id   | INTEGER (FK) | Linked to QR code                  |
| name         | TEXT         | User name                          |
| email        | TEXT         | User email                         |
| password     | TEXT         | SHA-256 hashed password            |
| gender       | TEXT         | User gender                        |
| age          | INTEGER      | User age                           |
| redirectlink | TEXT         | Link to redirect after scanning QR |

---

## 🧭 App Routes Overview

| Route                         | Method    | Description                                |
| ----------------------------- | --------- | ------------------------------------------ |
| `/user_login`                 | GET, POST | User login page                            |
| `/options`                    | GET       | Displays user options after login          |
| `/edit_user_details`          | POST      | Edit user profile                          |
| `/logout`                     | GET       | Logout user                                |
| `/admin_login`                | GET, POST | Admin login                                |
| `/admin_panel`                | GET       | Admin dashboard                            |
| `/display_database`           | GET       | Shows all database tables                  |
| `/delete_user`                | GET, POST | Delete user and related key                |
| `/add_qr_code`                | GET, POST | Add new QR code record                     |
| `/<qr_code_id>`               | GET       | Redirect to user link or registration page |
| `/enter_details/<qr_code_id>` | GET, POST | Register new user via QR link              |

---

## 🔑 Default Admin Credentials

```
Username: admin  
Password: admin
```

---

## 🧩 How It Works

1. **Admin adds QR codes** (ID, image, and URL).
2. **Users scan** the QR code — if no user exists for that QR ID, they’re redirected to a registration form.
3. **User fills details** (name, email, password, gender, age, key, redirect link).
4. User data and key mapping are saved in the database.
5. **Subsequent QR scans** redirect to the stored redirect link.

---

## ⚠️ Notes

* The SQLite database path is hardcoded as:

  ```
  /home/3qq/qr_code_db.sqlite
  ```

  Change this path as needed for your environment.

* HTML templates like `user_login.html`, `admin_login.html`, `options.html`, etc., should be placed in a `templates/` directory.

* Make sure to create the database and required tables before running the app.

---

```

---

Would you like me to include an **SQL script** to automatically create the required tables (`qr_codes`, `qr_keys`, `user_data`) for this app?
```
