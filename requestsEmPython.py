import requests


def callurl(url):
    
    response = requests.get(url)
    if response.status_code == 200:
        jsonData = response.json()
        results = jsonData["results"]
        firstPkemon = results[0]
        #print(firstPkemon)

       
        urlFirstPokemon = firstPkemon['url']
        newResponse = requests.get(urlFirstPokemon)
        if newResponse.status_code == 200:
            firstPkemonData = newResponse.json()
            types = firstPkemonData["types"]
            print(types)
            print(types[0])
            print(types[0]['type']['name'])


def main():
    callurl('https://pokeapi.co/api/v2/pokemon')
    

main()