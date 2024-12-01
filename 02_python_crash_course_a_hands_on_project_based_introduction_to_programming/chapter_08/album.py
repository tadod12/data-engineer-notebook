def make_album(artist, title):
    dic = {
        'artist': artist,
        'title': title
    }
    return dic


album_0 = make_album('MCK', '99%')
album_1 = make_album('Zomboy', 'Lone Wolf')
album_2 = make_album('Virtual Riot', 'Still Kids')
print(album_0)
print(album_1)
print(album_2)
