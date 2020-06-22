import asyncio
import datetime
import random
import string

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

import settings
from cogs.Embeds import error_function


class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~Kakashi command for Zara
    @commands.command(aliases=['Kakashi'])
    async def kakashi(self, ctx):

        # Surround with try/except to catch any exceptions that may occur
        try:

            with open('images/WaifuImages/kakashiImages.txt') as file:
                kakashi_array = file.readlines()

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(title="**Hatake Kakashi**",
                                      colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(kakashi_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # Bot ~Toga command for Josh
    @commands.command(aliases=['Toga'])
    async def toga(self, ctx):

        try:

            with open('images/WaifuImages/togaImages.txt') as file:
                toga_array = file.readlines()

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # Set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(title="**Himiko Toga**",
                                      colour=discord.Colour(int(random.choice(settings.colour_list))))
                embed.set_image(url=random.choice(toga_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # Bot ~Tamaki command for Kate
    @commands.command(aliases=['Tamaki'])
    async def tamaki(self, ctx):

        try:
            with open('images/WaifuImages/tamakiImages.txt') as file:
                tamaki_array = file.readlines()

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:

                # set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(title="**Tamaki Suoh**",
                                      colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(tamaki_array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            else:

                message = await ctx.send(error_function())

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # Bot ~Husk command for Kaiju
    @commands.command(aliases=['Husk'])
    async def husk(self, ctx):

        # Surround with try/except to catch any exceptions that may occur
        try:

            if ctx.author.id == 552153335516495873:
                with open('images/WaifuImages/husk.txt') as file:
                    husk_array = file.readlines()

                # If the channel that the command has been sent is in the list of accepted channels
                if str(ctx.channel) in settings.channels:

                    # Set member as the author
                    member = ctx.message.author
                    userAvatar = member.avatar_url

                    embed = discord.Embed(title="**Husk**",
                                          colour=discord.Colour(random.choice(settings.colour_list)))
                    embed.set_image(url=random.choice(husk_array))
                    embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed=embed)

                else:

                    message = await ctx.send(error_function())

                    # Let the user read the message for 2.5 seconds
                    await asyncio.sleep(2.5)
                    # Delete the message
                    await message.delete()
            else:
                # Send an error message to the user saying that they don't have permission to use this command
                message = await ctx.send("Uh oh! You don't have permission to use this command!")

                # Let the user read the message for 2.5 seconds
                await asyncio.sleep(2.5)
                # Delete the message
                await message.delete()

        except FileNotFoundError as e:
            print(e)

    # Bot ~ensoPerson command for the server members
    @commands.command(aliases=['enso', 'Ensoperson'])
    @cooldown(1, 1, BucketType.user)
    async def ensoperson(self, ctx, name=None):
        array = ['hammy', 'hussein', 'inna', 'kaiju', 'kate',
                 'lukas', 'marshall', 'stitch', 'zara', 'josh',
                 'gria', 'lilu', 'marcus', 'eric', 'ifrah',
                 'janet', 'connor', 'taz', 'ryder', 'ange',
                 'izzy', 'david', 'clarity', 'angel', 'chloe',
                 'corona', 'skye']

        def displayServerImage(array, ctx, name):
            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:
                # Set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"**Look At What A Cutie {name.capitalize()} is!! <a:huh:676195228872474643> <a:huh:676195228872474643> **",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()

                return embed

        if name:
            proper_name = name.lower()
            try:
                with open(f'images/ServerMembers/{proper_name}.txt') as file:
                    images_array = file.readlines()

                    embed = displayServerImage(images_array, ctx, proper_name)
                    await ctx.send(embed=embed)

            except Exception as e:
                print(e)

                await ctx.send(f"Sorry! That person doesn't exist!! Try the names listed below!")

                nice = string.capwords(', '.join(map(str, array)))
                await ctx.send(nice)

        else:
            with open(f'images/ServerMembers/{random.choice(array)}.txt') as file:
                array = file.readlines()

            # If the channel that the command has been sent is in the list of accepted channels
            if str(ctx.channel) in settings.channels:
                # Set member as the author
                member = ctx.message.author
                userAvatar = member.avatar_url

                embed = discord.Embed(
                    title=f"Oh Look! A Cute Person <a:huh:676195228872474643> <a:huh:676195228872474643> ",
                    colour=discord.Colour(random.choice(settings.colour_list)))
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Waifus(bot))
