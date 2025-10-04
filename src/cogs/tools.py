import discord
from discord.ext import commands
from discord import app_commands
from cogs.ids import *
from datetime import timedelta, datetime, timezone
import json
import os
import io

class Colors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Special", emoji=SPECIAL_ROLE_EMOJI),
            discord.SelectOption(label="Super Supporter", emoji=SUPER_SUPPORTER_ROLE_EMOJI),
            discord.SelectOption(label="Jira Enthusiast", emoji=MEMBER_TIER_2_ROLE_EMOJI),
            discord.SelectOption(label="Jira Fan", emoji=MEMBER_TIER_1_ROLE_EMOJI),
            discord.SelectOption(label="Channel Member", emoji=MEMBER_ROLE_EMOJI),
            discord.SelectOption(label="Tier 3", emoji=SUB_TIER_3_ROLE_EMOJI),
            discord.SelectOption(label="Tier 2", emoji=SUB_TIER_2_ROLE_EMOJI),
            discord.SelectOption(label="Tier 1", emoji=SUB_TIER_1_ROLE_EMOJI),
            discord.SelectOption(label="Twitch Sub", emoji=SUB_ROLE_EMOJI),
            discord.SelectOption(label="Booster", emoji=BOOSTER_ROLE_EMOJI),
            discord.SelectOption(label="Contributor", emoji=CONTRIBUTOR_ROLE_EMOJI),
            discord.SelectOption(label="Musician", emoji=MUSICIAN_ROLE_EMOJI),
            discord.SelectOption(label="Artist", emoji=ARTIST_ROLE_EMOJI),
            discord.SelectOption(label="Goober 2", emoji=GOOBER_2_ROLE_EMOJI),
            discord.SelectOption(label="Goober", emoji=GOOBER_ROLE_EMOJI),
            discord.SelectOption(label="Pings", emoji=PUSHPIN_EMOJI),
            discord.SelectOption(label="None", emoji=X_EMOJI)
        ]
        super().__init__(placeholder="Choose an option...", min_values=1, max_values=1, options=options,custom_id="colors")

    async def remove_colors(self, user_roles, interaction):
        for i in range(len(user_roles)):
            for j in range(len(COLOR_ROLE_IDS)):
                if user_roles[i] == COLOR_ROLE_IDS[j]:
                    await interaction.user.remove_roles(interaction.guild.get_role(user_roles[i]))

    async def callback(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        
        if CREATORS_ROLE_ID in user_roles or SALAMI_ROLE_ID in user_roles or ACRYLIC_ROLE_ID in user_roles or MOD_ROLE_ID in user_roles or ART_PANEL_ROLE_ID in user_roles:
            await interaction.response.send_message(f"{X_EMOJI} You have a role that is ranked higher than all role colors, meaning you cannot change your role color.", ephemeral=True)
            return

        if self.values[0] == "Special":
            if SPECIAL_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(SPECIAL_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Super Supporter":
            if SUPER_SUPPORTER_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(SUPER_SUPPORTER_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Jira Enthusiast":
            if MEMBER_TIER_2_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(MEMBER_TIER_2_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Jira Fan":
            if MEMBER_TIER_1_ROLE_ID in user_roles or MEMBER_TIER_2_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(MEMBER_TIER_1_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` or `Jira Enthusiast` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Channel Member":
            if MEMBER_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(MEMBER_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Tier 3":
            if SUB_TIER_3_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(SUB_TIER_3_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Tier 2":
            if SUB_TIER_2_ROLE_ID in user_roles or SUB_TIER_3_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(SUB_TIER_2_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` or `Tier 3` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Tier 1":
            if SUB_TIER_1_ROLE_ID in user_roles or SUB_TIER_2_ROLE_ID in user_roles or SUB_TIER_3_ROLE_ID in user_roles: #could honestly change this to just check if it has the twitch sub role but eh
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(SUB_TIER_1_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}`, `Tier 2`, or `Tier 3` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Twitch Sub":
            if SUB_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(SUB_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Booster":
            if BOOSTER_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(BOOSTER_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Contributor":
            if CONTRIBUTOR_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(CONTRIBUTOR_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Musician":
            if MUSICIAN_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(MUSICIAN_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Artist":
            if ARTIST_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(ARTIST_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Goober 2":
            if GOOBER_2_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(GOOBER_2_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Goober":
            if GOOBER_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(GOOBER_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `{self.values[0]}` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "Pings":
            if POLL_PINGS_ROLE_ID in user_roles or EVENT_PINGS_ROLE_ID in user_roles or MERCH_PINGS_ROLE_ID in user_roles or GIVEAWAY_PINGS_ROLE_ID in user_roles or STREAM_PINGS_ROLE_ID in user_roles or SECOND_CHANNEL_PINGS_ROLE_ID in user_roles or VOD_CHANNEL_PINGS_ROLE_ID in user_roles:
                await self.remove_colors(user_roles,interaction)
                await interaction.user.add_roles(interaction.guild.get_role(PINGS_COLOR_ROLE_ID))
                await interaction.response.send_message(f"{CHECK_EMOJI} You have now set your role color to: {self.values[0]}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{X_EMOJI} You must have `a notifcation role` to set your role color to: {self.values[0]}.", ephemeral=True)
        elif self.values[0] == "None":
            await self.remove_colors(user_roles,interaction)
            await interaction.response.send_message(f"{CHECK_EMOJI} You have reset your role color to its defualt.", ephemeral=True)

class ColorsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Colors())

class ToolsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.add_view(ColorsView())

    tools = app_commands.Group(name="tools", description="Jira's Tools and Utilities")

    def load_strikes(self):
        with open(os.path.abspath('./strikes.json'), "r") as f:
            return json.load(f)

    def save_strikes(self, data):
        with open(os.path.abspath('./strikes.json'), "w") as f:
            json.dump(data, f, indent=4)

    def clean_expired_strikes(self, data):
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

    @tools.command(name="report", description="Report a user or bug to staff.")
    async def report(self, interaction: discord.Interaction, reason: str, file: discord.Attachment = None, member: discord.Member = None):
        await interaction.response.send_message("Reporting member...", ephemeral=True)

        if member:
            reported_user = member.mention
        else:
            reported_user = "None provided"

        embed = discord.Embed(
            title=f"{NO_ENTRY_EMOJI} New Report",
            description=f"**Reported By:** {interaction.user.mention}\n**Reported User:** {reported_user}\n**Reason:** {reason}",
            color=discord.Color.red()
        )

        if file:
            if not file.content_type or not file.content_type.startswith("image/"):
                await interaction.followup.send(f"{WARNING_EMOJI} Please upload a valid image file (PNG, JPEG, etc.)", ephemeral=True)
                return
            else:
                embed.set_image(url=file.url)
        
        embed.timestamp = discord.utils.utcnow()

        # Send to report channel
        report_channel = self.bot.get_channel(REPORTS_CHANNEL_ID)
        if report_channel:
            await report_channel.send(embed=embed)
        else:
            await interaction.followup.send(f"{WARNING_EMOJI} Report channel with ID {REPORTS_CHANNEL_ID} not found.", ephemeral=True)

        embed = discord.Embed(
            title=f"{NO_ENTRY_EMOJI} New Report",
            description=f"**Reported By:** {interaction.user.mention}",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        # Send to log channel
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        await interaction.followup.send(f"{CHECK_EMOJI} Your report has been sent to staff.", ephemeral=True)

    @tools.command(name="goober", description="Check if you are eligble for Goober role.")
    async def goober(self, interaction: discord.Interaction):
        await interaction.response.send_message("Checking if you are eligble...", ephemeral=True)

        now = datetime.now(timezone.utc)
        joined_at = interaction.user.joined_at

        if not joined_at:
            await interaction.followup.send(f"{WARNING_EMOJI} Couldn't determine when you joined, please try again. If this continues to happen, please report this to staff via `/tools report`.", ephemeral=True)
            return

        tenure = now - joined_at
        required_tenure = timedelta(days=3)

        user_id = str(interaction.user.id)
        data = self.load_strikes()
        guild_id = str(interaction.guild.id)

        self.clean_expired_strikes(data)

        strikes = data.get(guild_id, {}).get(user_id, [])

        if tenure >= required_tenure:
            role = interaction.guild.get_role(GOOBER_ROLE_ID)
            if not role:
                await interaction.followup.send(f"{WARNING_EMOJI} Role not found. Check the GOOBER_ROLE_ID. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
                return

            if role in interaction.user.roles:
                await interaction.followup.send(f"{X_EMOJI} You already have Goober role.", ephemeral=True)
                return

            if int(len(strikes)) >= 2:
                await interaction.followup.send(f"{X_EMOJI} You currently have 2+ active strikes and cannot obtain Goober role.", ephemeral=True)
                return

            try:
                await interaction.user.add_roles(role, reason="Met 3-day server tenure requirement")
                await interaction.followup.send(f"{CHECK_EMOJI} You have been in the server for {tenure.days} days and as such have been promoted to Goober role.", ephemeral=True)

                embed = discord.Embed(
                    title=f"{GOOBER_ROLE_EMOJI} User Promoted to Goober",
                    description=f"**User:** {interaction.user.mention}",
                    color=discord.Color.dark_orange()
                )
                embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
                embed.timestamp = discord.utils.utcnow()

                # Send to log channel
                log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
                if log_channel:
                    await log_channel.send(embed=embed)
                else:
                    await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Failed to assign role to {interaction.user.mention}. Check my permissions. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
        else:
            remaining = required_tenure - tenure
            hours_left = int(remaining.total_seconds() // 3600)
            await interaction.followup.send(f"{X_EMOJI} You have only been in the server for {tenure.days} days.\nYou need **{hours_left} more hours** to qualify.", ephemeral=True)

    @tools.command(name="goober2", description="Check if you are eligble for Goober 2 role.")
    async def goober2(self, interaction: discord.Interaction):
        await interaction.response.send_message("Checking if you are eligble...", ephemeral=True)

        now = datetime.now(timezone.utc)
        joined_at = interaction.user.joined_at

        if not joined_at:
            await interaction.followup.send(f"{WARNING_EMOJI} Couldn't determine when you joined, please try again. If this continues to happen, please report this to staff via `/tools report`.", ephemeral=True)
            return

        tenure = now - joined_at
        required_tenure = timedelta(days=21)

        user_id = str(interaction.user.id)
        data = self.load_strikes()
        guild_id = str(interaction.guild.id)

        self.clean_expired_strikes(data)

        strikes = data.get(guild_id, {}).get(user_id, [])

        if tenure >= required_tenure:
            goober = interaction.guild.get_role(GOOBER_ROLE_ID)
            role = interaction.guild.get_role(GOOBER_2_ROLE_ID)
            if not role:
                await interaction.followup.send(f"{WARNING_EMOJI} Role not found. Check the GOOBER_2_ROLE_ID. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
                return

            if role in interaction.user.roles:
                await interaction.followup.send(f"{X_EMOJI} You already have Goober 2 role.", ephemeral=True)
                return
            
            if goober not in interaction.user.roles:
                await interaction.followup.send(f"{X_EMOJI} You must have Goober role before you can get Goober 2 role.", ephemeral=True)
                return

            if int(len(strikes)) >= 2:
                await interaction.followup.send(f"{X_EMOJI} You currently have 2+ active strikes and cannot obtain Goober 2 role.", ephemeral=True)
                return

            try:
                await interaction.user.add_roles(role, reason="Met 3-week server tenure requirement")
                await interaction.followup.send(f"{CHECK_EMOJI} You have been in the server for {tenure.days} days and as such have been promoted to Goober 2 role.", ephemeral=True)

                embed = discord.Embed(
                    title=f"{GOOBER_2_ROLE_EMOJI} User Promoted to Goober 2",
                    description=f"**User:** {interaction.user.mention}",
                    color=discord.Color.teal()
                )
                embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
                embed.timestamp = discord.utils.utcnow()

                # Send to log channel
                log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
                if log_channel:
                    await log_channel.send(embed=embed)
                else:
                    await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Failed to assign role to {interaction.user.mention}. Check my permissions. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
        else:
            remaining = required_tenure - tenure
            hours_left = int(remaining.total_seconds() // 3600)
            await interaction.followup.send(f"{X_EMOJI} You have only been in the server for {tenure.days} days.\nYou need **{hours_left} more hours** to qualify.", ephemeral=True)

    @tools.command(name="musician", description="Apply for Musician role.")
    async def musician(self, interaction: discord.Interaction, file: discord.Attachment = None, link: str = None):
        await interaction.response.send_message("Sending application...", ephemeral=True)

        author_roles = [role.id for role in interaction.user.roles]

        if GOOBER_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You must have Goober role to use this command.", ephemeral=True)
            return
        
        if MUSICIAN_ROLE_ID in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You already have Musician role.", ephemeral=True)
            return

        if not file and not link:
            await interaction.followup.send(f"{X_EMOJI} You must pass either a file or a link.", ephemeral=True)
            return

        # Check for audio content type
        if file:
            file.content_type
            if not file.content_type or not file.content_type.startswith("audio/"):
                await interaction.followup.send(f"{WARNING_EMOJI} Please upload a valid audio file (MP3, WAV, etc.)", ephemeral=True)
                return

        # Get the target channel
        apply_channel = self.bot.get_channel(MUSICIAN_APPLY_CHANNEL_ID)
        if not apply_channel:
            await interaction.followup.send(f"{WARNING_EMOJI} Apply channel with ID {MUSICIAN_APPLY_CHANNEL_ID} not found.", ephemeral=True)
            return

        # Create an embed with the image
        embed = discord.Embed(
            title=f"{MUSICIAN_ROLE_EMOJI} New Application",
            description=f"Uploaded by {interaction.user.mention}",
            color=discord.Color.blue()
        )
        
        if link:
            embed.description = f"{embed.description}\n{link}"

        if file:
            file_bytes = await file.read()
            discord_file = discord.File(io.BytesIO(file_bytes), filename=file.filename)
            await apply_channel.send(embed=embed, file=discord_file)
        else:
            await apply_channel.send(embed=embed)

        embed = discord.Embed(
            title=f"{MUSICIAN_ROLE_EMOJI} New Musician Application",
            description=f"**User:** {interaction.user.mention}",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        # Send to log channel
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        # Confirm to user
        await interaction.followup.send(f"{CHECK_EMOJI} Your application for Musician role has been sent.", ephemeral=True)

    @tools.command(name="artist", description="Apply for Artist role.")
    async def artist(self, interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.send_message("Sending application...", ephemeral=True)

        author_roles = [role.id for role in interaction.user.roles]

        if GOOBER_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You must have Goober role to use this command.", ephemeral=True)
            return
        
        if ARTIST_ROLE_ID in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You already have Artist role.", ephemeral=True)
            return

        # Check for image content type
        if not file.content_type or not file.content_type.startswith("image/"):
            await interaction.followup.send(f"{WARNING_EMOJI} Please upload a valid image file (PNG, JPEG, etc.)", ephemeral=True)
            return

        # Get the target channel
        apply_channel = self.bot.get_channel(ARTIST_APPLY_CHANNEL_ID)
        if not apply_channel:
            await interaction.followup.send(f"{WARNING_EMOJI} Apply channel with ID {ARTIST_APPLY_CHANNEL_ID} not found.", ephemeral=True)
            return

        # Create an embed with the image
        embed = discord.Embed(
            title=f"{ARTIST_ROLE_EMOJI} New Application",
            description=f"Uploaded by {interaction.user.mention}",
            color=discord.Color.blue()
        )
        embed.set_image(url=file.url)

        # Send the embed to the target channel
        await apply_channel.send(embed=embed)

        embed = discord.Embed(
            title=f"{ARTIST_ROLE_EMOJI} New Artist Application",
            description=f"**User:** {interaction.user.mention}",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        # Send to log channel
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        # Confirm to user
        await interaction.followup.send(f"{CHECK_EMOJI} Your application for Artist role has been sent.", ephemeral=True)

    @tools.command(name="review_applicant", description="Accept or deny an applicant.")
    async def review_applicant(self, interaction: discord.Interaction, accepted: bool, member: discord.Member, message_id: str, reason: str = "No reason provided."):
        await interaction.response.send_message(f"{"Accepting" if accepted else "Denying"} member...", ephemeral=True)
        
        author_roles = [role.id for role in interaction.user.roles]

        # Check if the user has the authorized role
        if MOD_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return
        
        try:
            message_id_int = int(message_id)
        except ValueError:
            await interaction.followup.send(f"{X_EMOJI} Invalid message ID format.", ephemeral=True)
            return
        
        artist_apply_channel = self.bot.get_channel(ARTIST_APPLY_CHANNEL_ID)
        if not artist_apply_channel:
            await interaction.followup.send(f"{WARNING_EMOJI} Apply channel with ID {ARTIST_APPLY_CHANNEL_ID} not found.", ephemeral=True)
            return
        music_apply_channel = self.bot.get_channel(MUSICIAN_APPLY_CHANNEL_ID)
        if not music_apply_channel:
            await interaction.followup.send(f"{WARNING_EMOJI} Apply channel with ID {MUSICIAN_APPLY_CHANNEL_ID} not found.", ephemeral=True)
            return
        
        try:
            message = await artist_apply_channel.fetch_message(message_id_int)
            await message.delete()
            is_for_artist = True
        except discord.NotFound:
            try:
                message = await music_apply_channel.fetch_message(message_id_int)
                await message.delete()
                is_for_artist = False
            except discord.NotFound:
                await interaction.followup.send(f"{WARNING_EMOJI} Message not found in the application channel.", ephemeral=True)
                return
            except discord.Forbidden:
                await interaction.followup.send(f"{X_EMOJI} I don't have permission to delete that message.", ephemeral=True)
                return
        except discord.Forbidden:
            await interaction.followup.send(f"{X_EMOJI} I don't have permission to delete that message.", ephemeral=True)
            return
        
        if is_for_artist:
            title = f"{CHECK_EMOJI} Artist Application Accepted" if accepted else f"{X_EMOJI} Artist Application Denied"
        else:
            title = f"{CHECK_EMOJI} Musician Application Accepted" if accepted else f"{X_EMOJI} Musician Application Denied"
        color = discord.Color.green() if accepted else discord.Color.red()

        embed = discord.Embed(
            title=title,
            description=f"**User:** {member.mention}\n**Reason:** {reason}\n**Moderator:** {interaction.user.mention}",
            color=color
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        # Try to DM the user
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)
            #return

        # If accepted, assign the role
        if accepted:
            if is_for_artist:
                role = interaction.guild.get_role(ARTIST_ROLE_ID)
            else:
                role = interaction.guild.get_role(MUSICIAN_ROLE_ID)
            if not role:
                await interaction.followup.send(f"{WARNING_EMOJI} Role not found. Check the ARTIST_ROLE_ID and or MUSICIAN_ROLE_ID. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
                return
            try:
                await member.add_roles(role, reason=f"Accepted by {interaction.user} - {reason}")
            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Couldn't assign role to {member.mention}. Check my permissions. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
                return

        # Respond to the reviewer
        action = "accepted and given the role" if accepted else "denied"
        await interaction.followup.send(f"{CHECK_EMOJI} {member.mention} has been {action} and notified via DM (If possible).", ephemeral=True)

    @tools.command(name="strikes", description="Check how many strikes you, or another user, has.")
    async def strikes(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.send_message("Checking strikes...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]
        
        if member:
            if MOD_ROLE_ID not in author_roles:
                await interaction.followup.send(f"{X_EMOJI} You don't have permission to check the strikes of other users.", ephemeral=True)
                return
            user_id = str(member.id)
        else:
            user_id = str(interaction.user.id)
            member = interaction.user
        
        data = self.load_strikes()
        guild_id = str(interaction.guild.id)

        self.clean_expired_strikes(data)

        strikes = data.get(guild_id, {}).get(user_id, [])
        await interaction.followup.send(f"{member.mention} has {len(strikes)} active strike(s).", ephemeral=True)
    
    @tools.command(name="roles", description="For creating/updating the embed in #role-info.")
    async def roles(self, interaction: discord.Interaction, edit : bool = True):
        await interaction.response.send_message("Updating role embed...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Permission check
        if ACRYLIC_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        embeds = []

        file = discord.File(os.path.abspath('./img/Roles.png'), filename="Roles.png")

        embed_exclusive = discord.Embed(color=16772213)
        embed_exclusive.add_field(inline=False, name=f"{STAR_EMOJI} Exclusive Roles {STAR_EMOJI}", value="----------------------------\n")
        embed_exclusive.add_field(inline=True, name="", value=f"{ACRYLIC_ROLE_EMOJI}{ACRYLIC_ROLE_MENTION}{ACRYLIC_ROLE_EMOJI}\nA role exclusive to the channel owner himself, Acrylic")
        embed_exclusive.add_field(inline=True, name="", value=f"{SALAMI_ROLE_EMOJI}{SALAMI_ROLE_MENTION}{SALAMI_ROLE_EMOJI}\nA role exclusive to Salami, the artist for the videos")
        embed_exclusive.add_field(inline=True, name="", value=f"{CREATORS_ROLE_EMOJI}{CREATORS_ROLE_MENTION}{CREATORS_ROLE_EMOJI}\nA role exclusive to the creators of the channel, its real purpose is just to group Acrylic and Salami together on the member list")
        embeds.append(embed_exclusive)

        embed_staff = discord.Embed(color=16772213)
        embed_staff.add_field(inline=False, name=f"{STAFF_EMOJI} Staff Roles {STAFF_EMOJI}", value="----------------------------\n")
        embed_staff.add_field(inline=True, name="", value=f"{ART_PANEL_ROLE_EMOJI}{ART_PANEL_ROLE_MENTION}{ART_PANEL_ROLE_EMOJI}\nBehind the scenes access to upcoming videos, providing feedback and suggested changes to make before the video is released publicly")
        embed_staff.add_field(inline=True, name="", value=f"{MOD_ROLE_EMOJI}{MOD_ROLE_MENTION}{MOD_ROLE_EMOJI}\nAccess to <@1396161419434655855> commands. Moderates server to ensure a safe environment for everybody")
        embeds.append(embed_staff)

        embed_community = discord.Embed(color=16772213)
        embed_community.add_field(inline=False, name=f"{COMMUNITY_EMOJI} Community Roles {COMMUNITY_EMOJI}", value="----------------------------\n")
        embed_community.add_field(inline=True, name="", value=f"{SPECIAL_ROLE_EMOJI}{SPECIAL_ROLE_MENTION}{SPECIAL_ROLE_EMOJI}\nGranted to users under special circumstances, say winning an event")
        embed_community.add_field(inline=True, name="", value=f"{SUPER_SUPPORTER_ROLE_EMOJI}{SUPER_SUPPORTER_ROLE_MENTION}{SUPER_SUPPORTER_ROLE_EMOJI}\nAutomatically granted to those who are a Tier 2, YouTube channel member and a Tier 3, Twitch sub. No additional perks, you just stand out more")
        embed_community.add_field(inline=True, name="", value=f"{MEMBER_TIER_2_ROLE_EMOJI}{MEMBER_TIER_2_ROLE_MENTION}{MEMBER_TIER_2_ROLE_EMOJI}\nAutomatically granted to those who are a Tier 2, YouTube channel member. See YouTube channel for perks")
        embed_community.add_field(inline=True, name="", value=f"{MEMBER_TIER_1_ROLE_EMOJI}{MEMBER_TIER_1_ROLE_MENTION}{MEMBER_TIER_1_ROLE_EMOJI}\nAutomatically granted to those who are a Tier 1, YouTube channel member. See YouTube channel for perks")
        embed_community.add_field(inline=True, name="", value=f"{MEMBER_ROLE_EMOJI}{MEMBER_ROLE_MENTION}{MEMBER_ROLE_EMOJI}\nAutomatically granted to anyone who is a YouTube channel member, regardless of tier. Comes with perms to change your nickname")
        embed_community.add_field(inline=True, name="", value=f"{SUB_TIER_3_ROLE_EMOJI}{SUB_TIER_3_ROLE_MENTION}{SUB_TIER_3_ROLE_EMOJI}\nAutomatically granted to those who are a Tier 3, Twitch sub")
        embed_community.add_field(inline=True, name="", value=f"{SUB_TIER_2_ROLE_EMOJI}{SUB_TIER_2_ROLE_MENTION}{SUB_TIER_2_ROLE_EMOJI}\nAutomatically granted to those who are a Tier 2, Twitch sub")
        embed_community.add_field(inline=True, name="", value=f"{SUB_TIER_1_ROLE_EMOJI}{SUB_TIER_1_ROLE_MENTION}{SUB_TIER_1_ROLE_EMOJI}\nAutomatically granted to those who are a Tier 1, Twitch sub")
        embed_community.add_field(inline=True, name="", value=f"{SUB_ROLE_EMOJI}{SUB_ROLE_MENTION}{SUB_ROLE_EMOJI}\nAutomatically granted to anyone who is a Twitch sub, regardless of tier. Comes with perms to change your nickname")
        embed_community.add_field(inline=True, name="", value=f"{BOOSTER_ROLE_EMOJI}{BOOSTER_ROLE_MENTION}{BOOSTER_ROLE_EMOJI}\nAutomatically granted to those who boost the server. Comes with perms to change your nickname")
        embed_community.add_field(inline=True, name="", value=f"{CONTRIBUTOR_ROLE_EMOJI}{CONTRIBUTOR_ROLE_MENTION}{CONTRIBUTOR_ROLE_EMOJI}\nGranted to those who have contributed to the channel in some way.")
        embed_community.add_field(inline=True, name="", value=f"{MUSICIAN_ROLE_EMOJI}{MUSICIAN_ROLE_MENTION}{MUSICIAN_ROLE_EMOJI}\nApply for this role using `/tools musician` and send your own music. Don't worry, your music isn't being judged on skill, the application process is just to prevent low effort content")
        embed_community.add_field(inline=True, name="", value=f"{ARTIST_ROLE_EMOJI}{ARTIST_ROLE_MENTION}{ARTIST_ROLE_EMOJI}\nApply for this role using `/tools artist` and send your own art. Don't worry, your art isn't being judged on skill, the application process is just to prevent low effort, stolen, and or A.I. art")
        embed_community.add_field(inline=True, name="", value=f"{GOOBER_2_ROLE_EMOJI}{GOOBER_2_ROLE_MENTION}{GOOBER_2_ROLE_EMOJI}\nRun `/tools goober2` at least 3 weeks after joining and you will be granted this role. Comes with perms to create polls, change your nickname, and start activities in voice chats")
        embed_community.add_field(inline=True, name="", value=f"{GOOBER_ROLE_EMOJI}{GOOBER_ROLE_MENTION}{GOOBER_ROLE_EMOJI}\nRun `/tools goober` at least 3 days after joining and you will be granted this role. Comes with extended reaction perms, along with image and embed perms")
        embeds.append(embed_community)

        embed_notification = discord.Embed(color=16772213)
        embed_notification.add_field(inline=False, name=f"{PUSHPIN_EMOJI} Notification Roles {PUSHPIN_EMOJI}", value="----------------------------\n")
        embed_notification.add_field(inline=True, name="", value=f"{POLL_PINGS_ROLE_MENTION}\nSometimes we host polls for everybody to participate in, not just channel members")
        embed_notification.add_field(inline=True, name="", value=f"{EVENT_PINGS_ROLE_MENTION}\nYou'll be pinged for events. What kind of events? idk maybe like a game sesh or something")
        embed_notification.add_field(inline=True, name="", value=f"{MERCH_PINGS_ROLE_MENTION}\nYou'll be pinged whenever new merch is announced and or dropped")
        embed_notification.add_field(inline=True, name="", value=f"{GIVEAWAY_PINGS_ROLE_MENTION}\nYou'll be pinged whenever a giveaway is hosted")
        embed_notification.add_field(inline=True, name="", value=f"{STREAM_PINGS_ROLE_MENTION}\nGet notified when Acrylic goes live")
        embed_notification.add_field(inline=True, name="", value=f"{SECOND_CHANNEL_PINGS_ROLE_MENTION}\nGet notified whenever a video is posted on the second channel")
        embed_notification.add_field(inline=True, name="", value=f"{VOD_CHANNEL_PINGS_ROLE_MENTION}\nYou'll be notified whenever a video is uploaded to the VOD channel")
        embed_notification.add_field(inline=False, name="", value="")
        embed_notification.add_field(inline=False, name="To obtain these roles, go to the \"Channels & Roles\" tab", value="")
        embeds.append(embed_notification)

        if edit:
            target_message = None
            for channel in interaction.guild.text_channels:
                try:
                    msg = await channel.fetch_message(ROLE_INFO_EMBED_MESSAGE_ID)
                    if msg:
                        target_message = msg
                        break
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    continue

            if not target_message:
                await interaction.followup.send(f"{WARNING_EMOJI} Message not found in any accessible text channel.", ephemeral=True)
                return
                
            await msg.edit(embeds=embeds)
            await interaction.followup.send(f"{CHECK_EMOJI} Role embeds have been updated.", ephemeral=True)
        else:
            role_channel = self.bot.get_channel(ROLE_INFO_CHANNEL_ID)
            if role_channel:
                await role_channel.send(embeds=embeds, file=file)
                #await role_channel.send(embed=embed_exclusive, file=file)
                #await role_channel.send(embed=embed_staff)
                #await role_channel.send(embed=embed_community)
                #await role_channel.send(embed=embed_notification)
                await interaction.followup.send(f"{CHECK_EMOJI} Role embeds have been created.", ephemeral=True)
            else:
                await interaction.followup.send(f"{WARNING_EMOJI} Role channel with ID {ROLE_INFO_CHANNEL_ID} not found.", ephemeral=True)

    
    @tools.command(name="role_colors", description="For creating the role color embed and dropdown in #role-colors.")
    async def roles(self, interaction: discord.Interaction):
        await interaction.response.send_message("Creating role color embed...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Permission check
        if ACRYLIC_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        file = discord.File(os.path.abspath('./img/RoleColors.png'), filename="RoleColors.png")

        embed = discord.Embed(color=16772213,description=f"Almost all roles in this server come with their own unique role color. But what do you do if you like the color of one role, but you can't use it because you have another role that's higher rank? You use this feature!\n\nYou can change your role color to that of any other role you own using the dropdown menu below. This also works with Sub/Membership roles! You will be able to use the color from lower ranking tiers, provided you have one ranked higher. For example, someone with {MEMBER_TIER_2_ROLE_MENTION} can use the role color of {MEMBER_TIER_1_ROLE_MENTION}.\n\nRole colors do not override role icons, so you will still have the icon of your highest ranking role, despite your choice of role color.\n\nIf, for any reason, you lose the role associated with your role color of choice, you will also lose that role color.\n\nIf you have a role color and want to remove it, pick the `None` option in the dropdown menu below. This will return you back to inheriting your role color from your highest ranking role.")

        color_channel = self.bot.get_channel(ROLE_COLOR_CHANNEL_ID)
        if color_channel:
            await color_channel.send(embed=embed,file=file,view=ColorsView())
            await interaction.followup.send(f"{CHECK_EMOJI} thing is created.", ephemeral=True)
        else:
            await interaction.followup.send(f"{WARNING_EMOJI} Color channel with ID {ROLE_COLOR_CHANNEL_ID} not found.", ephemeral=True)