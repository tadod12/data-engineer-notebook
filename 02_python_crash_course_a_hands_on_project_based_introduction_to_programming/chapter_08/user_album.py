def make_album(artist, title):
    dic = {
        'artist': artist,
        'title': title
    }
    return dic


flag = True
albums = []
while flag:
    artist = input("Enter Artist: ")
    title = input("Enter Title: ")
    albums.append(make_album(artist, title))
    if input('Another? ') == 'no':
        flag = False
print(albums)
