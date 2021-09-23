import requests

r = requests.post("http://localhost:13000/client", headers={'Content-type': 'application/json'}, json={"name": "jon", "surname": "aizpuru"})
print(r.content)
r = requests.get("http://localhost:13000/clients")
print(r.content)
r = requests.delete("http://localhost:13000/client/2")
print(r.content)