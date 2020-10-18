import json
import sys
import os
try:
    import requests
    from dotenv import load_dotenv
except:
    print("Missing packages, run pip install -r requirements")
    print("ALSO: I strongly recommend using a virtual environment. See my docker image or create a virtual python environment")

load_dotenv()

url = "https://maps.googleapis.com/maps/api/directions/json?mode=bicycling&origin=%s&destination=%s&key=%s" % (("%s,%s" % (59.919111, 10.736179)), ("%s,%s" % (59.9121109, 10.7661939)), os.getenv("API_KEY"))

res = requests.get(url)
j = res.json()
print(j)

