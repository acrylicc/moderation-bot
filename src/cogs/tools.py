import discord
from discord.ext import commands
from discord import app_commands
from cogs.ids import *
from datetime import timedelta, datetime, timezone

class ToolsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    tools = app_commands.Group(name="tools", description="Jira's Tools and Utilities")

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
            print(f"{WARNING_EMOJI} Report channel with ID {REPORTS_CHANNEL_ID} not found.")

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
            print(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.")

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

        if tenure >= required_tenure:
            role = interaction.guild.get_role(GOOBER_ROLE_ID)
            if not role:
                await interaction.followup.send(f"{WARNING_EMOJI} Role not found. Check the GOOBER_ROLE_ID. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
                return

            if role in interaction.user.roles:
                await interaction.followup.send(f"{X_EMOJI} You already have Goober role.", ephemeral=True)
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
                    print(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.")

            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Failed to assign role to {interaction.user.mention}. Check my permissions. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
        else:
            remaining = required_tenure - tenure
            hours_left = int(remaining.total_seconds() // 3600)
            await interaction.followup.send(f"{X_EMOJI} You have only been in the server for {tenure.days} days.\nYou need **{hours_left} more hours** to qualify.", ephemeral=True)

    @tools.command(name="artist", description="Apply for Artist role.")
    async def uploadfile(self, interaction: discord.Interaction, file: discord.Attachment):
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
        apply_channel = self.bot.get_channel(APPLY_CHANNEL_ID)
        if not apply_channel:
            print(f"{WARNING_EMOJI} Apply channel with ID {APPLY_CHANNEL_ID} not found.")
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
            print(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.")

        # Confirm to user
        await interaction.followup.send(f"{CHECK_EMOJI} Your application for Artist role has been sent.", ephemeral=True)

    @tools.command(name="review_applicant", description="Accept or deny an applicant.")
    async def review_applicant(self, interaction: discord.Interaction, accepted: bool, member: discord.Member, message_id: str, reason: str = "No reason provided."):
        await interaction.response.send_message(f"{"Accepting" if accepted else "Denying"} member...", ephemeral=True)
        
        author_roles = [role.id for role in interaction.user.roles]

        # Check if the user has the authorized role
        if AUTHORIZED_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return
        
        try:
            message_id_int = int(message_id)
        except ValueError:
            await interaction.followup.send(f"{X_EMOJI} Invalid message ID format.", ephemeral=True)
            return
        
        apply_channel = self.bot.get_channel(APPLY_CHANNEL_ID)
        if not apply_channel:
            print(f"{WARNING_EMOJI} Apply channel with ID {APPLY_CHANNEL_ID} not found.")
            return
        
        try:
            message = await apply_channel.fetch_message(message_id_int)
            await message.delete()
        except discord.NotFound:
            await interaction.followup.send(f"{WARNING_EMOJI} Message not found in the application channel.", ephemeral=True)
            return
        except discord.Forbidden:
            await interaction.followup.send(f"{X_EMOJI} I don't have permission to delete that message.", ephemeral=True)
            return
        
        title = f"{CHECK_EMOJI} Artist Application Accepted" if accepted else f"{X_EMOJI} Artist Application Denied"
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
            print(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.")

        # Try to DM the user
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)
            #return

        # If accepted, assign the role
        if accepted:
            role = interaction.guild.get_role(ARTIST_ROLE_ID)
            if not role:
                await interaction.followup.send(f"{WARNING_EMOJI} Role not found. Check the ARTIST_ROLE_ID. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
                return
            try:
                await member.add_roles(role, reason=f"Accepted by {interaction.user} - {reason}")
            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Couldn't assign role to {member.mention}. Check my permissions. If you are seeing this, please report this to staff via `/tools report`.", ephemeral=True)
                return

        # Respond to the reviewer
        action = "accepted and given the role" if accepted else "denied"
        await interaction.followup.send(f"{CHECK_EMOJI} {member.mention} has been {action} and notified via DM (If possible).", ephemeral=True)
