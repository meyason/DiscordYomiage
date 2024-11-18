import discord
from discord import app_commands
from discord.ext import commands
from exception.TalkBotException import AlreadyJoinedException, UserNotJoinedException
import service.VoiceService as VoiceService

class joinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="join", description="真紅ちゃんを呼びます。")
    async def join(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            await VoiceService.join(interaction)
        except(
            AlreadyJoinedException,
            UserNotJoinedException
        ) as e:
            embed = discord.Embed(title="あれ？",description=e,color=0xff1100)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        message = "おはよう。私が読み上げるな。"
        await VoiceService.talk(interaction, message)

        embed = discord.Embed(title="成功", description="おはよう。私が読み上げるな。", color=0x00ff00)
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot : commands.Bot):
    await bot.add_cog(joinCommand(bot))