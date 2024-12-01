def city_functions(city, country, population=0):
    if population == 0:
        result = f'{city.title()}, {country.title()}'
    else:
        result = f'{city.title()}, {country.title()} - population {population}'
    return result
