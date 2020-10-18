import json
import sys
try:
    from dotenv import load_dotenv
except:
    print("Missing packages, run pip install -r requirements")
    print("ALSO: I strongly recommend using a virtual environment. See my docker image or create a virtual python environment")

load_dotenv()


with open('sep20.json', 'r') as f:
    data = f.read()
    jData = json.loads(data)
    print(jData[100])