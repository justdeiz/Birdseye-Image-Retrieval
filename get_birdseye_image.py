import requests
from urllib import request
from PIL import Image
import argparse

BingMapsKey = ""

parser = argparse.ArgumentParser()
parser.add_argument('latitude', type=float)
parser.add_argument('longitude', type=float)
parser.add_argument('-k', "--key", required=False, type=str)

args = parser.parse_args()
centerPoint = f"{args.latitude},{args.longitude}"

if args.key is not None:
    BingMapsKey = args.key
elif BingMapsKey == "":
    print("No Bing Maps jey was specified. Set the BingMapsKey variable or use the -k argument!")
    exit(1)

url = f"https://dev.virtualearth.net/REST/V1/Imagery/Metadata/birdseyeV2/{centerPoint}?o=json&key={BingMapsKey}"

r = requests.get(url).json()

url2 = r["resourceSets"][0]["resources"][0]["imageUrl"]
subdomain = r["resourceSets"][0]["resources"][0]["imageUrlSubdomains"][0]
zoom = r["resourceSets"][0]["resources"][0]["zoomMax"]

TILESIZE = r["resourceSets"][0]["resources"][0]["imageHeight"]

tilesX = int(r["resourceSets"][0]["resources"][0]["tilesX"])
tilesY = int(r["resourceSets"][0]["resources"][0]["tilesY"])

tiles = int(tilesX) * int(tilesY)
result = Image.new('RGB', (tilesX * TILESIZE, tilesY * TILESIZE))

for tileY in range(tilesY):
    for tileX in range(tilesX):
        tile = tileX + tilesX * tileY
        print(f"\rtileId {tile} / {tiles-1}", end="")
        furl = url2.format(subdomain = subdomain, zoom = zoom, tileId = tile)
        with request.urlopen(furl) as file:
            image = Image.open(file)
            result.paste(image, (tileX * TILESIZE, tileY * TILESIZE))
print()

result.save("out.jpg", format="jpeg")
