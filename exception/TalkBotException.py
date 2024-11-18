class MusicBotException(Exception):
    def __init__(self, arg=""):
        self.arg = arg

class AlreadyJoinedException(MusicBotException):
    def __str__(self):
        return (
            "すでに私はいるぞ。"
        )
    
class UserNotJoinedException(MusicBotException):
    def __str__(self):
        return (
            "お前、ボイスチャットにいないじゃないか。からかってるのかよ。"
        )
    
class NotJoinedException(MusicBotException):
    def __str__(self) -> str:
        return (
            "私はいないぞ。"
        )
    
class NotSameVoiceChannelException(MusicBotException):
    def __str__(self) -> str:
        return (
            "お前と私は違うチャンネルにいるみたいだな。"
        )
    
class FailTalkException(MusicBotException):
    def __str__(self) -> str:
        return (
            "ごめん、ちょっとこれは無理かもだ。"
        )
    
class AlreadyExistWordException(MusicBotException):
    def __str__(self) -> str:
        return (
            "その言葉はもう知ってるぞ。"
        )
    
class NotExistWordException(MusicBotException):
    def __str__(self) -> str:
        return (
            "その言葉は知らないな..."
        )
    
class EmptyWordException(MusicBotException):
    def __str__(self) -> str:
        return (
            "どういう言葉なんだ？教えてくれ。"
        )

class NotExistDictionaryException(MusicBotException):
    def __str__(self) -> str:
        return (
            "私、何も知らないみたいだ。"
        )
    