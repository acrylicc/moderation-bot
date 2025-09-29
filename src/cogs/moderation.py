import discord
from discord.ext import commands
from discord import app_commands
from cogs.ids import *
from datetime import timedelta, datetime, timezone
from typing import Optional
import json
import os

class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    mod = app_commands.Group(name="mod", description="Jira Moderation commands")

    def parse_duration(self, duration_str: str) -> Optional[timedelta]:
        """Parses duration strings like '10m', '2h', '1d' into timedelta."""
        try:
            unit = duration_str[-1]
            value = int(duration_str[:-1])
            if unit == "s":
                return timedelta(seconds=value)
            elif unit == "m":
                return timedelta(minutes=value)
            elif unit == "h":
                return timedelta(hours=value)
            elif unit == "d":
                return timedelta(days=value)
            else:
                return None
        except:
            return None
        
    def load_strikes(self):
        # Safe JSON loader (with empty file check)
        try:
            with open(os.path.abspath("./strikes.json"), "r") as f:
                data = f.read().strip()
                if not data:
                    return {}
                return json.loads(data)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(os.path.abspath("./strikes.json"), "w") as f:
                json.dump({}, f)
            return {}

    def save_strikes(self, data):
        with open(os.path.abspath("./strikes.json"), "w") as f:
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
                if len(data.get(guild_id, {}).get(user_id, [])) != original_len:
                    updated = True
            if not data[guild_id]:
                del data[guild_id]
                updated = True

        return updated


    @mod.command(name="ban", description="Ban a member from the server.")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str, message: str = "No additional message provided", silent: bool = True):
        await interaction.response.send_message("Banning member...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Check if the user has the authorized role
        if MOD_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        # Prevent banning users with protected roles
        try:
            target_roles = [role.id for role in member.roles]
            if any(role_id in PROTECTED_ROLE_IDS for role_id in target_roles) or ART_PANEL_ROLE_ID in target_roles:
                if CREATORS_ROLE_ID in author_roles and CREATORS_ROLE_ID not in target_roles:
                    pass
                else:
                    await interaction.followup.send(f"{X_EMOJI} You cannot ban this user because they have a protected role.", ephemeral=True)
                    return
        except:
            pass

        embed = discord.Embed(
            title=f"{LOCK_EMOJI} User Banned",
            description=f"**User:** {member.mention}\n**Reason:** {reason}\n**Message:** {message}\n**Moderator:** {interaction.user.mention}",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        # Try to DM the user
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)
            #return
        
        # Try banning the user
        try:
            await member.ban(reason=reason,delete_message_seconds=0)

            await interaction.followup.send(embed=embed, ephemeral=True)

            if silent is False:
                await interaction.followup.send(embed=embed)

            # Send to log channel
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
            else:
                await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send(f"{X_EMOJI} I don't have permission to ban this user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"{X_EMOJI} An unexpected error occurred: {str(e)}", ephemeral=True)

    @mod.command(name="pardon", description="Unban a user from the server.")
    async def pardon(self, interaction: discord.Interaction, user_id: str, silent: bool = True):
        await interaction.response.send_message("Unbanning member...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Check if the user has the authorized role
        if MOD_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        try:
            # Check if user is banned
            banned_user = None
            async for ban in interaction.guild.bans():
                if ban.user.id == int(user_id):
                    banned_user = ban
                    break

            if banned_user is None:
                await interaction.followup.send(f"{WARNING_EMOJI} This user is not banned.", ephemeral=True)
                return

            # Unban the user
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user)

            # Create the embed
            embed = discord.Embed(
                title=f"{UNLOCK_EMOJI} User Unbanned",
                description=f"**User:** {user.mention}\n**Moderator:** {interaction.user.mention}",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.timestamp = discord.utils.utcnow()

            await interaction.followup.send(embed=embed, ephemeral=True)

            if silent is False:
                await interaction.followup.send(embed=embed)

            # Send embed to log channel
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
            else:
                await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send(f"{X_EMOJI} I don't have permission to unban this user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"{X_EMOJI} An unexpected error occurred: {str(e)}", ephemeral=True)

    @mod.command(name="timeout", description="Temporarily timeout a member.")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str, message: str = "No additional message provided", silent: bool = True):
        await interaction.response.send_message("Timing member out...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Permission check
        if MOD_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        # Prevent timing out users with protected roles
        try:
            target_roles = [role.id for role in member.roles]
            if any(role_id in PROTECTED_ROLE_IDS for role_id in target_roles):
                if CREATORS_ROLE_ID in author_roles and CREATORS_ROLE_ID not in target_roles:
                    pass
                else:
                    await interaction.followup.send(f"{X_EMOJI} You cannot timeout this user because they have a protected role.", ephemeral=True)
                    return
        except:
            pass

        # Parse the duration string
        timeout_duration = self.parse_duration(duration)
        if not timeout_duration:
            await interaction.followup.send(f"{X_EMOJI} Invalid duration format. Use something like `10m`, `2h`, `1d`.", ephemeral=True)
            return

        try:
            until = discord.utils.utcnow() + timeout_duration
            await member.timeout(until, reason=reason)

            # Create the embed
            embed = discord.Embed(
                title=f"{HOURGLASS_EMOJI} User Timed Out",
                description=f"**User:** {member.mention}\n**Duration:** {duration}\n**Reason:** {reason}\n**Message:** {message}\n**Moderator:** {interaction.user.mention}",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.timestamp = discord.utils.utcnow()

            # Try to DM the user
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)

            # Respond in command channel
            await interaction.followup.send(embed=embed, ephemeral=True)

            if silent is False:
                await interaction.followup.send(embed=embed)

            # Send to log channel
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
            else:
                await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send(f"{X_EMOJI} I don't have permission to timeout this user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"{X_EMOJI} An unexpected error occurred: {str(e)}", ephemeral=True)

    @mod.command(name="untimeout", description="Remove timeout from a member.")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member, message: str = "No additional message provided", silent: bool = True):
        await interaction.response.send_message("Removing timeout from member...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Permission check
        if MOD_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        # Prevent timing out users with protected roles
        try:
            target_roles = [role.id for role in member.roles]
            if any(role_id in PROTECTED_ROLE_IDS for role_id in target_roles):
                if CREATORS_ROLE_ID in author_roles and CREATORS_ROLE_ID not in target_roles:
                    pass
                else:
                    await interaction.followup.send(f"{X_EMOJI} You cannot timeout this user because they have a protected role.", ephemeral=True)
                    return
        except:
            pass


        try:
            await member.timeout(discord.utils.utcnow() + self.parse_duration('0s'))

            # Create the embed
            embed = discord.Embed(
                title=f"{HOURGLASS_EMOJI} User Untimed Out",
                description=f"**User:** {member.mention}\n**Message:** {message}\n**Moderator:** {interaction.user.mention}",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.timestamp = discord.utils.utcnow()

            # Try to DM the user
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)

            # Respond in command channel
            await interaction.followup.send(embed=embed, ephemeral=True)

            if silent is False:
                await interaction.followup.send(embed=embed)

            # Send to log channel
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
            else:
                await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send(f"{X_EMOJI} I don't have permission to timeout this user.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"{X_EMOJI} An unexpected error occurred: {str(e)}", ephemeral=True)

    @mod.command(name="delete_message", description="Delete a message by its ID.")
    async def delete_message(self, interaction: discord.Interaction, message_id: str, reason: str, message: str = "No additional message provided", should_resend: bool = True, silent: bool = True):
        await interaction.response.send_message("Deleting message...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Check permission role
        if MOD_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        try:
            # Prevent deletion of protected message IDs
            message_id_int = int(message_id)
            if message_id_int in RESTRICTED_MESSAGE_IDS:
                await interaction.followup.send(f"{X_EMOJI} This message is restricted and cannot be deleted.", ephemeral=True)
                return

            # Search all text channels for the message
            target_message = None
            for channel in interaction.guild.text_channels:
                try:
                    msg = await channel.fetch_message(message_id_int)
                    member = msg.author
                    if msg:
                        target_message = msg
                        break
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    continue

            if not target_message:
                await interaction.followup.send(f"{WARNING_EMOJI} Message not found in any accessible text channel.", ephemeral=True)
                return

            # Check if message author has protected roles
            if isinstance(target_message.author, discord.Member):
                target_roles = [role.id for role in target_message.author.roles]
                if any(rid in PROTECTED_ROLE_IDS for rid in target_roles):
                    if CREATORS_ROLE_ID in author_roles and CREATORS_ROLE_ID not in target_roles:
                        pass
                    else:
                        await interaction.followup.send(f"{X_EMOJI} Cannot delete messages from protected users.", ephemeral=True)
                        return

            # Create response embed
            embed = discord.Embed(
                title=f"{TRASH_EMOJI} Message Deleted",
                description=f"""
                **Message ID:** `{message_id}`
                **Channel:** {target_message.channel.mention}
                **Author:** {target_message.author.mention}
                **Reason:** {reason}
                **Message:** {message}
                **Moderator:** {interaction.user.mention}
                """,
                color=discord.Color.red()
            )

            embed.timestamp = discord.utils.utcnow()

            if should_resend:
                resend_files = []
                if target_message.attachments:
                    for attachment in target_message.attachments:
                        try:
                            # Convert attachment to discord.File
                            file = await attachment.to_file(use_cached=True)
                            resend_files.append(file)
                        except Exception as e:
                            await interaction.followup.send(f"{X_EMOJI} Could not resend some attachments due to an error: {e}", ephemeral=True)

            # Send to log channel
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_message = await log_channel.send(embed=embed)

                if should_resend:
                    thread_title = f"Deleted Message"
                    thread = await log_message.create_thread(
                        name=thread_title,
                        auto_archive_duration=60
                    )

                    content_preview = target_message.content or "*[No text content]*"
                    if len(content_preview) > 1900:
                        content_preview = content_preview[:1900] + "\n... *(truncated)*"

                    resend_embed = discord.Embed(
                        title=f"{CLIPBOARD_EMOJI} Original Message Contents",
                        description=content_preview,
                        color=discord.Color.orange()
                    )
                    resend_embed.set_author(name=str(target_message.author), icon_url=target_message.author.display_avatar.url)
                    resend_embed.timestamp = discord.utils.utcnow()

                    await thread.send(embed=resend_embed)

                    # Resend attachments if any
                    if resend_files:
                        await thread.send(files=resend_files)
            else:
                await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

            # Try to DM the user
            try:
                await member.send(embed=embed)
                if should_resend:
                    await member.send(embed=resend_embed)
                    if resend_files:
                        dm_files = []
                        for attachment in target_message.attachments:
                            file = await attachment.to_file(use_cached=True)
                            dm_files.append(file)
                        await member.send(files=dm_files)
            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)

            await target_message.delete()
            
            if silent is False:
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"{X_EMOJI} An unexpected error occurred: {str(e)}", ephemeral=True)

    @mod.command(name="strike", description="Give a member a strike.")
    async def strike(self, interaction: discord.Interaction, member: discord.Member, reason: str, message: str = "No additional message provided", silent: bool = True):
        await interaction.response.send_message("Giving strike to member...", ephemeral=True)
        author_roles = [role.id for role in interaction.user.roles]

        # Permission check
        if MOD_ROLE_ID not in author_roles:
            await interaction.followup.send(f"{X_EMOJI} You don't have permission to use this command.", ephemeral=True)
            return

        # Prevent striking users with protected roles
        try:
            target_roles = [role.id for role in member.roles]
            if any(role_id in PROTECTED_ROLE_IDS for role_id in target_roles):
                if CREATORS_ROLE_ID in author_roles and CREATORS_ROLE_ID not in target_roles:
                    pass
                else:
                    await interaction.followup.send(f"{X_EMOJI} You cannot strike this user because they have a protected role.", ephemeral=True)
                    return
        except Exception:
            pass

        try:
            data = self.load_strikes()
            guild_id = str(interaction.guild.id)
            user_id = str(member.id)
            now = datetime.now(timezone.utc)

            # Ensure structure exists to avoid KeyError
            data.setdefault(guild_id, {}).setdefault(user_id, [])

            # Clean expired strikes
            if self.clean_expired_strikes(data):
                self.save_strikes(data)

            # Make sure keys still exist after cleanup
            data.setdefault(guild_id, {}).setdefault(user_id, [])

            # Add new strike
            data[guild_id][user_id].append({
                "timestamp": now.isoformat()
            })


            self.save_strikes(data)

            # Prepare embed
            embed = discord.Embed(
                title=f"{X_EMOJI} User Striked",
                description=(
                    f"**User:** {member.mention}\n"
                    f"**Reason:** {reason}\n"
                    f"**Message:** {message}\n"
                    f"**Moderator:** {interaction.user.mention}"
                ),
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.timestamp = now

            # DM the user
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)

            # Always respond to the staff member
            await interaction.followup.send(embed=embed, ephemeral=True)

            # Optionally show public embed
            if not silent:
                await interaction.channel.send(embed=embed)

            # Log to mod-log
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)
            else:
                await interaction.followup.send(f"{WARNING_EMOJI} Log channel with ID {LOG_CHANNEL_ID} not found.", ephemeral=True)

            # Check for 4 strikes (ban)
            if len(data[guild_id][user_id]) >= 4:
                ban_embed = discord.Embed(
                    title=f"{LOCK_EMOJI} User {"Soft-Banned" if ART_PANEL_ROLE_ID in target_roles else "Banned"}",
                    description=(
                        f"**User:** {member.mention}\n"
                        f"**Reason:** Reached 4 active strikes.\n"
                        f"**Moderator:** <@1396161419434655855>"
                    ),
                    color=discord.Color.red()
                )
                ban_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                ban_embed.timestamp = now

                try:
                    await member.send(embed=ban_embed)
                except discord.Forbidden:
                    await interaction.followup.send(f"{WARNING_EMOJI} Couldn't DM {member.mention}. They might have DMs disabled.", ephemeral=True)

                try:
                    if ART_PANEL_ROLE_ID in target_roles:
                        await member.timeout(discord.utils.utcnow() + self.parse_duration('20d'))
                    else:
                        await member.ban(reason="Reached 4 active strikes.", delete_message_seconds=0)
                    await interaction.followup.send(embed=ban_embed, ephemeral=True)
                    if not silent:
                        await interaction.channel.send(embed=ban_embed)
                    if log_channel:
                        await log_channel.send(embed=ban_embed)
                except discord.Forbidden:
                    await interaction.followup.send(f"{X_EMOJI} I don't have permission to ban this user.", ephemeral=True)
                except Exception as e:
                    await interaction.followup.send(f"{X_EMOJI} An unexpected error occurred: {str(e)}", ephemeral=True)
                return

            # If 2 or more strikes, revoke goober roles
            elif len(data[guild_id][user_id]) >= 2:
                goober_role = interaction.guild.get_role(GOOBER_ROLE_ID)
                goober_2_role = interaction.guild.get_role(GOOBER_2_ROLE_ID)

                try:
                    if goober_role in member.roles:
                        await member.remove_roles(goober_role, reason="Reached 2+ active strikes.")
                    if goober_2_role in member.roles:
                        await member.remove_roles(goober_2_role, reason="Reached 2+ active strikes.")
                except Exception as e:
                    await interaction.followup.send(f"{WARNING_EMOJI} Could not remove Goober roles: {e}", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"{X_EMOJI} An unexpected error occurred: {str(e)}", ephemeral=True)
