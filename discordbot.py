import discord
from discord.player import FFmpegPCMAudio
from discord.ext import commands
from command.Command import load_extension
from exception.TalkBotException import *
from logger.Logger import enable_logging
from service.TextFormatter import TextFormatter
import model.ShinkuTalker as ShinkuTalker
from Config.Config import DISCORD_TOKEN, EXCEPT_BOTS, LOGGING
from manager.BotManager import BotManager
import datetime
import asyncio
import signal


intents=discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='***', intents = intents)
textformatter = TextFormatter()
botmanager = BotManager.get_instance()

@bot.event
async def on_ready():
    print('Running...') 
    
@bot.event
async def on_message(message):
    now = datetime.datetime.now()
    # 指定したbot以外のbotは無視
    except_bot_ids = [int(bot_id) for bot_id in EXCEPT_BOTS.split(',')]
    if message.author.bot and not message.author.id in except_bot_ids:
        return
    # メッセージが送信されたdiscordグループを取得
    guild = message.guild
    # メッセージが送信されたdiscordグループでbotがボイスチャンネルに参加しているか確認
    if guild.voice_client is None:
        return
    # ターゲットのテキストチャンネルか確認
    if not botmanager.is_exist_manager(guild.id):
        return
    speakmanager = botmanager.get_speakmanager(guild.id)
    userdictionary = botmanager.get_userdictionary(guild.id)
    if not speakmanager.is_setted_textChannel(message.channel):
        return
    isSingen = botmanager.get_singen(guild.id)
    if isSingen:
        if(guild.voice_client.is_playing()):
            return
        botmanager.set_singen(guild.id, False)

    try:
        # 添付ファイルの場合を考慮
        if message.attachments or type(message.content) is not str:
            text = "添付ファイルだ。"
        else:
            # メンションはdisplayNameに変換
            print(message.content)
            text = message.content
            flag = False
            for mention in message.mentions:
                # メンションがこのbotの場合は削除
                if mention.id == bot.user.id:
                    flag = True
                    text = text.replace(f"<@{mention.id}>", "")
                    continue
                text = text.replace(f"<@{mention.id}>", "アットマーク" + mention.display_name)

            limit = 500
            if flag:
                # botをメンションした場合は文字数制限を緩和
                limit = 5000
            text = textformatter.format_text(text, userdictionary.dictionary, limit)
            if text == "":
                return
            
        if guild.voice_client.is_playing():
            guild.voice_client.stop()

        audio = await asyncio.wait_for(shinku.talk(text), timeout=60)

    except Exception as e:
        print(e)
        error_message = "ごめん、これはちょっと無理かもだ。"
        await message.channel.send(error_message)
        audio = await shinku.talk(error_message)
    
    print("ロード時間: ", datetime.datetime.now() - now)

    guild.voice_client.play(FFmpegPCMAudio(audio, pipe=True))
    
@bot.event
async def on_voice_state_update(member, before, after):
    # 参加していない場合は無視
    if not member.guild.voice_client:
        return
    if before.channel:
        if len(before.channel.members) == 1:
            botmanager.delete_manager(member.guild.id)
            await member.guild.voice_client.disconnect()
            return
    
    # ユーザーがボイスチャンネルに参加した場合ユーザー名を取得
    if before.channel != after.channel:
        if after.channel:
            # botは無視
            if member.bot:
                return
            # 参加してるチャンネルと違う場合は無視
            if member.guild.voice_client.channel != after.channel:
                return
            isSingen = botmanager.get_singen(member.guild.id)
            if isSingen:
                if(member.guild.voice_client.is_playing()):
                    return
                botmanager.set_singen(member.guild.id, False)
            text = f"やあ、{member.display_name}。"
            userdictionary = botmanager.get_userdictionary(member.guild.id)
            text = textformatter.format_text(text, userdictionary.dictionary)
            audio = await shinku.talk(text)
            member.guild.voice_client.play(FFmpegPCMAudio(audio, pipe=True))

async def main():
    await load_extension(bot)
    print('Bot is ready.')
    signal.signal(signal.SIGINT, signal_handler)
    await bot.start(DISCORD_TOKEN)

def signal_handler(signal, frame):
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown_bot())

async def shutdown_bot():
    for vc in bot.voice_clients:
        await vc.disconnect()
    await bot.close()
    
if LOGGING:
    enable_logging()
model = ShinkuTalker.preloader()
shinku = ShinkuTalker.ShinkuTalker(model)
botmanager.registerShinkuTalker(shinku)
botmanager.registerTextFormatter(textformatter)

asyncio.run(main())

    
