import requests
import json

# Replace with your own values
TOKEN = "YOUR_BOT_TOKEN"
GUILD_ID = "YOUR_GUILD_ID"
USER_ID = "USER_ID_TO_ADD"

# Endpoint to add a user to a guild
url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{USER_ID}"

# Headers with authorization
headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

# Data to send (you can customize this)
data = {
    "access_token": "ACCESS_TOKEN_OF_THE_USER",
    "nick": "New Nickname (optional)",
    "roles": ["ROLE_ID_1", "ROLE_ID_2"]  # List of role IDs to assign (optional)
}

# Make the request
response = requests.put(url, headers=headers, data=json.dumps(data))

# Check if the user was added successfully
if response.status_code == 201:
    print(f"User {USER_ID} added to the server {GUILD_ID} successfully!")
else:
    print(f"Error adding user {USER_ID} to the server {GUILD_ID}. Status code: {response.status_code}")

