from exception.TalkBotException import *
from manager.BotManager import BotManager
from model.SpeakManager import SpeakManager
from dictionary.UserDictionary import UserDictionary
from discord.player import FFmpegPCMAudio

botmanager = BotManager.get_instance()

def leaveCheck(interaction):
    if not(interaction.guild.voice_client and interaction.guild.voice_client.is_connected()):
        raise NotJoinedException()
    
async def join(interaction):
    if interaction.user.voice is None:
        raise UserNotJoinedException()
    
    if interaction.guild.voice_client and interaction.guild.voice_client.is_connected():
        raise AlreadyJoinedException()
    
    botmanager.initialize(interaction.guild.id, SpeakManager(), UserDictionary(interaction.guild.id))

    botmanager.get_speakmanager(interaction.guild.id).set(interaction.channel)

    await interaction.user.voice.channel.connect()

async def leave(interaction):
    if not(interaction.guild.voice_client and interaction.guild.voice_client.is_connected()):
        raise NotJoinedException()
    if interaction.user.voice is None:
        raise UserNotJoinedException()
    
    botmanager.delete_manager(interaction.guild.id)
    
    await interaction.guild.voice_client.disconnect()

async def talk(interaction, text):
    shinku = botmanager.get_shinku(interaction.guild.id)
    textformatter = botmanager.get_textformatter(interaction.guild.id)
    userdictionary = botmanager.get_userdictionary(interaction.guild.id)

    text = textformatter.format_text(text, userdictionary.dictionary)
    audio = await shinku.talk(text)
    interaction.guild.voice_client.play(FFmpegPCMAudio(audio, pipe=True))

def is_exist_container(interaction):
    return botmanager.is_exist_manager(interaction.guild.id)

def add_dictinary(interaction, word, yomikata):
    userdictionary = botmanager.get_userdictionary(interaction.guild.id)

    dictionary = userdictionary.dictionary
    if word in dictionary:
        raise AlreadyExistWordException()
    if word.strip() == "" or yomikata.strip() == "":
        raise EmptyWordException()
    
    userdictionary.add(word, yomikata)
    userdictionary.write()

def delete_dictionary(interaction, word):
    userdictionary = botmanager.get_userdictionary(interaction.guild.id)
    
    dictionary = userdictionary.dictionary
    if word not in dictionary:
        raise NotExistWordException()
    if word.strip() == "":
        raise EmptyWordException()
    
    userdictionary.delete_word(word)
    userdictionary.write()

def list_dictionary(interaction):
    userdictionary = botmanager.get_userdictionary(interaction.guild.id)
    
    dictionary = userdictionary.dictionary
    if not dictionary:
        raise NotExistDictionaryException()
    
    return dictionary