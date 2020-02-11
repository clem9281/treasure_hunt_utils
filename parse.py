import requests
import time
import random
import sys
import json
from util import Queue
import os


URL = "https://lambda-treasure-hunt.herokuapp.com"


def has_unknowns(visited):
    for key in visited:
        if "?" in visited[key]["directions"].values():
            return True
    return False


def has_cooldown_error(e):
    res = e.response.json()
    for element in res["errors"]:
        if "Cooldown" in element:
            return True
    return False


def login():
    # login
    try:
        login_r = requests.post(
            f"{URL}/api/login/", data={"username": "isaac", "password": "navi1212"},
        )
        login_r.raise_for_status()
        return login_r.json()["key"]
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def init(token):
    # get room info
    try:
        room_r = requests.get(
            f"{URL}/api/adv/init/", headers={"Authorization": f"Token {token}"},
        )
        room_r.raise_for_status()
        room = room_r.json()
        cooldown = room["cooldown"]
        time.sleep(cooldown)
        return room
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def move(direction, token, next_room_id=None):
    if next_room_id:
        body = json.dumps({"direction": direction, "next_room_id": f"{next_room_id}"})
    else:
        body = json.dumps({"direction": direction})
    while True:
        try:
            next_room_r = requests.post(
                f"{URL}/api/adv/move/",
                headers={
                    "Authorization": f"Token {token}",
                    "Content-Type": "application/json",
                },
                data=body,
            )
            next_room_r.raise_for_status()
            next_room = next_room_r.json()
            cooldown = next_room["cooldown"]
            time.sleep(cooldown)
            return next_room
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 400 and has_cooldown_error(e):
                res = e.response.json()
                print(f"CoolDown Error: Waiting {res['cooldown']}")
                time.sleep(res["cooldown"])
            else:
                print(e)
                sys.exit(1)


def update_visited_unknowns(visited, room):
    if room["room_id"] not in visited:
        visited[room["room_id"]] = {"directions": {}, "info": {}}
        for direction in room["exits"]:
            visited[room["room_id"]]["directions"][direction] = "?"
        visited[room["room_id"]]["info"] = room


def update_visited_knowns(visited, room, next_room, direction):
    reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
    visited[room["room_id"]]["directions"][direction] = next_room
    visited[next_room["room_id"]]["directions"][reverse_dirs[direction]] = room


def bfs_back(room, visited, token):
    q = Queue()
    q.enqueue([{"room": room, "direction": None}])
    traversal_visited = set()
    while q.len() > 0:
        path = q.dequeue()
        current = path[-1]["room"]
        if current["room_id"] not in traversal_visited:
            traversal_visited.add(current["room_id"])
            if "?" in visited[current["room_id"]]["directions"].values():

                for element in path:

                    if element["direction"]:
                        move(element["direction"], token, element["room"]["room_id"])
                return current
            for direction in current["exits"]:
                next_room = visited[current["room_id"]]["directions"][direction]
                path_copy = path.copy()
                path_copy.append({"room": next_room, "direction": direction})
                q.enqueue(path_copy)


visited = {}


def path_maker():

    count = 0
    # login and get token
    token = os.environ["TOKEN"]

    # initialize player and get current room info
    room = init(token)

    global visited

    update_visited_unknowns(visited, room)

    while has_unknowns(visited):

        if "?" in visited[room["room_id"]]["directions"].values():
            exits = room["exits"]
            random.shuffle(exits)
            count += 1
            for direction in exits:
                if visited[room["room_id"]]["directions"][direction] == "?":
                    next_room = move(direction, token)
                    update_visited_unknowns(visited, next_room)
                    update_visited_knowns(visited, room, next_room, direction)
                    room = next_room
                    break
        else:

            room = bfs_back(room, visited, token)

    v = json.dumps(visited)
    f = open("output.json", "w")
    f.write(v)
    f.close()


# path_maker()


# login
# token = os.environ["TOKEN"]

# print(f"logged in, token: {token}")


# room = init(token)

# print(f"got room: {room}")

# direction = "w"

# next_room = move(direction, token, 3)

# next_direction = next_room["exits"][0]

# another_next_room = move(next_direction, token)

