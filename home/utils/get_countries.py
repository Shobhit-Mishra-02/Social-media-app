import requests

def get_country_names():
    res = requests.get("https://restcountries.com/v3.1/independent?status=true&fields=name")
    
    data = []

    for country in res.json():
        name_in_tuple = (country['name']['common'], country['name']['common'])
        data.append(name_in_tuple) 

    return data
