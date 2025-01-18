import logging
import os
from typing import Callable, Optional

import pyttsx3
from elevenlabs import generate, set_api_key
from RealtimeSTT import AudioToTextRecorder


class TarotVoice:
    def __init__(self):
        self.logger = logging.getLogger("tarot_voice")
        self.recorder = AudioToTextRecorder(
            spinner=False,
            post_speech_silence_duration=1.5,
            compute_type="float32",
            model="small.en",
            beam_size=8,
            batch_size=25,
            language="en",
            print_transcription_time=True
        )
        self.tts_engine = pyttsx3.init()
        self.use_elevenlabs = False
        
        # Configure elevenlabs if API key is available
        if os.getenv("ELEVENLABS_API_KEY"):
            set_api_key(os.getenv("ELEVENLABS_API_KEY"))
            self.use_elevenlabs = True

    def start_listening(self, callback: Callable[[str], None]) -> None:
        """Start voice listening with callback for processing"""
        self.logger.info("Starting voice listener")
        self.recorder.text(callback)

    def stop_listening(self) -> None:
        """Stop voice listening"""
        self.logger.info("Stopping voice listener")
        self.recorder.stop()

    def speak(self, text: str) -> None:
        """Speak text using TTS"""
        self.logger.info(f"Speaking: {text}")
        
        if self.use_elevenlabs:
            try:
                audio = generate(
                    text=text,
                    voice="Rachel",
                    model="eleven_multilingual_v2"
                )
                play(audio)
            except Exception as e:
                self.logger.warning(f"ElevenLabs failed: {str(e)}")
                self._fallback_tts(text)
        else:
            self._fallback_tts(text)

    def _fallback_tts(self, text: str) -> None:
        """Fallback to pyttsx3 if ElevenLabs fails or isn't configured"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
