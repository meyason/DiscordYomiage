import re
import romkan
import jaconv

class TextFormatter:

    def __init__(self):
        # bep-eng.dicからローマ字->かな辞書取得
        # https://fastapi.metacpan.org/source/MASH/Lingua-JA-Yomi-0.01/lib/Lingua/JA
        dic_file = 'service\\bep-eng.dic'
        dict = {}
        with open(dic_file, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if i >= 6:
                    line_list = line.replace('\n', '').split(' ')
                    dict[line_list[0]] = line_list[1]
        self.dict = dict

    def format_text(self, text, dictionary):
        # URLの正規表現パターン
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        
        # URLのチェック
        if url_pattern.match(text):
            return "URL"
        
        #``````で囲まれた部分はコードと読む
        text = re.sub(r'``````(.+?)``````', 'コード', text)
        
        """
        堀江晶太はほりえしょうたに変換
        これは外せない
        お好みで消してもいい
        """
        text = text.replace('堀江', 'ほりえ')
        text = text.replace('晶太', 'しょうた')

        # ユーザー辞書を取得し、単語を置換
        for word, definition in dictionary.items():
            text = text.replace(word, definition)

        # 全角アルファベットを半角アルファベットに変換
        text = jaconv.z2h(text, kana=False, digit=False, ascii=True)
        
        # アルファベットを取得し、辞書にある英単語をかなに変換
        words = re.findall(r'[a-zA-Z]+', text)
        for word in words:
            upper_word = word.upper()
            if upper_word == 'W' or re.fullmatch(r'[ｗw]+', word, re.IGNORECASE):
                text = re.sub(word, ' ふふふっ。', text)
            elif upper_word in self.dict:
                text = text.replace(word, self.dict[upper_word])

        # ローマ字を日本語に変換
        text = romkan.to_kana(text)

        
        # 文字数が1000字を超える場合省略
        if len(text) > 500:
            return text[:500] + "以下略"
        
        return text


if __name__ == "__main__":
    formatter = TextFormatter()
    print(formatter.format_text("https://example.com"))  # "URL"
    print(formatter.format_text("a" * 1001))  # "aaaaaaaa...以下略"
    print(formatter.format_text("konnnichiwa"))  # "コンニチハ"
    print(formatter.format_text("これはｓｈですね"))  # "これはshですね"
    print(formatter.format_text("これはテストです。"))