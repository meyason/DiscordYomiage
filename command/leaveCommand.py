import discord
from discord import app_commands
from discord.ext import commands
import service.VoiceService as VoiceService
from exception.TalkBotException import NotJoinedException, UserNotJoinedException

class leaveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "leave", description = "真紅ちゃんとさようならします。")
    async def leave(self, interaction: discord.Interaction):
        try:
            await VoiceService.leave(interaction)
        except(
            NotJoinedException,
            UserNotJoinedException
        ) as e:
            embed = discord.Embed(title="あれ？",description=e,color=0xff1100)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(title="成功",description="今日はいっぱい話せてうれしいよ。おやすみ。",color=0x3ded97)
        await interaction.response.send_message(embed=embed, ephemeral=True)
            
async def setup(bot : commands.Bot):
    await bot.add_cog(leaveCommand(bot))