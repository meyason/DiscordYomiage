import discord
from discord import app_commands
from discord.ext import commands
from exception.TalkBotException import NotExistWordException, EmptyWordException
import service.VoiceService as VoiceService
import dictionary.UserDictionary as UserDictionary

class deleteDictionaryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="delete_word", description="真紅ちゃんから言葉を奪います。")
    async def deleteDictionary(self, interaction: discord.Interaction, word: str):
        
        try:
            if not VoiceService.is_exist_container(interaction):
                UserDictionary.delete_dictionary(interaction.guild.id, word)
            else:
                VoiceService.delete_dictionary(interaction, word)
        except(
            NotExistWordException,
            EmptyWordException
        ) as e:
            embed = discord.Embed(title="うーん",description=e,color=0xff1100)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        
        embed = discord.Embed(title="えーっと",description="あれ...？　なんだったかな",color=0x3ded97)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot : commands.Bot):
    await bot.add_cog(deleteDictionaryCommand(bot))