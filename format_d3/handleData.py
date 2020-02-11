import json

f = open("./d3dataTest.json", "r")
data = json.loads(f.read())
f.close()

links = []

# print(data)
# This takes in the d3 data we created and turns it into the links we need to form connections in d3
for el in data:
    for inner in data[el]["connections"]:
        holder = {
            "source": el,
            "target": data[el]["connections"][inner],
            "type": "corridor",
        }
        links.append(holder)

print(links)
f = open("./linksTest.json", "w")
f.write(json.dumps(links))
f.close()
