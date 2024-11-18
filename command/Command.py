INITIAL_EXTENSIONS = [
    'command.joinCommand',
    'command.leaveCommand',
    'command.addDictionaryCommand',
    'command.deleteDictionaryCommand',
    'command.listDictionaryCommand',
]

async def load_extension(bot):
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)