class SpeakManager():
    def __init__(self):
        self.guild_to_textChannel = None
        
    def set(self, channel):
        self.guild_to_textChannel = channel
        
    def get(self):
        return self.guild_to_textChannel
    
    def delete(self):
        self.guild_to_textChannel = None
        
    def is_setted_textChannel(self, channel):
        return self.guild_to_textChannel == channel
    