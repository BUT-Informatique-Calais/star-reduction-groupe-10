import requests
import json
import time
from PIL import Image
import numpy as np

api_url = "http://nova.astrometry.net/api/"

R = requests.post(f"{api_url}login", data={'request-json': json.dumps({"apikey": "axcybncczwmrpsij"})})
print(R.text)

session_id = R.json()
session_id = session_id.get("session")
print(session_id)

try:
    fn = 'examples/test_M31_linear.fits'
    f = open(fn, 'rb')
    file_args = (fn, f.read())
except IOError:
    print('File %s does not exist' % fn)
    raise

upload = requests.post(f"{api_url}upload", files={'file': file_args}, data={'request-json': json.dumps({"session": session_id})})

print("status", upload.status_code)
print("Content", upload.text)

upload_json = upload.json()
subid = upload_json.get('subid')
print(subid)

while True:
    result = requests.get(f"{api_url}submissions/{subid}", params={'session': session_id}).json()
    status = result['jobs'][0]['status']
    print(f"Statut actuel : {status}")

    if status in ['success', 'failure']:
        break
    time.sleep(10)  # Attendre 10 secondes

status = 'success'
    
if status == 'success':
    job_id = 14999132
    print("ID de job :", job_id)

    # Récupération des annotations d'étoiles
    annotations = requests.get(f"{api_url}jobs/{job_id}/annotations", params={'session': session_id}).json()
    stars = annotations
    print(json.dumps(annotations, indent=2))  # Affiche les annotations de manière lisible
    print(stars)
    print("Étoiles détectées :", len(stars))
    
else:
    print("Échec de l'analyse.")
    
    
# Charger l'image
image = np.array(Image.open('./results/original.png').convert('L'))

# Créer un masque vide
mask = np.zeros_like(image, dtype=np.uint8)

# Marquer les étoiles (exemple simplifié)
for star in stars:
    x, y = star['x'], star['y']
    mask[y, x] = 255  # Marquer en blanc

# Sauvegarder le masque
Image.fromarray(mask).save('masque_etoiles.png')
