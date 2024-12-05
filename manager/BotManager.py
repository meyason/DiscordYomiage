
class BotManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BotManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__container = {}
        return cls._instance

    def registerShinkuTalker(self, shinku):
        self.__shinku = shinku

    def registerTextFormatter(self, textformatter):
        self.__textformatter = textformatter
    
    def initialize(self, guild_id, speakmanager, userdictionary):
        self.__container[guild_id] = {"speakmanager": speakmanager, "userdictionary": userdictionary, "shinku": self.__shinku, "textformatter": self.__textformatter, "singen": False}

    def get_speakmanager(self, guild_id):
        return self.__container[guild_id]["speakmanager"]
    
    def get_userdictionary(self, guild_id):
        return self.__container[guild_id]["userdictionary"]
    
    def set_singen(self, guild_id, singen):
        self.__container[guild_id]["singen"] = singen

    def get_singen(self, guild_id):
        return self.__container[guild_id]["singen"]
    
    def get_shinku(self, guild_id):
        return self.__container[guild_id]["shinku"]
    
    def get_textformatter(self, guild_id):
        return self.__container[guild_id]["textformatter"]
    
    def is_exist_manager(self, guild_id):
        return guild_id in self.__container
    
    def delete_manager(self, guild_id):
        self.__container[guild_id]["userdictionary"].delete_memory_dictionary()
        self.__container[guild_id]["speakmanager"].delete()
        del self.__container[guild_id]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.__container = {}
        return cls._instance 

