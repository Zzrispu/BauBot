import os
import discord
from discord.ext import commands

from config import TOKEN, OWNER_ID

bot = commands.Bot(command_prefix='🐢', intents=discord.Intents.all())
bot.owner_id = OWNER_ID

async def load_commands():
    for file in os.listdir('./commands'):
        if file.endswith('.py'):
            name = file[:-3]
            await bot.load_extension(name=f'commands.{name}')

@bot.event
async def on_ready():
    await load_commands()
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)} comandos foram carregados.')
    except Exception as e:
        return print(f'[ERROR] - {e}')
    
    await bot.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name='🧑‍🍳 Cozinhando...'))
    print(f'{bot.user} está online!')

bot.run(TOKEN)