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

        playlist_name = input("Insert playlist name: ")
        cur.execute(
            f"SELECT * FROM playlist WHERE nome_playlist = '{playlist_name}' AND email_usuario = '{current_user.email}'")
        selected_playlist = cur.fetchone()

        if selected_playlist is None:
            print("Playlist not found!")
            continue

        music_index = 1
        while music_index >= 0:
            musics = query.musics_not_in_playlist(cur, selected_playlist[0])
            print("Avaialable musics: ")
            print("Index - Music name | Album name | Artist name")
            print("-1 - Done")
            for i, music in enumerate(musics):
                print(f"{i} - {music[1]} | {music[2]} | {music[3]}")

            music_index = int(input("Insert music index: "))
            if music_index < -1 or music_index >= len(musics):
                print("Invalid index!")
                continue
            elif music_index == -1:
                print("Done!")
                break

            cur.execute(f"INSERT INTO playlist_musica VALUES({musics[music_index][0]}, {selected_playlist[0]})")
            conn.commit()
            print("Music added successfully!")



#
#
#
#
# email_usuario = input("Insert email: ")
# nome_usuario = input("Insert name: ")
# senha = input("Insert password: ")
#
#
# cur.execute("INSERT INTO usuario VALUES"
#             f"('{email_usuario}', '{nome_usuario}', '{senha}')")
#
# conn.commit()
