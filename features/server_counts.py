
import json
import discord
from discord.ext import tasks as d_tasks
import requests

class ServerCounts(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()

        self.bot = bot

        
        with open('config.json', 'r', encoding='utf8') as f:
            data = json.load(f)

        if "send_server_count" not in data:
            return
        
        if data["send_server_count"]["top_gg"]["enabled"]:
            self.top_gg_token = data["send_server_count"]["top_gg"]["token"]
            self.topgg_send.start()

            
        self.bot_id = data["bot_id"]

    @d_tasks.loop(hours=1)
    async def topgg_send(self):
        res = requests.post(f"https://top.gg/api/bots/{str(self.bot_id)}/stats", headers={
            "Authorization": f"Bearer {self.top_gg_token}",
            "Content-Type": "application/json"
        }, json={
            "server_count": len(self.bot.guilds)
        })
        
        if not res.ok:
            print("Sending server count to top.gg failed")
