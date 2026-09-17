from getpass import getpass

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models import connect_db
from models import create_tables

from encryption import encrypt_password
from encryption import decrypt_password

from password_generator import generate_password


def register():
    print("\n--- Register ---")
    username = input("Username: ")
    password = getpass("Password: ")

    db = connect_db()
    cursor = db.cursor()
    password_hash = generate_password_hash(password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (%s, %s)
            """,
            (username, password_hash)
        )
        db.commit()
        print("Account created.")
    except:
        print("Username already exists.")

    cursor.close()
    db.close()


def login():
    print("\n--- Login ---")
    username = input("Username: ")
    password = getpass("Password: ")

    db = connect_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            SELECT id, password_hash
            FROM users
            WHERE username = %s
            """,
            (username,)
        )
        user = cursor.fetchone()
    except:
        print("Something went wrong.")
        cursor.close()
        db.close()
        return None

    cursor.close()
    db.close()

    if user:
        if check_password_hash(user[1], password):
            print("Login successful.")
            return user[0]

    print("Invalid username or password.")
    return None


def add_password(user_id):
    print("\n--- Add Password ---")
    website = input("Website: ")
    username = input("Username: ")
    password = getpass("Password: ")
    encrypted = encrypt_password(password)

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO passwords
        (user_id, website, username, encrypted_password)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, website, username, encrypted)
    )
    db.commit()
    cursor.close()
    db.close()
    print("Password saved.")


def view_passwords(user_id):
    print("\n--- Saved Passwords ---")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, website, username FROM passwords WHERE user_id = %s", (user_id,))
    passwords = cursor.fetchall()

    if not passwords:
        print("No passwords saved.")

    for password in passwords:
        print(password[0], "-", password[1], "-", password[2])

    cursor.close()
    db.close()


def show_password(user_id):
    view_passwords(user_id)
    entry_id = input("\nEnter password ID: ")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT website, username, encrypted_password
        FROM passwords
        WHERE id = %s AND user_id = %s
        """,
        (entry_id, user_id)
    )
    password = cursor.fetchone()
    cursor.close()
    db.close()

    if password:
        decrypted = decrypt_password(password[2])
        print("\nWebsite:", password[0])
        print("Username:", password[1])
        print("Password:", decrypted)
    else:
        print("Password not found.")


def generate_new_password():
    password = generate_password()
    print("\nGenerated password:")
    print(password)


def edit_password(user_id):
    view_passwords(user_id)
    entry_id = input("\nEnter password ID: ")
    website = input("New website: ")
    username = input("New username: ")
    password = getpass("New password: ")
    encrypted = encrypt_password(password)

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE passwords
        SET website = %s,
            username = %s,
            encrypted_password = %s
        WHERE id = %s AND user_id = %s
        """,
        (website, username, encrypted, entry_id, user_id)
    )
    db.commit()

    if cursor.rowcount == 1:
        print("Password updated.")
    else:
        print("Password not found.")

    db.close()


def delete_password(user_id):
    view_passwords(user_id)
    entry_id = input("\nEnter password ID: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM passwords
        WHERE id = %s AND user_id = %s
        """,
        (entry_id, user_id)
    )
    conn.commit()

    if cursor.rowcount == 1:
        print("Password deleted.")
    else:
        print("Password not found.")

    cursor.close()
    conn.close()


def password_menu(user_id):
    while True:
        print("-----------------------------")
        print("          MAIN MENU")
        print("-----------------------------")
        print("1. Add password")
        print("2. View passwords")
        print("3. Show password")
        print("4. Generate password")
        print("5. Edit password")
        print("6. Delete password")
        print("7. Logout")

        choice = input("\nChoose: ")

        if choice == "1":
            add_password(user_id)
        elif choice == "2":
            view_passwords(user_id)
        elif choice == "3":
            show_password(user_id)
        elif choice == "4":
            generate_new_password()
        elif choice == "5":
            edit_password(user_id)
        elif choice == "6":
            delete_password(user_id)
        elif choice == "7":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def main():
    create_tables()

    while True:
        print("-----------------------------")
        print("   SECURE PASSWORD MANAGER")
        print("-----------------------------")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nChoose: ")

        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
            if user_id:
                password_menu(user_id)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()