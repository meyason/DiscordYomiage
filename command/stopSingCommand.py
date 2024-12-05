import discord
from discord import app_commands
from discord.ext import commands
import service.VoiceService as VoiceService
from exception.TalkBotException import NotJoinedException, UserNotJoinedException, NotSingException

class stopSingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "stop", description = "真紅ちゃんの歌を止めます。")
    async def stop_sing(self, interaction: discord.Interaction):

        try:
            await VoiceService.stop(interaction)
        except(
            NotJoinedException,
            UserNotJoinedException,
            NotSingException
        ) as e:
            embed = discord.Embed(title="あれ？",description=e,color=0xff1100)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(title="そ、そっか",description="歌うの楽しかったよ。",color=0x3ded97)
        await interaction.response.send_message(embed=embed, ephemeral=True)
            
async def setup(bot : commands.Bot):
    await bot.add_cog(stopSingCommand(bot))