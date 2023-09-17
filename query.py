from datetime import timedelta


def create_playlist(cur, conn, current_user):
    name = input("Insert playlist name: ")

    cur.execute(f"SELECT * FROM playlist WHERE nome_playlist = '{name}' AND email_usuario = '{current_user.email}'")
    if cur.fetchone() is not None:
        print("Playlist already exists!")
    else:
        cur.execute(f"INSERT INTO playlist (nome_playlist, email_usuario) VALUES ('{name}', '{current_user.email}')")
        conn.commit()
        print("Playlist created successfully!")


def musics_not_in_playlist(cur, id_playlist):
    cur.execute(f"SELECT id_musica, nome_musica, nome_album, nome_artista FROM musica "
                f"NATURAL JOIN album "
                f"NATURAL JOIN artista "
                f"WHERE id_musica NOT IN(SELECT id_musica FROM playlist_musica WHERE id_playlist = {id_playlist})")
    return cur.fetchall()


def musics_in_playlist(cur, id_playlist):
    cur.execute(f"SELECT id_musica, nome_musica, nome_album, nome_artista, visualizacoes FROM musica "
                f"NATURAL JOIN album "
                f"NATURAL JOIN artista "
                f"WHERE id_musica IN(SELECT id_musica FROM playlist_musica WHERE id_playlist = {id_playlist})"
                f"ORDER BY visualizacoes DESC, nome_musica ASC")
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
        print("Music removed successfully!")


def delete_playlist(cur, conn, current_user):
    # Call method to display all playlists
    show_playlists_musics(cur, current_user)
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
        playlist_musics = musics_in_playlist(cur, playlist[0])

        cur.execute(f"SELECT SUM(duracao) FROM playlist "
                    f"NATURAL JOIN playlist_musica "
                    f"NATURAL JOIN musica "
                    f"WHERE id_playlist = {playlist[0]} "
                    f"GROUP BY id_playlist")
        playlist_duration = cur.fetchone()

        print(f"Playlist: {playlist[1]} - Duration: {timedelta(seconds=playlist_duration[0])}")
        for music in playlist_musics:
            print(f"|----- Music: {music[1]} | Album: {music[2]} | Artist: {music[3]} | Views: {music[4]}")
    print("\n")
    input("Press enter to continue...")


def display_genres_w_id(cur):
    cur.execute(f"SELECT * FROM genero")
    genres = cur.fetchall()

    for genre in genres:
        print(f"{genre[0]} - {genre[1]}")

    return len(genres)


def filtered_search(cur, current_user):
    cur.execute(f"SELECT id_playlist, nome_playlist FROM playlist "
                f"WHERE email_usuario = '{current_user.email}'")

    user_playlists = cur.fetchall()

    print("Choose what to filter: ")
    print("1 - Filter by artist")
    print("2 - Filter by album")
    print("3 - Filter by genre\n")

    option = input("Choose an option: ")
    match option:
        case "1":
            filter_element = "UPPER('" + input("Insert artist name: ") + "')"
            filter_field = "UPPER(nome_artista)"

        case "2":
            filter_element = "UPPER('" + input("Insert album name: ") + "')"
            filter_field = "UPPER(nome_album)"

        case "3":
            print("Available genres: ")
            num_genres = display_genres_w_id(cur)
            filter_field = "id_genero"
            filter_element = int(input("\nInsert genre id to filter: "))

            if filter_element < 0 or filter_element >= num_genres:
                print("Invalid genre id!")
                return

        case _:
            print("Invalid filter option!")
            return

    for playlist in user_playlists:
        cur.execute(f"SELECT nome_genero, nome_musica, nome_album, nome_artista FROM musica "
                    f"NATURAL JOIN album "
                    f"NATURAL JOIN artista "
                    f"NATURAL JOIN genero_musica "
                    f"NATURAL JOIN genero "
                    f"NATURAL JOIN playlist_musica "
                    f"WHERE id_playlist = {playlist[0]} AND {filter_field} = {filter_element}")

        print(f"Playlist: {playlist[1]}")

        musics = cur.fetchall()

        if len(musics) != 0:
            for music in musics:
                print(f"|----- Genre: {music[0]} | Music: {music[1]} | Album: {music[2]} | Artist: {music[3]}")
        else:
            print("No matches found...")

        print("\n")
        input("Press enter to continue...")


def play_music(cur, conn, current_user):
    cur.execute(f"SELECT id_playlist, nome_playlist FROM playlist "
                f"WHERE email_usuario = '{current_user.email}'")

    user_playlists = cur.fetchall()

    print("Choose playlist to play: ")
    for i, playlist in enumerate(user_playlists):
        print(f"{i} - {playlist[1]}")

    playlist_index = int(input("Insert playlist index: "))
    if playlist_index < 0 or playlist_index >= len(user_playlists):
        print("Invalid index!")
        return

    playlist_musics = musics_in_playlist(cur, user_playlists[playlist_index][0])

    print("Choose music to play: ")
    for i, music in enumerate(playlist_musics):
        print(f"{i} - Music: {music[1]} | Album: {music[2]} | Artist: {music[3]}")

    music_index = int(input("Insert music index: "))
    if music_index < 0 or music_index >= len(playlist_musics):
        print("Invalid index!")
        return

    cur.execute(f"UPDATE musica SET visualizacoes = visualizacoes + 1 "
                f"WHERE id_musica = {playlist_musics[music_index][0]}")
    conn.commit()
    music_name = playlist_musics[music_index][1]

    print(f"Playing {music_name}...")
    print("\n")
    input("Press enter to continue...")