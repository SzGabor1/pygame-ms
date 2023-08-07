import requests

# Replace the base URL with the actual URL where your FastAPI backend is running
BASE_URL = "http://127.0.0.1:8000"

# Function to register a new user


def register_user(username, password):
    url = f"{BASE_URL}/users/"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json()

# Function to log in an existing user


def login_user(username, password):
    url = f"{BASE_URL}/login/"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json()

# Function to create a character for a logged-in user


def create_character(username, character_name, character_class):
    url = f"{BASE_URL}/characters/"
    data = {
        "username": username,
        "character_name": character_name,
        "character_class": character_class,
    }
    response = requests.post(url, json=data)
    return response.json()

# Function to update a character for a logged-in user


def update_character(username, character_id, updated_data):
    url = f"{BASE_URL}/characters/{character_id}/"
    data = {"username": username, **updated_data}
    response = requests.put(url, json=data)
    return response.json()


# Example usage:
if __name__ == "__main__":
    username = "example_user"
    password = "example_password"
    character_name = "example_character"
    character_class = "warrior"

    # Register a new user
    registration_response = register_user(username, password)
    print("Registration Response:", registration_response)

    # Log in the registered user
    login_response = login_user(username, password)
    print("Login Response:", login_response)

    # Create a character for the logged-in user
    character_creation_response = create_character(
        username, character_name, character_class)
    print("Character Creation Response:", character_creation_response)

    # Update the character for the logged-in user
    character_id = character_creation_response["id"]
    updated_data = {"character_level": 5, "character_weapon": "Sword of Power"}
    update_response = update_character(username, character_id, updated_data)
    print("Update Response:", update_response)
