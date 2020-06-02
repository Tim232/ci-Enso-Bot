import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ';')

@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(activity=discord.Game(name='With Tiddies'))

@client.event
async def on_member_join(member):
    print (f'{member} has joined the server')

@client.event
async def on_member_removed(member):
    print (f'{member} has has left the server')

@client.command(aliases = ["ping"])
@commands.has_any_role('Hamothy')
async def Ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#@client.command(aliases = ['8ball'])
#async def _8ball(ctx, *, question):
#    Responses = ["Hamothy believes it is certain",
#                 "Kate decides it will come true",
#                 "Josh doesn't believe.",
#                 "Izzy can't predict this",
#                 "Idk idiot lmao",
#                 "Why are you even askin me",
#                 "its not like i can read ur question"]
#    await ctx.send(f'Question: {question}\nAnswer: {random.choice(Responses)}')

@client.command()
@commands.has_any_role('Hamothy')
async def roles(ctx):
    embed = discord.Embed(title="```So you wanna know how the leveled roles system works huh?```", colour=discord.Colour(0x30e419), description="------------------------------------------------")

    embed.set_image(url="https://media.discordapp.net/attachments/669812887564320769/717149671771996180/unknown.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/683490529862090814/715010931620446269/image1.jpg")
    embed.set_author(name="Hamothy", icon_url="https://cdn.discordapp.com/attachments/689525645734182916/717137453651066900/Rias_Gremory.png")
    embed.set_footer(text="-------------------------------------------------------------------------------------------------------")

    embed.add_field(name = "Cooldown", value="**•XP is gained every time you talk with a 2 minute cooldown.**", inline=True),
    embed.add_field(name = "Message Length",value = "**•XP is not determined by the size of the message. You will not get more XP just because the message is bigger.**", inline = True),
    embed.add_field(name = "Roles",value="**•As seen below, those are the colours and roles that will be achieved upon gaining that amount of experience**", inline = True)

    await ctx.send(embed=embed)


client.run('NzE2NzAxNjk5MTQ1NzI4MDk0.XtWFiw.KZrh9Tkp9vTY9JYSgZfpg2P4mlQ')