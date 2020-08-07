import asyncio
import datetime
import os
import random

import aiomysql
import discord
from discord import Embed
from discord import File
from discord.ext.commands import has_permissions, Cog, group, bot_has_permissions

from settings import enso_embedmod_colours, blank_space, storage_modlog_for_guild, remove_modlog_channel, \
    get_modlog_for_guild


async def generate_embed(ctx, desc):
    """Generate New Error Embed"""

    embed = Embed(description=desc,
                  colour=enso_embedmod_colours)

    await ctx.send(embed=embed)


# Method to ask the user if they want to be anonymous or not
def anon_or_not(author):
    # Set up embed to let the user how to start sending modmail
    AnonModMailEmbed = Embed(title="**Want to send it Anonymously?**",
                             colour=enso_embedmod_colours,
                             timestamp=datetime.datetime.utcnow())

    AnonModMailEmbed.set_thumbnail(url=author.avatar_url)
    AnonModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [(blank_space, "**We understand that for some things,"
                            "you may want to remain Anonymous."
                            "\nUse the reactions below to choose!**", False),
              (blank_space, "**Use :white_check_mark: for** `Yes`", True),
              (blank_space, "**Use :x: for** `No`", True),
              (blank_space, blank_space, True),
              (blank_space,
               "The Staff will not know who is sending this"
               "\nPurely negative feedback will not be considered.", True)]

    for name, value, inline in fields:
        AnonModMailEmbed.add_field(name=name, value=value, inline=inline)

    return AnonModMailEmbed


# Method to send an embed to to let the user know to type into chat
def send_instructions(author):
    # Set up embed to let the user know that they have aborted the modmail
    SendModMailEmbed = Embed(title="**Please enter a message for it to be sent to the staff!**",
                             colour=enso_embedmod_colours,
                             timestamp=datetime.datetime.utcnow())

    SendModMailEmbed.set_thumbnail(url=author.avatar_url)
    SendModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [("**Make sure that the message is above **50** and below **1024** characters!**",
               "**Include as much detail as possible :P**",
               False)]

    for name, value, inline in fields:
        SendModMailEmbed.add_field(name=name, value=value, inline=inline)

    return SendModMailEmbed


# Method to let the user know that the message must be above 50 characters
def error_handling(author):
    # Set up embed to let the user know that the message must be above 50 characters
    ErrorHandlingEmbed = Embed(
        title="Uh Oh! Please make sure the message is above **50** and below **1024** characters!",
        colour=enso_embedmod_colours,
        timestamp=datetime.datetime.utcnow())

    ErrorHandlingEmbed.set_thumbnail(url=author.avatar_url)
    ErrorHandlingEmbed.set_footer(text=f"Sent by {author}")

    fields = [("Please enter in a message which is above **50** and below **1024** characters!",
               "**This helps us reduce spam and allows you to include more detail in your mail!**",
               False)]

    for name, value, inline in fields:
        ErrorHandlingEmbed.add_field(name=name, value=value, inline=inline)

    return ErrorHandlingEmbed


# Method to send an embed into chat to let the user know that their mail has been sent successfully
def message_sent_confirmation(author):
    # Set up embed to let the user know that they have sent the mail
    ConfirmationEmbed = Embed(title="**Message relayed to Staff!!**",
                              colour=enso_embedmod_colours,
                              timestamp=datetime.datetime.utcnow())

    ConfirmationEmbed.set_thumbnail(url=author.avatar_url)
    ConfirmationEmbed.set_footer(text=f"Sent by {author}")

    fields = [("Thank you for your input! The staff team appreciate it very much!",
               f"\n As mentioned previously, please don't be hesistant to DM the Staff for anything! :P",
               False)]

    for name, value, inline in fields:
        ConfirmationEmbed.add_field(name=name, value=value, inline=inline)

    return ConfirmationEmbed


