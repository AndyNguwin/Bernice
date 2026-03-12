async def status_handler(user_id: int, response_type=4):
    # Response 4: new message
    # Response 7: edit message

    creator_id = 152994401612726272

    if user_id != creator_id:
        return {
            "type": 4,
            "data": {
                "flags": 64,
                "content": "No no no. You can't do that. :^)"
            }
        }

    embed = None
    if response_type == 4:
        embed = [
            {
                "title" : "BOT STATUS:\t:green_circle:",
                "description": f"**BOT IS CURRENTLY ALIVE!**\nHave fun :^)"
            }
        ]
    elif response_type == 7:
       embed = [
            {
                "title" : "BOT STATUS:\t:red_circle:",
                "description": f"Bot is currently **off**.\nCatch you later :("
            }
        ] 

    return {
        "type": response_type,
        "data": {
            "embeds": embed,
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "style": 2,
                            "label": "Change Status",
                            "custom_id": f"status:{user_id}",
                        }
                    ]
                }
            ]
        }
    }

    
