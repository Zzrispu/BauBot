import discord
import aiohttp
import asyncio
from discord.ext import commands
from datetime import datetime

class MC_Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    @discord.app_commands.command(name='serverstatus', description='Responde uma embed do status do server, atualiza a cada segundo.')
    async def server_status(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer(ephemeral=True)
        
        async def get_status():
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.mcstatus.io/v2/status/java/147.185.221.17:36608') as response:
                    if response.status == 200:
                        response = await response.json()
                        
                        motd = ''
                        if 'motd' in response:
                            motd = response['motd']['clean']
                        else:
                            motd = 'bruh...'
                        
                        embed = discord.Embed(title='『Servidor do Baú』', description=f'*{motd}*')
                        embed.add_field(name='IP', value='147.185.221.17:36608', inline=True)
                        embed.add_field(name='Versão', value='1.20.1', inline=True)
                        embed.set_thumbnail(url=self.bot.user.avatar)
                        
                        if response['online'] == True:
                            embed.color = 0x228b22
                            
                            players = ''
                            if len(response['players']['list']) > 0:
                                for player in response['players']['list']:
                                    players += f'{player['name_clean']}\n'
                            else:
                                players = 'Não há players online'
                            
                            embed.add_field(name=f'Players {response['players']['online']}/{response['players']['max']}', value=players, inline=False)
                        else:
                            embed.color = 0xff0000
                            
                            embed.add_field(name='O servidor está offline', value='💻🔨🐒', inline=False)
                        
                        embed.add_field(name='Última Atualização', value=f'<t:{round(datetime.now().timestamp())}:R>', inline=False)
                        return embed
        
                    else:
                        return discord.Embed(title='[ERROR]', description='response.status')

        msg = await channel.send(embed=await get_status())
        await interaction.followup.send(content=f'ServerStatus foi mandada em {channel}.')
        
        while True:
            try:
                await asyncio.sleep(19)
                message = await channel.fetch_message(msg.id)
                await message.edit(embed=await get_status())
            except discord.errors.HTTPException as e:
                print(f'[ERROR] - HTTPException: {e}')
                break
            except Exception as e:
                print(f'[ERROR] - {e}')
                break
            

async def setup(bot):
    await bot.add_cog(MC_Server(bot))