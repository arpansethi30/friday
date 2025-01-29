import whisper
import pyaudio
import numpy as np
import pyttsx3
import sys
import time
from typing import Optional
import logging
from config import Config

class Speech:
    def __init__(self, config: Config):
        self.config = config
        self.setup_logging()
        self.model = whisper.load_model(config.WHISPER_MODEL)
        self.engine = self._setup_tts_engine()
        self.audio = pyaudio.PyAudio()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=self.config.LOG_FILE,
            level=self.config.LOG_LEVEL,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('Speech')
        
    def _setup_tts_engine(self) -> pyttsx3.Engine:
        engine = pyttsx3.init()
        
        if sys.platform == 'darwin':
            engine.setProperty('voice', self.config.VOICE_ID)
        else:
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
            
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 0.9)
        return engine
        
    def listen_and_transcribe(self, timeout: Optional[int] = None) -> str:
        try:
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.config.CHANNELS,
                rate=self.config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=self.config.CHUNK_SIZE
            )
            
            frames = []
            silence_threshold = 500
            is_speaking = False
            silence_frames = 0
            
            start_time = time.time()
            while True:
                if timeout and (time.time() - start_time) > timeout:
                    break
                    
                data = stream.read(self.config.CHUNK_SIZE, exception_on_overflow=False)
                frames.append(data)
                
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.abs(audio_data).mean()
                
                if volume > silence_threshold:
                    is_speaking = True
                    silence_frames = 0
                elif is_speaking:
                    silence_frames += 1
                    if silence_frames > 30:
                        break
                        
            stream.stop_stream()
            stream.close()
            
            if not frames:
                return ""
                
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
            float_data = audio_data.astype(np.float32) / 32768.0
            
            result = self.model.transcribe(float_data)
            transcribed_text = result["text"].strip()
            
            self.logger.debug(f"Transcribed: {transcribed_text}")
            return transcribed_text
            
        except Exception as e:
            self.logger.error(f"Error in listen_and_transcribe: {e}")
            return ""
            
    def speak(self, text: str, interrupt: bool = False):
        try:
            if interrupt and self.engine._inLoop:
                self.engine.stop()
                
            text = self._add_speech_markers(text)
            
            print(f"FRIDAY: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            self.logger.error(f"Error in speak: {e}")
            
    def _add_speech_markers(self, text: str) -> str:
        text = text.replace('. ', '... ')
        text = text.replace('? ', '... ')
        text = text.replace('! ', '... ')
        
        emphasis_words = ['urgent', 'important', 'warning', 'error']
        for word in emphasis_words:
            text = text.replace(f' {word} ', f' *{word}* ')
            
        return text
        
    def __del__(self):
        if hasattr(self, 'audio'):
            self.audio.terminate()