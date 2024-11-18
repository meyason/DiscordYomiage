import discord
from discord import app_commands
from discord.ext import commands
from exception.TalkBotException import AlreadyExistWordException, EmptyWordException
import service.VoiceService as VoiceService
import dictionary.UserDictionary as UserDictionary

class addDictionaryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="add_word", description="真紅ちゃんに言葉を教えます。")
    async def addDictionary(self, interaction: discord.Interaction, word: str, yomikata: str):
        
        try:
            # "äüöß"は単語区切り用に使うので、入ってたら削除
            if "äüöß" in word:
                word = word.replace("äüöß", "")
            
            # 300字以上はカットオフ
            word = word[:300]

            if not VoiceService.is_exist_container(interaction):
                UserDictionary.add_dictionary(interaction.guild.id, word, yomikata)
            else:
                VoiceService.add_dictinary(interaction, word, yomikata)
        except(
            AlreadyExistWordException,
            EmptyWordException
        ) as e:
            embed = discord.Embed(title="あれ？",description=e,color=0xff1100)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        
        embed = discord.Embed(title="了解だ。",description="よし。覚えたぞ！",color=0x3ded97)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot : commands.Bot):
    await bot.add_cog(addDictionaryCommand(bot))