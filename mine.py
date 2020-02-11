import hashlib
import requests

import sys
import json
import time
import random
import os


# This is the actual mining algorithm to get a coin


def proof_of_work(last_proof, difficulty):
    proof = random.randint(0, 200000000)
    while not valid_proof(last_proof, proof, difficulty):
        proof += random.randint(0, 10000)
    # guess = f'{last_proof}{proof}'.encode()
    # guess_hash = hashlib.sha256(guess).hexdigest()
    return proof


def valid_proof(last_proof, proof, difficulty):
    guess = f"{last_proof}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # return True or False
    return guess_hash[:difficulty] == "0" * difficulty


if __name__ == "__main__":

    url = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    token = os.environ["TOKEN"]

    print("token is", token)

    


    try:
        r = requests.get(
            f"{url}/last_proof/", headers={"Authorization": f"Token {token}"}
        )
        r.raise_for_status()
        data = r.json()
        cooldown = data["cooldown"]
        time.sleep(cooldown)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    print(data)
    new_proof = proof_of_work(data["proof"], data["difficulty"])
    print(new_proof)
    post_data = json.dumps({"proof": new_proof})

    try:
        mine_r = requests.post(
            f"{url}/mine/",
            headers={
                "Authorization": f"Token {token}",
                "Content-Type": "application/json",
            },
            data=post_data,
        )
        mine_r.raise_for_status()
        mine = mine_r.json()
        print(mine)
        cooldown = mine["cooldown"]
        time.sleep(cooldown)
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 400 and has_cooldown_error(e):
            res = e.response.json()
            print(f"CoolDown Error: Waiting {res['cooldown']}")
            time.sleep(res["cooldown"])
        else:
            print(e)
            sys.exit(1)
    
