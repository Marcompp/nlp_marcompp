import http.client

conn = http.client.HTTPConnection("pokeapi.co")

#https://pokeapi.co/api/v2/pokemon/

print(conn)

payload = "{}"

payload = "eevee"
conn.request("GET", "/api/v2/pokemon/", payload)


res = conn.getresponse()
data = res.read()
print(res.status)
print(data.decode("utf-8")) 