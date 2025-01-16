from RealtimeSTT import AudioToTextRecorder
from typing import Callable, Optional
import logging

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
        # TODO: Implement TTS using elevenlabs or pyttsx3
