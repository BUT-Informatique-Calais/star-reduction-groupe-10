import requests
import json

R = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": "axcybncczwmrpsij"})})
print(R.text)

session_id = R.json()
session_id = session_id.get("session")
print(session_id)
