import requests
import json

# Replace with your own values
TOKEN = "YOUR_BOT_TOKEN"
GUILD_ID = "YOUR_GUILD_ID"
USER_FILE = "users.txt"  # File containing access tokens and user IDs (one per line)

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
        "roles": role_ids
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

# Read user IDs and access tokens from the file
users = read_users_from_file(USER_FILE)

# Cycle through each user
for user in users:
    user_id, access_token = user.split(",")
    add_user_to_guild(user_id, access_token)
