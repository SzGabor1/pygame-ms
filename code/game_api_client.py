import requests
import hashlib


BASE_URL = "http://91.229.245.186:8000"


def register_user(username, password):
    url = f"{BASE_URL}/register/"
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    data = {"username": username, "password": hashed_password}
    response = requests.post(url, json=data)

    response_dict = {
        "status_code": response.status_code,
        "json_response": response.json(),
        "content": response.text
    }

    return response_dict


def login_user(username, password):
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    response = requests.post(
        f"{BASE_URL}/login/", json={"username": username, "password": hashed_password})

    if response.status_code == 200:
        data = response.json()

        return {"username": data["username"], "user_id": data["user_id"]}
    elif response.status_code == 401:
        return response.status_code
        raise ValueError("Invalid credentials")
    else:
        raise ValueError("An error occurred during login")


def get_characters(user_id):
    url = f"{BASE_URL}/get_characters/"
    response = requests.get(url, json={"user_id": user_id})
    return response.json()


def create_character(character_data):
    url = f"{BASE_URL}/insert_character/"
    response = requests.post(url, json=character_data)
    return response.json()


def update_character(character_id, updated_data):
    url = f"{BASE_URL}/update_character/{character_id}/"
    response = requests.put(url, json=updated_data)
    return response.json()


def get_top_ten_highest_level_users():
    url = f"{BASE_URL}/highest_level_users/"
    response = requests.get(url)

    if response.status_code == 200:
        highest_level_users = response.json()
        return highest_level_users
    else:
        raise ValueError(
            f"Failed to retrieve highest level users. Status code: {response.status_code}")
