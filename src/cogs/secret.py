import discord
from discord.ext import commands
from discord import app_commands
from cogs.ids import *
import os
from cogs.characters import character_replace

class SecretCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    secret = app_commands.Group(name="secret", description="Top Secret Commands! Shh!")

    @secret.command(name="acrylic", description="Exclusive.")
    async def acrylic(self, interaction: discord.Interaction, string: str, member: discord.Member = None, custom: bool = False):
        await interaction.response.send_message("Sending secret message...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Permission check
        if ACRYLIC_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        # Respond in command channel
        if member:
            try:
                if custom:
                    await member.send(character_replace(string))
                else:
                    await member.send(string)
            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)
        else:
            if custom:
                await interaction.channel.send(character_replace(string))
            else:
                await interaction.channel.send(string)
        await interaction.followup.send(f"{CHECK_EMOJI} Message sent if possible.", ephemeral=True)

    @secret.command(name="role", description="For managing member's roles.")
    async def role(self, interaction: discord.Interaction, give: bool, role: discord.Role, member: discord.Member, reason: str = "No reason provided", silent: bool = True):
        await interaction.response.send_message(f"Giving role to {member.mention}..." if give else f"Removing role from {member.mention}...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Permission check
        if ACRYLIC_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return
        

        embed = discord.Embed(
            title=f"You've Been Promoted To \"{role.name}\" Role!" if give else f"You've Been Demoted From \"{role.name}\" Role",
            description=f"**Reason:** {reason}",
            color=role.color
        )
        if role.icon:
            embed.set_thumbnail(url=role.icon.url)
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(icon_url=interaction.user.avatar.url,name=interaction.user.global_name)

        if give:
            member_roles = [role.id for role in member.roles]
            if role.id in member_roles:
                await interaction.followup.send(f"{X_EMOJI} {member.mention} already has {role.mention}.", ephemeral=True)
                return
            
            await member.add_roles(role, reason=reason)
        elif give == False:
            member_roles = [role.id for role in member.roles]
            if role.id not in member_roles:
                await interaction.followup.send(f"{X_EMOJI} {member.mention} does not have {role.mention}, so it cannot be revoked.", ephemeral=True)
                return
            
            await member.remove_roles(role, reason=reason)

        # DM the user
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)

        name = member.nick if member.nick else member.global_name if member.global_name else member.name
        embed = discord.Embed(
            title=f"{name} Has Been Promoted To \"{role.name}\" Role!" if give else f"{name} Has Been Demoted From \"{role.name}\" Role",
            description=f"**Reason:** {reason}",
            color=role.color
        )
        if role.icon:
            embed.set_thumbnail(url=role.icon.url)
        embed.timestamp = discord.utils.utcnow()

        # Always respond to the staff member
        await interaction.followup.send(embed=embed, ephemeral=True)

        # Optionally show public embed
        if not silent:
            await interaction.channel.send(embed=embed)