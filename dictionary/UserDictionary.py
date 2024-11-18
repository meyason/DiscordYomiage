import os
from exception.TalkBotException import *

class UserDictionary:

    def __init__(self, guild_id):
        self.guild_id = guild_id
        file_name = f"{self.guild_id}_dictionary.dic"
        dir_name = f"dictionary\\files"
        if file_name not in os.listdir(dir_name):
            print("dictionary not found")
            self.create()
            word_dictionary = {}
        else:
            word_dictionary = self.read()
        self.dictionary = word_dictionary

    def delete_memory_dictionary(self):
        self.dictionary = {}

    def add(self, word, definition):
        self.dictionary[word] = definition

    def search(self, word):
        return self.dictionary[word]
    
    def delete_word(self, word):
        del self.dictionary[word]
    
    def write(self):
        file_name = f"dictionary\\files\\{self.guild_id}_dictionary.dic"
        with open(file_name, mode='w', encoding='utf-8') as f:
            for word, definition in self.dictionary.items():
                word = word.strip()
                definition = definition.strip()
                f.write(f"{word}" + " äüöß " + f"{definition}\n")

    def read(self):
        word_dictionary = {}
        file_name = f"dictionary\\files\\{self.guild_id}_dictionary.dic"
        with open(file_name, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if(line.strip() == ""):
                    continue
                print("line : "  + line)
                word, definition = line.split(" äüöß ")
                word_dictionary[word] = definition
            print("dictionary read")
            return word_dictionary

    def create(self):
        file_name = f"dictionary\\files\\{self.guild_id}_dictionary.dic"
        with open(file_name, mode='w', encoding='utf-8') as f:
            f.write("")
            


# BotManagerのコンテナにguild_idが存在しない場合（未接続時）は以下を使って直接書き込み        
            
def read_dictionary(guild_id):
    if f"{guild_id}_dictionary.dic" not in os.listdir("dictionary\\files"):
        with open(f"dictionary\\files\\{guild_id}_dictionary.dic", mode='w', encoding='utf-8') as f:
            f.write("")
        raise NotExistDictionaryException()
    
    with open(f"dictionary\\files\\{guild_id}_dictionary.dic", mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        dictionary = {}
        if lines == []:
            raise NotExistDictionaryException()
        for line in lines:
            print(line)
            if(line.strip() == ""):
                continue
            print(line.split(" äüöß "))
            word, definition = line.split(" äüöß ")
            dictionary[word] = definition
        return dictionary
    
def add_dictionary(guild_id, word, yomikata):
    if word.strip() == "" or yomikata.strip() == "":
        raise EmptyWordException()
    dictionary = read_dictionary(guild_id)
    if word in dictionary:
        raise AlreadyExistWordException()
    with open(f"dictionary\\files\\{guild_id}_dictionary.dic", mode='a', encoding='utf-8') as f:
        word = word.strip()
        yomikata = yomikata.strip()
        f.write(f"{word} äüöß {yomikata}\n")

def delete_dictionary(guild_id, word):
    dictionary = read_dictionary(guild_id)
    if word not in dictionary:
        raise NotExistWordException()
    with open(f"dictionary\\files\\{guild_id}_dictionary.dic", mode='w', encoding='utf-8') as f:
        for w, y in dictionary.items():
            if w == word:
                continue
            w = w.strip()
            y = y.strip()
            f.write(f"{w} äüöß {y}\n")

