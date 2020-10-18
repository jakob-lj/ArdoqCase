import sys

try:
    import requests
except:
    print("Have you installed all dependencies?")
    sys.exit(1)

url = "https://data.urbansharing.com/oslobysykkel.no/trips/v1/2019/04.json"

result = requests.get(url)
f = open('apr19.json', 'w')

f.write(result.text)
f.close()