import discord
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
import gspread    # https://github.com/burnash/gspread
import asyncio
import datetime
import configparser

# Set up gspread and connect to sheet ==================================================

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('banker-bot-be73f3796456.json', scope)

gc = gspread.authorize(credentials)

sht1 = gc.open_by_key('1OZE3X0pDjxkeYg5AQWB9aH-j2g3GyR79jdSzB7ue-n4') # test sheet
worksheet = sht1.sheet1

# ======================================================================================


# Pull values from config file==========================================================

config = configparser.ConfigParser()
config.read('settings.ini')

# ======================================================================================


# Configure the bot's prefix ===========================================================

PREFIX = config['DEFAULT']['BotPrefix']
TOKEN = config['DEFAULT']['BotToken']

#tokenfile=open("./bottoken.txt", "r")
#if tokenfile.mode == 'r':
#	TOKEN = tokenfile.read()
#
#tokenfile.close()

# ======================================================================================

#
#val = worksheet.acell('A1').value
#
#print(val)
#worksheet.update_acell('B1', 'Bingo!')

client = commands.Bot(command_prefix = '!')
client.remove_command("help") # Removes the default help command to make way for the custom one below. This line must come BEFORE the new help command is compiled.

#client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Client commands ======================================================================
 
# Re-login to gspread every n minutes so that the oauth2 token does not expire, otherwise you get a 401 error after an arbitrary time post first-login (supposedly 1 hour)
# Remember to call this function with "client.loop.create_task(stay_alive())" at the end otherwise it won't run
async def stay_alive():
    await client.wait_until_ready()
    while not client.is_closed: # While the bot is running
        gc.login()
        await asyncio.sleep(600) # 10 minutes
        print('re-logged in to gspread')


# Lists all the bot commands and their usage
@client.command(pass_context=True)
async def help(ctx: commands.Context):
    embed = discord.Embed(
        colour = discord.Color(0x44ACFF)
        )
    embed.set_author(name="Bot Commands")
    embed.add_field(name=".help", value="Displays this message.", inline=False)
    embed.add_field(name=".history", value="Shows the total number of requests from a reddit user so far. Example: `.history u/Legion`.", inline=False)
    embed.add_field(name=".uptime", value="Shows how long the bot has been online.", inline=False)
    embed.set_footer(text="Questions or bugs? Please contact BOT AUTHOR NAME.")
    await client.say(embed=embed)
 
# Displays how long the bot has been online
@client.command(pass_context=True)
async def uptime(ctx: commands.Context):
    now = datetime.datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await client.say("{} has been up for {}".format(client.user.name, uptime_stamp))
 
# ======================================================================================

#@client.event
#async def on_message(message):
#    if message.content.startswith('!test'):
#        counter = 0
#        tmp = await client.send_message(message.channel, 'Calculating messages...')
#        async for log in client.logs_from(message.channel, limit=100):
#            if log.author == message.author:
#                counter += 1
#
#        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
#    elif message.content.startswith('!sleep'):
#        await asyncio.sleep(5)
#        await client.send_message(message.channel, 'Done sleeping')

client.loop.create_task(stay_alive())
client.run(TOKEN)

