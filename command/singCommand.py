import discord
from discord import app_commands
from discord.ext import commands
import service.VoiceService as VoiceService
from exception.TalkBotException import NotJoinedException, UserNotJoinedException
import os
import random

song_dict = {
    "aletheia.mp3": "アレセイア",
    "hikari.mp3": "ヒカリ輝くセカイ",
    "akasekaop.mp3" : "glowing world ～輝きの、セカイへ～",
    "sanctuary.mp3" : "サンクチュアリ",
    "akasekashinku.mp3" : "紅い瞳に映るセカイ feat.二階堂真紅",
    "colourfuldays.mp3" : "COLORFUL DAYS!!",
}

class singCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name = "sing", description = "真紅ちゃんが歌います。")
    async def sing(self, interaction: discord.Interaction):
        # audioディレクトリの中からランダムで再生
        # audioディレクトリ内のmp3ファイルを全て取得
        files = os.listdir("audio")
        mp3_files = [f for f in files if f.endswith(".mp3")]
        # ランダムで選択
        song = random.choice(mp3_files)
        print(song)

        try:
            await VoiceService.play(interaction, song)
        except(
            NotJoinedException,
            UserNotJoinedException
        ) as e:
            embed = discord.Embed(title="あれ？",description=e,color=0xff1100)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(title="よーし",description="聞いてくれ。「" + song_dict[song] + "」だ。",color=0x3ded97)
        await interaction.response.send_message(embed=embed)
            
async def setup(bot : commands.Bot):
    await bot.add_cog(singCommand(bot))