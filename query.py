from datetime import timedelta


def create_playlist(cur, conn, current_user):
    print("------------------CREATE PLAYLIST------------------")
    name = input("Insert playlist name: ")

    cur.execute(f"SELECT * FROM playlist WHERE nome_playlist = '{name}' AND email_usuario = '{current_user.email}'")
    if cur.fetchone() is not None:
        print("Playlist already exists!")
    else:
        cur.execute(f"INSERT INTO playlist (nome_playlist, email_usuario) VALUES ('{name}', '{current_user.email}')")
        conn.commit()


def musics_not_in_playlist(cur, id_playlist):
    cur.execute(f"SELECT id_musica, nome_musica, nome_album, nome_artista FROM musica "
                f"NATURAL JOIN album "
                f"NATURAL JOIN artista "
                f"WHERE id_musica NOT IN(SELECT id_musica FROM playlist_musica WHERE id_playlist = {id_playlist})")
    return cur.fetchall()


def musics_in_playlist(cur, id_playlist):
    cur.execute(f"SELECT id_musica, nome_musica, nome_album, nome_artista FROM musica "
                f"NATURAL JOIN album "
                f"NATURAL JOIN artista "
                f"WHERE id_musica IN(SELECT id_musica FROM playlist_musica WHERE id_playlist = {id_playlist})")
    return cur.fetchall()


def add_music_playlist(cur, conn, current_user):
    while True:
        playlist_name = input("Insert playlist name: ")
        cur.execute(
            f"SELECT * FROM playlist WHERE nome_playlist = '{playlist_name}' AND email_usuario = '{current_user.email}'")
        selected_playlist = cur.fetchone()

        if selected_playlist is None:
            print("Playlist not found!")
            continue
        else:
            break

    music_index = 1
    while music_index >= 0:
        musics = musics_not_in_playlist(cur, selected_playlist[0])
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


def remove_music_playlist(cur, conn, current_user):
    playlist_name = input("Insert playlist name: ")
    cur.execute(
        f"SELECT * FROM playlist WHERE nome_playlist = '{playlist_name}' AND email_usuario = '{current_user.email}'")
    selected_playlist = cur.fetchone()

    if selected_playlist is None:
        print("Playlist not found!")
        return

    music_index = 1
    while music_index >= 0:
        musics = musics_in_playlist(cur, selected_playlist[0])
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

        cur.execute(
            f"DELETE FROM playlist_musica WHERE id_musica = {musics[music_index][0]} AND id_playlist = {selected_playlist[0]}")
        conn.commit()
        print("Music added successfully!")
        print("Music removed successfully!")


def delete_playlist(cur, conn, current_user):
    # Call method to display all playlists
    # UNDER CONSTRUCTION BY Ferrao
    playlist_name = input("Insert playlist name: ")
    cur.execute(
        f"SELECT * FROM playlist WHERE nome_playlist = '{playlist_name}' AND email_usuario = '{current_user.email}'")
    selected_playlist = cur.fetchone()

    if selected_playlist is None:
        print("Playlist not found!")
        return

    cur.execute(f"DELETE FROM playlist_musica WHERE id_playlist = {selected_playlist[0]}")
    cur.execute(f"DELETE FROM playlist WHERE id_playlist = {selected_playlist[0]}")
    conn.commit()
    print("Playlist deleted successfully!")


def show_playlists_musics(cur, current_user):
    cur.execute(f"SELECT id_playlist, nome_playlist FROM playlist "
                f"WHERE email_usuario = '{current_user.email}'")

    user_playlists = cur.fetchall()

    for playlist in user_playlists:
        cur.execute(f"SELECT nome_musica, nome_album, nome_artista, SUM(duracao) FROM musica "
                    f"NATURAL JOIN album "
                    f"NATURAL JOIN artista "
                    f"NATURAL JOIN playlist_musica "
                    f"WHERE id_playlist = {playlist[0]}")

        print(f"Playlist: {playlist[1]}")

        musics = cur.fetchall()

        print(musics)

        for music in musics:
            print(f"Music: {music[0]} | Album: {music[1]} | Artist: {music[2]}")
        print("\n")

