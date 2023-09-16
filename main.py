import psycopg2
import reset
import os
from user import User
import query

DB_HOST = "localhost"
DB_NAME = "finimusic"
DB_USER = "admin"
DB_PASS = "123"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
print("Connection successful!")
print(f"Connected to {DB_NAME}.")
cur = conn.cursor()

while True:
    print("1 - Access DB")
    print("2 - Reset and Access DB")
    print("3 - Exit")
    option = input("Choose an option: ")
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 100)

    if option == "2":
        reset.run(cur, conn)
        print("Reset successful!")
        break
    elif option == "3":
        exit()
    elif option == "1":
        break
    else:
        print("Invalid option!")

while True:
    print("1 - Login")
    print("2 - Register")
    print("3 - Exit")
    option = input("Choose an option: ")
    print("\n" * 100)

    if option == "1":
        print("------------------USER LOGIN------------------")
        email = input("Insert email: ")
        password = input("Insert password: ")

        current_user = User("", email, password)

        cur.execute(f"SELECT * FROM usuario WHERE email_usuario = '{email}' AND senha = '{password}'")

        return_value = cur.fetchone()

        if return_value is None:
            print("Invalid email or password!")
        else:
            current_user.name = return_value[1]
            print("Login successful!")
            break
    elif option == "2":
        print("------------------USER REGISTER------------------")
        email = input("Insert email: ")
        name = input("Insert name: ")
        password = input("Insert password: ")

        current_user = User(name, email, password)

        cur.execute(f"SELECT * FROM usuario WHERE email_usuario = '{email}'")
        if cur.fetchone() is not None:
            print("Email already registered!")
        else:
            cur.execute(f"INSERT INTO usuario VALUES {current_user.sql_format()}")
            conn.commit()
            print("Register successful!")
            break
    elif option == "3":
        exit()
    else:
        print("Invalid option!")

while True:
    print("------------------MENU------------------")
    print("Currently logged as: " + current_user.name)
    print("Playlists: ")
    cur.execute(f"SELECT * FROM playlist WHERE email_usuario = '{current_user.email}'")
    playlists = cur.fetchall()
    for playlist in playlists:
        print(playlist[1])

    print("1 - Create playlist")
    print("2 - Add music to playlist")
    print("3 - Remove music from playlist")
    print("4 - Delete playlist")
    print("5 - Show playlists musics")
    print("6 - Exit")
    option = input("Choose an option: ")
    print("\n" * 100)

    if option == "1":
        print("------------------CREATE PLAYLIST------------------")
        query.create_playlist(cur, conn, current_user)
        print("Playlist created successfully!")

    elif option == "2":
        print("------------------ADD MUSIC TO PLAYLIST------------------")
        query.add_music_playlist(cur, conn, current_user)
        print("Music added successfully!")
