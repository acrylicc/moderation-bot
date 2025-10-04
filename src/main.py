# Yes i have the same functions in three different files, i have no clue how cogs work xyno lol

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from typing import Optional
import json

from cogs import moderation, tools, secret
from cogs.ids import *

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

def load_strikes():
    with open(os.path.abspath('strikes.json'), "r") as f:
        return json.load(f)

def save_strikes(data):
    with open(os.path.abspath('strikes.json'), "w") as f:
        json.dump(data, f, indent=4)

def clean_expired_strikes(data):
    now = datetime.now(timezone.utc)
    updated = False
    for guild_id in list(data.keys()):
        for user_id in list(data[guild_id].keys()):
            original_len = len(data[guild_id][user_id])

            data[guild_id][user_id] = [
                strike for strike in data[guild_id][user_id]
                if datetime.fromisoformat(strike["timestamp"]) > now - timedelta(days=30)
            ]

            if not data[guild_id][user_id]:
                del data[guild_id][user_id]
                updated = True
            elif len(data[guild_id][user_id]) != original_len:
                updated = True

        if not data[guild_id]:
            del data[guild_id]
            updated = True

        return updated

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.add_cog(moderation.ModerationCog(self))
        await self.add_cog(tools.ToolsCog(self))
        await self.add_cog(secret.SecretCog(self))

bot = Bot()

@tasks.loop(hours=6)
async def auto_clean_strikes():
    data = load_strikes()
    if clean_expired_strikes(data):
        save_strikes(data)

@bot.event
async def on_ready():
    auto_clean_strikes.start()
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    print("Commands synced!")

@bot.event
async def on_message(message):
    mention = f'<@{bot.user.id}>'
    if mention in message.content and 'today' in message.content.lower():
        weekday = datetime.today().weekday()
        if weekday == 0:
            await message.reply("https://tenor.com/view/mako-mako-mankanshoku-kill-la-kill-monday-mako-monday-gif-78982588398866667")
        elif weekday == 1:
            await message.reply("https://tenor.com/view/mako-mako-mankanshoku-kill-la-kill-tuesday-mako-tuesday-gif-17072428433246127365")
        elif weekday == 2:
            await message.reply("https://tenor.com/view/mako-mako-mankanshoku-kill-la-kill-wednesday-mako-wednesday-gif-3049094210901091093")
        elif weekday == 3:
            await message.reply("https://tenor.com/view/mako-mako-mankanshoku-kill-la-kill-thursday-mako-thursday-gif-8626784389241889032")
        elif weekday == 4:
            await message.reply("https://tenor.com/view/mako-mako-mankanshoku-kill-la-kill-friday-mako-friday-gif-10541299650248512573")
        elif weekday == 5:
            await message.reply("https://tenor.com/view/mako-kill-la-kill-mako-mankanshoku-saturday-mako-saturday-gif-7305386381456943983")
        elif weekday == 6:
            await message.reply("https://tenor.com/view/mako-mako-mankanshoku-kill-la-kill-sunday-mako-sunday-gif-16617755993563860585")
    elif mention in message.content:
        await message.reply("hi my name jira")

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        roles = [role.id for role in after.roles]
        super_supporter = bot.get_guild(GUILD_ID).get_role(SUPER_SUPPORTER_ROLE_ID)

        # If they have the two roles needed, but dont have the new role
        if MEMBER_TIER_2_ROLE_ID in roles and SUB_TIER_3_ROLE_ID in roles and SUPER_SUPPORTER_ROLE_ID not in roles:
            await after.add_roles(super_supporter)
        # Removing the role if they no longer have the prereqs
        elif SUPER_SUPPORTER_ROLE_ID in roles and MEMBER_TIER_2_ROLE_ID not in roles or SUB_TIER_3_ROLE_ID not in roles:
            await after.remove_roles(super_supporter)

        # If a user somehow has more than one color role, which should not be possible
        #  This command will remove all but one of them
        count = 0
        for i in range(len(roles)):
            for j in range(len(COLOR_ROLE_IDS)):
                if roles[i] == COLOR_ROLE_IDS[j] and count >= 1:
                    await after.remove_roles(bot.get_guild(GUILD_ID).get_role(roles[i]))
                elif roles[i] == COLOR_ROLE_IDS[j]:
                    count = count + 1

        # If a user has a color role for a normla role that they no longer have
        if SPECIAL_COLOR_ROLE_ID in roles and SPECIAL_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(SPECIAL_COLOR_ROLE_ID))
        elif SUPER_SUPPORTER_COLOR_ROLE_ID in roles and SUPER_SUPPORTER_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(SUPER_SUPPORTER_COLOR_ROLE_ID))
        elif MEMBER_TIER_2_COLOR_ROLE_ID in roles and MEMBER_TIER_2_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(MEMBER_TIER_2_COLOR_ROLE_ID))
        elif MEMBER_TIER_1_COLOR_ROLE_ID in roles and MEMBER_TIER_2_ROLE_ID not in roles and MEMBER_TIER_1_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(MEMBER_TIER_1_COLOR_ROLE_ID))
        elif MEMBER_COLOR_ROLE_ID in roles and MEMBER_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(MEMBER_COLOR_ROLE_ID))
        elif SUB_TIER_3_COLOR_ROLE_ID in roles and SUB_TIER_3_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(SUB_TIER_3_COLOR_ROLE_ID))
        elif SUB_TIER_2_COLOR_ROLE_ID in roles and SUB_TIER_3_ROLE_ID not in roles and SUB_TIER_2_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(SUB_TIER_2_COLOR_ROLE_ID))
        elif SUB_TIER_1_COLOR_ROLE_ID in roles and SUB_TIER_3_ROLE_ID not in roles and SUB_TIER_2_ROLE_ID not in roles and SUB_TIER_1_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(SUB_TIER_1_COLOR_ROLE_ID))
        elif SUB_COLOR_ROLE_ID in roles and SUB_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(SUB_COLOR_ROLE_ID))
        elif BOOSTER_COLOR_ROLE_ID in roles and BOOSTER_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(BOOSTER_COLOR_ROLE_ID))
        elif CONTRIBUTOR_COLOR_ROLE_ID in roles and CONTRIBUTOR_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(CONTRIBUTOR_COLOR_ROLE_ID))
        elif MUSICIAN_COLOR_ROLE_ID in roles and MUSICIAN_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(MUSICIAN_COLOR_ROLE_ID))
        elif ARTIST_COLOR_ROLE_ID in roles and ARTIST_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(ARTIST_COLOR_ROLE_ID))
        elif GOOBER_2_COLOR_ROLE_ID in roles and GOOBER_2_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(GOOBER_2_COLOR_ROLE_ID))
        elif GOOBER_COLOR_ROLE_ID in roles and GOOBER_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(GOOBER_COLOR_ROLE_ID))
        elif PINGS_COLOR_ROLE_ID in roles and POLL_PINGS_ROLE_ID not in roles and EVENT_PINGS_ROLE_ID not in roles and MERCH_PINGS_ROLE_ID not in roles and GIVEAWAY_PINGS_ROLE_ID not in roles and STREAM_PINGS_ROLE_ID not in roles and SECOND_CHANNEL_PINGS_ROLE_ID not in roles and VOD_CHANNEL_PINGS_ROLE_ID not in roles:
            await after.remove_roles(bot.get_guild(GUILD_ID).get_role(PINGS_COLOR_ROLE_ID))

token = os.getenv("bot_token")
bot.run(token)
