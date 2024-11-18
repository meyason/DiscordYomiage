from Config.Config import MODEL_PATH, CONFIG_PATH, STYLE_PATH
from style_bert_vits2.tts_model import TTSModel
from style_bert_vits2.nlp import bert_models
from style_bert_vits2.constants import Languages
import io
import soundfile as sf
import pydub
import asyncio

def preloader():
    model_file = MODEL_PATH
    config_file = CONFIG_PATH
    style_file = STYLE_PATH

    bert_models.load_model(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")
    bert_models.load_tokenizer(Languages.JP, "ku-nlp/deberta-v2-large-japanese-char-wwm")

    model = TTSModel(
        model_file,
        config_file,
        style_file,
        device="cuda"
    )
    print("Model loaded")
    return model
    
class ShinkuTalker():

    def __init__(self, model):
        self.model = model

    async def talk(self, text):
        sr, audio = await asyncio.to_thread(self.model.infer, text=text)

        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, audio, sr, format='WAV')
        wav_buffer.seek(0)

        # pydubを使ってmp3に変換
        audio_segment = pydub.AudioSegment.from_file(wav_buffer, format="wav")
        
        mp3_buffer = io.BytesIO()
        audio_segment.export(mp3_buffer, format="mp3")
        mp3_buffer.seek(0)
        return mp3_buffer