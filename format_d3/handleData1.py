import json

f = open("./old_output.json", "r")
data = json.loads(f.read())
f.close()

# print(data)

# This takes in the data we created with our traversal and turns it into a nicer format for d3
new_shape = {}
count = 0
for key in data:
    if key not in new_shape:
        new_shape[key] = {"coordinates": {}, "connections": {}}
    coord = data[key]["info"]["coordinates"]
    x = int(coord.split(",")[0][1:])
    y = int(coord.split(",")[1][:-1])
    connections = {}
    for direction in data[key]["directions"]:
        connections[direction] = data[key]["directions"][direction]["room_id"]

    new_shape[key]["coordinates"] = {"x": x, "y": y}
    new_shape[key]["connections"] = connections

# print(new_shape)
f = open("./d3dataTest.json", "w")
f.write(json.dumps(new_shape))
f.close()
