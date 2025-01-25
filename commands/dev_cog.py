import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = os.getenv("GUILD_ID")

class DevCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
           
    async def commands_autocomplete(
        self, interaction: discord.Interaction, current: str,
    ) -> list[discord.app_commands.Choice[str]]:
        commands_files = os.listdir('./commands')
        commands = []
        for file in commands_files:
            if file.endswith('.py'):
                commands.append(file[:-3])
        return [
            discord.app_commands.Choice(name=command, value=command)
            for command in commands if current.lower() in command.lower()
        ]
    
    # /ping
    @discord.app_commands.command(name='ping', description='🏓')
    async def ping(self, interaction: discord.Interaction):
        return await interaction.response.send_message(f'Is this working?', ephemeral=True)
    
    # /reload [command]
    @discord.app_commands.command(name='reload', description='Recarrega um comando.')
    @discord.app_commands.autocomplete(command=commands_autocomplete)
    async def reload(self, interaction: discord.Interaction, command: str):
        try:
            await self.bot.reload_extension(f'commands.{command}')
            await self.bot.tree.sync()
        except Exception as e:
            return await interaction.response.send_message(f'[ERROR] - {e}')
        return await interaction.response.send_message(f'{command} foi recarregado com sucesso.')
    
    # /unload [command]
    @discord.app_commands.command(name='unload', description='Descarrega um comando.')
    @discord.app_commands.autocomplete(command=commands_autocomplete)
    async def unload(self, interaction: discord.Interaction, command: str):
        try:
            await self.bot.reload_extension(f'commands.{command}')
        except Exception as e:
            return await interaction.response.send_message(f'[ERROR] - {e}')
        await interaction.response.send_message(f'{command} foi descarregado com sucesso.')
        
    # /load [command]
    @discord.app_commands.command(name='load', description='Carrega um comando.')
    @discord.app_commands.autocomplete(command=commands_autocomplete)
    async def unload(self, interaction: discord.Interaction, command: str):
        try:
            await self.bot.load_extension(f'commands.{command}')
        except Exception as e:
            return await interaction.response.send_message(f'[ERROR] - {e}')
        await interaction.response.send_message(f'{command} foi carregado com sucesso.')
        
async def setup(bot):
    await bot.add_cog(DevCog(bot), guilds=[discord.Object(id=GUILD_ID)])