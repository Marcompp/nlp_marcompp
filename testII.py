import requests

response = requests.get('https://pokeapi.co/api/v2/pokemon/'+'eevee')
print(response.status_code)  # 200 if successful
print(response.json())  # response content as a JSON object

print("Types: "+str(response.json()['types']))
