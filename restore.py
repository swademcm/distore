import requests
import json

# Replace with your own values
TOKEN = "MTIzNDY1NTEyMjkyMzk4Mjg0OA.G7gTg6.yfSDEARbAh3pFvLvM4rCsZp8r6FvLjsVVmLrl8"
GUILD_ID = "1234710670595850305"
USER_FILE = "users.txt"  # File containing access tokens and user IDs (one per line)
CLIENT_ID = "1234655122923982848"
CLIENT_SECRET = "b9GbK2aWUz2aAgCkdKGFgVS1MLF_BUk0"
ROLE_IDS = ['1237234002914447411']
# Endpoint to add a user to a guild
url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{{}}"

# Headers with authorization
headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

def add_user_to_guild(user_id, access_token, nickname=None, role_ids=None):
    data = {
        "access_token": access_token,
        "nick": nickname,
        "roles": role_ids if role_ids else []
    }
    response = requests.put(url.format(user_id), headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print(f"User {user_id} added to the server {GUILD_ID} successfully!")
    else:
        print(f"Error adding user {user_id} to the server {GUILD_ID}. Status code: {response.status_code}")

def read_users_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return [line.strip() for line in lines]

def refresh_access_token(refresh_token):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers)
    if response.status_code == 200:
        return response.json()["access_token"], response.json()["refresh_token"]
    else:
        print(f"Error refreshing access token. Status code: {response.status_code}")
        return None, None

def update_tokens_in_file(user_id, new_access_token, new_refresh_token):
    # Read the current users and tokens from the file
    with open(USER_FILE, "r") as file:
        lines = file.readlines()
    users = {line.split(",")[0]: line.strip().split(",")[1:] for line in lines}

    # Update the tokens for the user
    users[user_id] = [new_access_token, new_refresh_token]

    # Write the updated tokens back to the file
    with open(USER_FILE, "w") as file:
        for uid, tokens in users.items():
            file.write(f"{uid},{tokens[0]},{tokens[1]}\n")

def load_and_refresh_tokens():
    # Read user IDs, access tokens, and refresh tokens from the file
    with open(USER_FILE, "r") as file:
        lines = file.readlines()

    # Cycle through each user and refresh tokens
    for user in lines:
        user_id, access_token, refresh_token = user.strip().split(",")
        new_access_token, new_refresh_token = refresh_access_token(refresh_token)
        if new_access_token and new_refresh_token:
            update_tokens_in_file(user_id, new_access_token, new_refresh_token)
            add_user_to_guild(user_id, new_access_token)

def exchange_code_for_token(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:5000/callback"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers)
    if response.status_code == 200:
        return response.json()["access_token"], response.json()["refresh_token"]
    else:
        print(f"Error exchanging code for token. Status code: {response.status_code}")
        return None, None

def get_user_id(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error getting user ID. Status code: {response.status_code}")
        return None

def store_tokens_in_file(user_id, access_token, refresh_token):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id},{access_token},{refresh_token}\n")


def get_user_details(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png"
        return {"username": user_data['username'], "avatar_url": avatar_url}
    else:
        print(f"Error getting user details. Status code: {response.status_code}")
        return None
    

load_and_refresh_tokens()