# Method to actually allow the message to be sent to #mod-mail
def send_modmail(self, msg, author):
    embed = Embed(title="Modmail",
                  colour=enso_embedmod_colours,
                  timestamp=datetime.datetime.utcnow())

    if self.anon:

        embed.set_thumbnail(url=random.choice(self.avatars))
        embed.set_footer(text=f"Sent By Anon Member")

        fields = [("Member", "Anon Member", False),
                  ("Message", msg.content, False)]
    else:

        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text=f"Sent By {author}")

        fields = [("Member", author, False),
                  ("Message", msg.content, False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    return embed


# Set up the Cog
class Guild(Cog):
    """Modmail System!"""

    def __init__(self, bot):
        self.bot = bot
        self.anon = None
        self.avatars = ["https://cdn.discordapp.com/embed/avatars/0.png",
                        "https://cdn.discordapp.com/embed/avatars/1.png",
                        "https://cdn.discordapp.com/embed/avatars/2.png",
                        "https://cdn.discordapp.com/embed/avatars/3.png",
                        "https://cdn.discordapp.com/embed/avatars/4.png"]

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @group(invoke_without_command=True, usage="`[argument...]`")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def modlogs(self, ctx):
        """
        Show Current Modlogs Channel (If Setup)
        """

        ml_channel = get_modlog_for_guild(str(ctx.guild.id))

        # Send current modlogs channel only if it is setup
        # Send error if no modlogs channel has been setup
        if ml_channel is not None:

            # Get the modlog channel for the current guild
            channel = ctx.guild.get_channel(int(ml_channel))

            text = f"**The current modlogs channel is set to {channel.mention}**"
            await generate_embed(ctx, text)
        else:

            text = "**Modlogs Channel** already set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await generate_embed(ctx, text)

    @modlogs.command(name="setup")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mlsetup(self, ctx, channelID: int):
        """Setup a Channel for the Kick/Ban/Mute Actions to be Logged In"""

        # Retrieve a list of channel id's in the guild
        channels = [channel.id for channel in ctx.guild.channels]

        # Setup pool
        pool = self.bot.db

        # Setup pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the row of the guild
                select_query = """SELECT * FROM guilds WHERE guildID = (%s)"""
                val = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, val)
                result = await cur.fetchone()

        # Throw error if the modlog channel already exists and then stop the function
        if result[2] is not None:
            text = "**Modlogs Channel** already set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await generate_embed(ctx, text)
            return

        # Abort the process if the channel does not exist within the guild
        if channelID not in channels:
            text = "**Invalid ChannelID Detected... Aborting Process**"
            await generate_embed(ctx, text)

        else:
            # Set up the modlogs channel within the guild
            mod_log_setup = True
            await storage_modlog_for_guild(self.bot.db, ctx, channelID, mod_log_setup)

    @modlogs.command(name="update")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mlupdate(self, ctx, channelID: int):
        """Change the Channel that your Modlogs are Sent to"""

        # Retrieve a list of channel id's in the guild
        channels = [channel.id for channel in ctx.guild.channels]

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the guilds row from the guilds table
                select_query = """SELECT * FROM guilds WHERE guildID = (%s)"""
                vals = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

        # Throw error if the modlog channel already exists and then stop the function
        if result[2] is None:
            text = "**Modlogs Channel** not set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await generate_embed(ctx, text)

        # Abort the process if the channel does not exist within the guild
        if channelID not in channels:
            text = "**Invalid ChannelID Detected... Aborting Process**"
            await generate_embed(ctx, text)

        else:
            # Update the modlog channel within the database and cache
            mod_log_setup = False
            await storage_modlog_for_guild(self.bot.db, ctx, channelID, mod_log_setup)

    @modlogs.command("delete")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mldelete(self, ctx):
        """Delete the Existing Modlogs System"""

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the guilds row from the guilds table
                select_query = """SELECT * FROM guilds WHERE guildID = (%s)"""
                vals = ctx.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

        # Throw error is modlogs error has not been setup before performing a delete action
        if result[2] is None:
            text = "**Modlogs Channel** not set up!" \
                   f"\nDo **{ctx.prefix}help modlogs** to find out more!"
            await generate_embed(ctx, text)
            return

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Update the existing prefix within the database
                update_query = """UPDATE guilds SET modlogs = NULL WHERE guildID = (%s)"""
                update_vals = ctx.guild.id,

                # Execute the query
                await cur.execute(update_query, update_vals)
                await conn.commit()

        # Delete channel from cache
        remove_modlog_channel(str(ctx.guild.id))

        text = "**Modlogs System** successfully deleted!" \
               f"\nDo **{ctx.prefix}help modlogs** to setup Modlogs again!"
        await generate_embed(ctx, text)
        # Sending confirmation message that the modmail system has been deleted
        await ctx.send()

    @group(invoke_without_command=True, usage="`[argument...]`")
    @bot_has_permissions(administrator=True)
    async def modmail(self, ctx):
        """
        Show Current Modlogs Channel (If Setup)
        Setup/Update/Delete Modmail System
        """
        pass

    @modmail.command(name="setup")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mmsetup(self, ctx, channelID: int):
        """
        Setup Modmail System
        Input the ID of the Channel where the Modmail will be sent
        """

        # Retrieve a list of channel id's in the guild
        channels = [channel.id for channel in ctx.guild.channels]

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                val = ctx.author.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, val)
                result = await cur.fetchone()

        # Throw error if the guild already exists and then stop the function
        if result is not None:
            text = "**Modmail System** already set up!" \
                   f"\nDo **{ctx.prefix}help modmail** to find out more!"
            await generate_embed(ctx, text)
            return

        # As long as the channel exists within the guild
        if channelID in channels:

            # Ask for the channel ID that the modmail should be logged to
            await ctx.send("**Please enter the ID of the channel you want your modmail to be sent**")

            # Check the response is from the author and from the same channel as the previous message
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            # Wait for the message from the author
            msg = await self.bot.wait_for('message', check=check)

            # As long as the channel exists within the guild
            if int(msg.content) in channels:

                desc = "React to this message if you want to send a message to the Staff Team!" \
                       "\n\n**React with ✅**" \
                       "\n\nWe encourage all suggestions/thoughts and opinions on the server!" \
                       "\nAs long as it is **valid** criticism" \
                       "\n\n**Purely negative feedback will not be considered**"

                # Set up embed to let the user how to start sending modmail
                ModMail = Embed(title="**Welcome to Modmail!**",
                                description=desc,
                                colour=enso_embedmod_colours,
                                timestamp=datetime.datetime.utcnow())

                ModMail.set_thumbnail(url=self.bot.user.avatar_url)

                try:
                    # Get the channel object from the channelID input by the user
                    channel = ctx.author.guild.get_channel(channelID)
                    modmailchannelID = await channel.send(embed=ModMail)

                    # Auto add the ✅ reaction
                    await modmailchannelID.add_reaction('✅')

                    # Setup up pool connection and cursor
                    async with pool.acquire() as conn:
                        async with conn.cursor() as cur:
                            # Define the insert statement that will insert information about the modmail channel
                            insert_query = """INSERT INTO moderatormail (guildID, channelID, messageID, modmailChannelID) VALUES (%s, %s, %s, %s)"""
                            vals = ctx.author.guild.id, channelID, modmailchannelID.id, int(msg.content),

                            # Execute the SQL Query
                            await cur.execute(insert_query, vals)
                            await conn.commit()

                        text = "**Modmail System** is successfully set up!" \
                               f"\nRefer to **{ctx.prefix}help modmail** for more information"
                        await generate_embed(ctx, text)
                        return

                except aiomysql.IntegrityError:
                    text = "**Modmail System** already set up!" \
                           f"\nRefer to **{ctx.prefix}help modmail** for more information"
                    await generate_embed(ctx, text)
            else:
                # Send error message if the channel ID is not recognised
                text = "**Invalid ChannelID Detected... Aborting Process**"
                await generate_embed(ctx, text)
                return
        else:
            # Send error message if the channel ID is not recognised
            text = "**Invalid ChannelID Detected... Aborting Process**"
            await generate_embed(ctx, text)
            return

    @modmail.command(name="update")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mmupdate(self, ctx, channelID: int):
        """
        Update the Channel that the Modmail is logged to
        Input the ID of the New Channel
        """

        # Retrieve a list of channel id's in the guild
        channels = [channel.id for channel in ctx.guild.channels]

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                vals = ctx.author.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

            # Throw error if the guild already exists and then stop the function
            if result is None:
                text = "**Modmail System** not set up!" \
                       f"\nDo **{ctx.prefix}help modmail** to find out more!"
                await generate_embed(ctx, text)
                return

        # As long as the channel exists within the guild
        if channelID in channels:

            try:

                # Setup up pool connection and cursor
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        # Define the update statement that will insert information about the modmail channel
                        update_query = """UPDATE moderatormail SET modmailChannelID = (%s) WHERE guildID = (%s)"""
                        vals = channelID, ctx.author.guild.id

                        # Execute the SQL Query
                        await cur.execute(update_query, vals)
                        await conn.commit()

            except aiomysql.Error:
                text = "**Something Went Wrong! >:( Try Again Later!**"
                await generate_embed(ctx, text)

            # Send confirmation that the channel has been updated
            channel = ctx.author.guild.get_channel(channelID)
            text = "**Channel Updated**" \
                   f"\nNew Modmail will be sent to {channel.mention}"
            await generate_embed(ctx, text)

        else:
            # Send error message if the channel ID is not recognised
            text = "**Invalid ChannelID Detected... Aborting Process**"
            await generate_embed(ctx, text)
            return

    @modmail.command(name="delete")
    @has_permissions(manage_guild=True)
    @bot_has_permissions(administrator=True)
    async def mmdelete(self, ctx):
        """Delete the Entire Modmail System from the Guild"""

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                vals = ctx.author.guild.id,

                # Execute the SQL Query
                await cur.execute(select_query, vals)
                result = await cur.fetchone()

            # Throw error if modmail system does not exist already
            if result is None:
                text = "**Modmail System** not set up!" \
                       f"\nDo **{ctx.prefix}help modmail** to find out more!"
                await generate_embed(ctx, text)
                return

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Define the delete statement to remove all information about the guild
                delete_query = """DELETE FROM moderatormail WHERE guildID = (%s)"""
                vals = ctx.author.guild.id,

                # Execute the SQL Query
                await cur.execute(delete_query, vals)
                await conn.commit()

            # Sending confirmation message that the modmail system has been deleted
            text = "**Modmail System** successfully deleted!" \
                   f"\nDo **{ctx.prefix}help modmail** to find out more!"
            await generate_embed(ctx, text)

    # Setting up Listener to listen for reactions within the modmail channel created
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Don't count reactions that are made by the bot
        if payload.user_id == self.bot.user.id:
            return

        # Don't count other reactions other than ✅ and ❌
        elif payload.user_id:
            if str(payload.emoji) not in ['✅', '❌']:
                return

        # Find a role corresponding to the Emoji name.
        guildid = payload.guild_id

        # Setup pool
        pool = self.bot.db

        # Setup up pool connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the author's row from the Members Table
                select_query = """SELECT * FROM moderatormail WHERE guildID = (%s)"""
                val = guildid,

                # Execute the SQL Query
                await cur.execute(select_query, val)
                result = await cur.fetchone()

            # Adding error handling
            if result is None:
                return

            # Define variables
            guild_id = int(result[0])
            channel_id = int(result[1])
            message_id = int(result[2])
            modmail_channel_id = int(result[3])

        # Bunch of checks to make sure it has the right guild, channel, message and reaction
        if payload.guild_id == guild_id and payload.channel_id == channel_id and payload.message_id == message_id and payload.emoji.name == "✅":

            # Get the guild
            guild = self.bot.get_guild(payload.guild_id)
            # Get the member
            member = guild.get_member(payload.user_id)
            # Get the setup modmail channel
            channel = guild.get_channel(payload.channel_id)
            # Get the modmail logging channel
            modmail_channel = guild.get_channel(modmail_channel_id)

            # Fetch the message and remove the reaction
            reaction = await channel.fetch_message(message_id)
            await reaction.remove_reaction('✅', member)

            # Setting up the channel permissions for the new channel that will be created
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                guild.me: discord.PermissionOverwrite(administrator=True),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            # Saving this for later within when discord.py 1.4 comes out
            # cat = await guild.create_category_channel(member.name, overwrites=overwrites, position=0)

            # Create the text channel
            user_channel = await guild.create_text_channel(member.name, overwrites=overwrites,
                                                           position=0)

            # Mention the user to make sure that they get pinged
            mention = await user_channel.send(member.mention)
            await mention.delete()

            try:

                # Send the embed if they want to remain anonymous or not
                Anon_or_Not = await user_channel.send(embed=anon_or_not(member))
                # Add reactions to the message
                await Anon_or_Not.add_reaction('✅')
                await Anon_or_Not.add_reaction('❌')

                # Checking if the user reacted with ✅ with response to sending staff a message
                def emoji_check(reaction, user):
                    return user == member and str(reaction.emoji) in ['✅', '❌']

                # Surround with try/except to catch any exceptions that may occur
                try:
                    # Wait for the user to add a reaction
                    reaction, user = await self.bot.wait_for('reaction_add', check=emoji_check)
                except Exception as ex:
                    print(ex)
                    return
                else:
                    if str(reaction.emoji) == "✅":
                        self.anon = True

                        # Delete the old embed
                        await Anon_or_Not.delete()

                        # Tell the user to type their mail into the chat
                        instructions = await user_channel.send(embed=send_instructions(member))

                        # Making sure that the reply is from the author
                        def check(m):
                            return m.author == payload.member and user_channel.id == instructions.channel.id

                        # Wait for the message from the author
                        msg = await self.bot.wait_for('message', check=check)

                        # Making sure that the message is below 50 characters and the message was sent in the channel
                        while len(msg.content) < 50 and msg.channel == user_channel:
                            await user_channel.send(embed=error_handling(member))

                            # Wait for the message from the author
                            msg = await self.bot.wait_for('message', check=check)

                        # As long as the message is above 50 characters and in the correct channel
                        if len(msg.content) > 50 and msg.channel == user_channel:
                            # Delete the previous embed
                            await instructions.delete()

                            # Determine a path for the message logs to be stored
                            path = "cogs/Anon.txt"
                            with open(path, 'a+') as f:
                                # Store the date and content of every message in the text file
                                async for message in user_channel.history(limit=300):
                                    print(f"{message.created_at} : {message.content}", file=f)

                            # Send the message to the modmail channel
                            await modmail_channel.send(embed=send_modmail(self, msg, member),
                                                       file=File(fp=path))

                            # Removing file from the directory after it has been sent
                            if os.path.exists(path):
                                os.remove(path)
                            else:
                                print("The file does not exist")

                            # Make sure the user knows that their message has been sent
                            await user_channel.send(embed=message_sent_confirmation(member))

                            # Let the user read the message for 5 seconds
                            await asyncio.sleep(5)

                            # Delete the channel and then stop the function
                            await user_channel.delete()
                            return

                        # If the user types anywhere else, delete the channel
                        else:
                            await user_channel.delete()
                            return

                    if str(reaction.emoji) == "❌":
                        self.anon = False

                        # Delete the old embed
                        await Anon_or_Not.delete()

                        # Tell the user to type their mail into the chat
                        instructions = await user_channel.send(embed=send_instructions(member))

                        # Making sure that the reply is from the author
                        def check(m):
                            return m.author == payload.member and user_channel.id == instructions.channel.id

                        # Wait for the message from the author
                        msg = await self.bot.wait_for('message', check=check, timeout=300)

                        # Making sure that the message is below 50 characters and the message was sent in the channel
                        while len(msg.content) < 50 and msg.channel == user_channel:
                            await user_channel.send(embed=error_handling(member))

                            # Wait for the message from the author again
                            msg = await self.bot.wait_for('message', check=check, timeout=300)

                        if len(msg.content) > 50 and msg.channel == user_channel:
                            # Delete the previous embed
                            await instructions.delete()

                            # Determine a path for the message logs to be stored
                            path = "cogs/{}.txt".format(payload.member.name)
                            with open(path, 'a+') as f:
                                # Store the date and content of every message in the text file
                                async for message in user_channel.history(limit=300):
                                    print(f"{message.created_at} : {message.content}", file=f)

                            # Send the message to the modmail channel
                            await modmail_channel.send(embed=send_modmail(self, msg, member),
                                                       file=File(fp=path))

                            # Removing file from the directory after it has been sent
                            if os.path.exists(path):
                                os.remove(path)
                            else:
                                print("The file does not exist")

                            # Make sure the user knows that their message has been sent
                            await user_channel.send(embed=message_sent_confirmation(member))

                            # Let the user read the message for 5 seconds
                            await asyncio.sleep(5)

                            # Delete the channel and then stop the function
                            await user_channel.delete()
                            return

                        # If the user types anywhere else, delete the channel
                        else:
                            await user_channel.delete()
                            return

            except Exception as ex:
                print(ex)

                # Removing file from the directory after it has been sent
                if os.path.exists(path):
                    os.remove(path)
                else:
                    print("The file does not exist")

                # Send out an error message if the user waited too long
                await user_channel.send(
                    "Sorry! Something seems to have gone wrong and the modmail will be aborting."
                    "\nRemember to make sure it's under **1024** characters!!")

                await asyncio.sleep(5)
                await user_channel.delete()


def setup(bot):
    bot.add_cog(Guild(bot))
