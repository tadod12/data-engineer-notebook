favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

names = {'jen', 'phil', 'edward', 'dodat', 'lby', 'sarah'}
for name in names:
    if name in favorite_languages.keys():
        print(f'Thank {name.title()} for responding!')
    else:
        print(f'{name.title()}, please take the poll.')
