import os
import time
import whisper
import pyaudio
import wave
import pyttsx3
import logging
from typing import Optional
import numpy as np
from config import Config

class Speech:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger('FRIDAY.Speech')
        
        # Initialize whisper model
        self.model = whisper.load_model(self.config.WHISPER_MODEL)
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', self.config.VOICE_ID)
        
        # Adjust voice properties for better clarity
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Audio recording settings
        self.chunk = self.config.CHUNK_SIZE
        self.format = pyaudio.paFloat32
        self.channels = self.config.CHANNELS
        self.rate = self.config.SAMPLE_RATE
        self.record_seconds = self.config.RECORD_SECONDS
        
        self.audio = pyaudio.PyAudio()
        
    def listen_and_transcribe(self) -> Optional[str]:
        """Record audio and transcribe it to text"""
        try:
            # Open audio stream
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.logger.info("Listening...")
            frames = []
            
            # Record audio
            for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
                try:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    frames.append(np.frombuffer(data, dtype=np.float32))
                except Exception as e:
                    self.logger.debug(f"Non-critical error during recording: {e}")
                    continue
                
            self.logger.info("Finished recording")
            
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            
            if not frames:
                return None
            
            # Convert audio to numpy array
            audio_data = np.concatenate(frames, axis=0)
            
            # Transcribe using whisper
            result = self.model.transcribe(audio_data)
            transcribed_text = result["text"].strip()
            
            if transcribed_text:
                self.logger.debug(f"Transcribed text: {transcribed_text}")
                
            return transcribed_text if transcribed_text else None
            
        except Exception as e:
            self.logger.error(f"Error in listen_and_transcribe: {e}")
            return None
            
    def speak(self, text: str) -> None:
        """Convert text to speech"""
        try:
            self.logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Error in speak: {e}")
            
    def __del__(self):
        """Cleanup resources"""
        try:
            self.audio.terminate()
        except:
            pass