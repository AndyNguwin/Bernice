import requests
import dotenv
import os

dotenv.load_dotenv()
DISCORD_APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = "1462694896665231476"

# url = f"https://discord.com/api/v10/applications/{DISCORD_APPLICATION_ID}/commands"
url = f"https://discord.com/api/v10/applications/{DISCORD_APPLICATION_ID}/guilds/{GUILD_ID}/commands"
# Guild for dev (quicker)

commands = [
    {
        "name": "drop",
        "type": 1,
        "description": "Drop a random idol photocard"
    },
    {
        "name": "inventory",
        "type": 1,
        "description": "View your inventory of photocards"
    },
    {
        "name": "view",
        "type": 1,
        "description": "View your a card with using a card's code.",
        "options": [
            {
                "type": 3,
                "name": "code",
                "description": "6-character code of card",
                "required": True
            }
        ]
    },
    {
        "name": "status",
        "type": 1,
        "description": "Change bot status [CREATOR ONLY COMMAND]"
    }
]

# For authorization, you can use either your bot token
headers = {
    "Authorization": f"Bot {DISCORD_TOKEN}"
}


# r = requests.post(url, headers=headers, json=commands)
r = requests.put(url, headers=headers, json=commands)

print(r.status_code)
print(r.json())
