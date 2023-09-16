def create_playlist(cur, conn, current_user):
    print("------------------CREATE PLAYLIST------------------")
    name = input("Insert playlist name: ")

    cur.execute(f"SELECT * FROM playlist WHERE nome_playlist = '{name}' AND email_usuario = '{current_user.email}'")
    if cur.fetchone() is not None:
        print("Playlist already exists!")
    else:
        cur.execute(f"INSERT INTO playlist (nome_playlist, email_usuario) VALUES ('{name}', '{current_user.email}')")
        conn.commit()

