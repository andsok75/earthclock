import json
import sys

def print_fields(d, path=''):
    if path:
        print(path)
    if isinstance(d, list) and len(d) != 0:
        print_fields(d[0], path + "[]")
    if not isinstance(d, dict):
        return
    for k in d.keys():
        print_fields(d[k], path + f"/{k}")

def round_point(point, n):
    return [round(point[0], n), round(point[1], n)]


file_name = sys.argv[1]
precision = int(sys.argv[2])

print(f"converting file {file_name} to precision {precision}")

countries = json.load(open(file_name))

print_fields(countries)
print(set(f["geometry"]["type"] for f in countries["features"]))

for f in countries["features"]:
    t = f["geometry"]["type"]
    if t == "Polygon":
        polygon = f["geometry"]["coordinates"][0]
        for i, point in enumerate(polygon):
            polygon[i] = round_point(point, precision)
    elif t == "MultiPolygon":
        for polygons in f["geometry"]["coordinates"]:
            for polygon in polygons:
                for i, point in enumerate(polygon):
                    polygon[i] = round_point(point, precision)
    else:
        raise Exception(f"unexpected polygon type {t}")

json.dump(countries, open(file_name, "w"), separators=(',', ':'))
