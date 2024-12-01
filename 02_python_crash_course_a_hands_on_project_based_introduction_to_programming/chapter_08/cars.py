def make_car(manufacturer, model, **info):
    info['manufacturer'] = manufacturer
    info['model'] = model
    return info


car = make_car('subaru', 'outback', color='blue', tow_package='True')
print(car)
