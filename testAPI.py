import requests
import json
import time
import numpy as np
from astropy.table import Table
from astropy.io import fits
import io
import cv2

def upload_image_API(image : str) -> None:
    api_url : str = ""
    R : requests = None
    session_id : str = ""
    f : str = ""
    file_args : tuple = ()
    subid : str = ""
    status : str = ""
    result : dict = {}
    job_id : int = 0
    job_status : dict = {}
    
    # URL of the API
    api_url = "http://nova.astrometry.net/api/"

    # Login
    R = requests.post(f"{api_url}login", data={'request-json': json.dumps({"apikey": "axcybncczwmrpsij"})})
    # print("Login : ", R.text)

    session_id = R.json()
    session_id = session_id.get("session")
    
    if session_id is None:
        print("Login failed")
        return None

    # Upload the image in local
    try:
        f = open(image, 'rb')
        file_args = (image, f.read())
    except IOError:
        print("File %s does not exist" % image)
        raise

    # Upload the image to the API
    upload = requests.post(f"{api_url}upload", files={'file': file_args}, data={'request-json': json.dumps({"session": session_id})})
    # print("Upload : ", upload.text)

    upload_json = upload.json()
    subid = upload_json.get('subid')
    
    if subid is None:
        print("Upload failed")
        return None

    while True:
        # Get the status of the job
        result = requests.get(f"{api_url}submissions/{subid}", params={'session': session_id}).json()
        job = result.get('jobs', [])
        
        # Check if a job ID has been generated
        if job and job[0] is not None:   
            job_id = job[0]       
              
            # Check if this job is finished (success)
            job_status = requests.get(f"{api_url}jobs/{job_id}/info").json()
            status = job_status.get('status')
            if status == "success":
                print(f"Success ! Generation of the mask for the Job {job_id}.")
                make_mask(job_id)
                break
            
            elif status == "failure":
                print("Astrometry failed on this image.")
                break
            else:
                print(f"Job {job_id} in progress... Status: {status}")
        else:
            print("Waiting for the creation of the Job...")

        time.sleep(10) # Wait before the next check



def make_mask(job_id : int)-> None:     
    r : requests = None
    width : int = 0
    height : int = 0
    x_coords : list = []
    y_coords : list = []
    mask : np.ndarray = None
    x : int = 0
    y : int = 0
    radius : int = 3
    color : int = 255
    thickness : int = -1
       
    # Downloading the file containing the detected stars
    r = requests.get(f"http://nova.astrometry.net/axy_file/{job_id}")
    
    # Content type check
    if r.status_code != 200:
        print(f"Error HTTP : {r.status_code}")
        return None

    try:
        with fits.open(io.BytesIO(r.content)) as hdul:
            # Recovering of dimensions
            header = hdul[0].header
            width = header.get('IMAGEW')
            height = header.get('IMAGEH')
            
            if not width or not height:
                raise ValueError("IMAGEW/IMAGEH dimensions not found in FITS")

            # Recovering of star coordinates
            data_table = Table.read(hdul[1])
            x_coords = data_table['X']
            y_coords = data_table['Y']

        # Creation of the mask
        mask = np.zeros((height, width), dtype=np.uint8)
        for x, y in zip(x_coords, y_coords):
            cv2.circle(mask, (int(x), int(y)), radius, color, thickness)
            
        cv2.imwrite("masque_API.png", mask)

    except Exception as e:
        print(f"Error while reading the FITS : {e}")
        return None
    
upload_image_API("./examples/test_M31_linear.fits")