import discord
from discord import app_commands
from discord.ext import commands
from exception.TalkBotException import NotExistDictionaryException
import service.VoiceService as VoiceService
import dictionary.UserDictionary as UserDictionary

class listDictionaryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="list_word", description="真紅ちゃんが知っている言葉を表示します。")
    async def listDictionary(self, interaction: discord.Interaction):
        
        try:
            if not VoiceService.is_exist_container(interaction):
                dictionary = UserDictionary.read_dictionary(interaction.guild.id)
            else:
                dictionary = VoiceService.list_dictionary(interaction)
        except(
            NotExistDictionaryException
        ) as e:
            embed = discord.Embed(title="うーん",description=e,color=0xff1100)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        words = ""
        for word in dictionary:
            define = dictionary[word]
            if(word.strip() == "" or define.strip() == ""):
                continue
            word.strip()
            define.strip()
            words += f"{word} : {define}\n"
        
        
        embed = discord.Embed(title="私はこんなに知ってるぞ！",description=words,color=0x3ded97)
        await interaction.response.send_message(embed=embed)

async def setup(bot : commands.Bot):
    await bot.add_cog(listDictionaryCommand(bot))