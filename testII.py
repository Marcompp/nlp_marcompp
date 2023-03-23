import requests
import numpy as np

specieslist = []

response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')
print(response.status_code)  # 200 if successful
res = response.json()  # response content as a JSON object

for re in res["results"]:
    specieslist.append(re["name"])
print(specieslist)
np.savetxt("pokelist.txt", specieslist, delimiter=',',fmt='%s')
pokelist = np.loadtxt("pokelist.txt", delimiter=',',dtype='str')
print(pokelist)