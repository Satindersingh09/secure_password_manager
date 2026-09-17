This is a simple terminal-based password manager made using Python and MySQL.

The program allows users to create an account and securely manage saved website passwords.

Features
Register
Login
Add password
View saved passwords
Show password
Edit password
Delete password
Generate passwords
MySQL database
Technologies
Python
MySQL
Cryptography
Werkzeug
mysql-connector-python
python-dotenv
Database

The project uses MySQL.

Create the database using:

CREATE DATABASE secure_password_manager;

The program creates the required tables automatically.

Database Schema

users

Column	Type	Notes
id	INT	Primary key, auto increment
username	VARCHAR(80)	Unique, not null
password_hash	VARCHAR(255)	Hashed with Werkzeug, not null

passwords

Column	Type	Notes
id	INT	Primary key, auto increment
user_id	INT	Foreign key referencing users(id)
website	VARCHAR(150)	Not null
username	VARCHAR(150)	Not null
encrypted_password	TEXT	Encrypted with Fernet, not null
Security

User account passwords are hashed using Werkzeug.

Saved website passwords are encrypted using Fernet.

SQL queries use parameters instead of directly adding user input to SQL statements.

Users can only access password entries belonging to their own account.

Running the Project

Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Create the MySQL database.

Create a .env file with the database information and encryption key.

Run the program:

python app.py
Project Files

app.py
Main program and menu system.

config.py
Contains database configuration.

models.py
Connects to MySQL and creates the database tables.

encryption.py
Encrypts and decrypts saved passwords.

password_generator.py
Generates random passwords.

requirements.txt
Contains the Python packages.

README.md
Project documentation.