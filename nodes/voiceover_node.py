#!/usr/bin/env python3
"""
Voiceover Node - AI voice generation using Coqui XTTS v2
Creates high-quality, emotion-controlled voiceovers with GPU acceleration

TODO: Upgrade to RAV (Real-time Audio Variational) or similar advanced voice cloning model
- RAV offers state-of-the-art voice cloning with minimal training data
- Better voice quality and more natural prosody than XTTS v2
- Research and implement once XTTS v2 is fully stable in production
"""

import sys
import os
import asyncio
import time
from pathlib import Path
import torch
from TTS.api import TTS
from moviepy.editor import AudioFileClip
import logging
import torch.serialization

# Monkey-patch torch.load to disable weights_only
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceoverNode:
    """Generates high-quality AI voiceovers using Coqui XTTS v2"""
    
    def __init__(self):
        """Initialize the Voiceover Node with XTTS v2"""
        print("🎙️ Initializing Voiceover Node with Coqui XTTS v2...")
        
        # Create temp directory for audio
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Check for GPU availability
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✅ Using device: {self.device.upper()}")
        
        # Initialize TTS
        try:
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
            # Retrieve list of bundled Coqui voices for validation/fallbacks
            self.available_speakers = list(self.tts.synthesizer.tts_model.speaker_manager.name_to_id)
            print(f"✅ Coqui XTTS v2 loaded with {len(self.available_speakers)} speakers")
        except Exception as e:
            logger.error(f"❌ Failed to load XTTS v2: {e}")
            raise
        
        # Voice cloning settings
        self.voice_samples_dir = Path("voice_samples")
        self.voice_samples_dir.mkdir(exist_ok=True)
        
        # TODO: Implement advanced voice cloning with RAV model
        # - Research and integrate RAV (Real-time Audio Variational) model
        # - RAV provides superior voice cloning quality with minimal training data
        # - Better emotion control and more natural speech synthesis
        # - Plan implementation after XTTS v2 is stable in production
        
        # Emotion control parameters
        self.emotion_options = {
            "neutral": 0.0,
            "happy": 0.7,
            "sad": -0.7,
            "angry": 0.9,
            "fearful": -0.5,
            "disgust": -0.3,
            "surprised": 0.6
        }
    
    def generate_voiceover(self, text: str, output_path: Path, 
                         voice: str = "female_professional", 
                         emotion: str = "neutral",
                         cloned_voice: str = None) -> None:
        """
        Generate voiceover with emotion control and optional voice cloning
        
        Args:
            text: Text to speak
            output_path: Output audio file path
            voice: Predefined voice profile (ignored if cloned_voice provided)
            emotion: Emotion to convey (see self.emotion_options)
            cloned_voice: Path to reference audio for voice cloning
        """
        try:
            # Set emotion parameters
            emotion_value = self.emotion_options.get(emotion, 0.0)
            
            # Generate voiceover
            if cloned_voice and os.path.exists(cloned_voice):
                # Use voice cloning
                self.tts.tts_to_file(
                    text=text,
                    file_path=str(output_path),
                    speaker_wav=str(cloned_voice),
                    emotion=emotion_value,
                    language="en"
                )
            else:
                # Use predefined voice
                self.tts.tts_to_file(
                    text=text,
                    file_path=str(output_path),
                    speaker=self._get_voice_id(voice),
                    emotion=emotion_value,
                    language="en"
                )
            
            print(f"✅ Voiceover generated: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"❌ Voiceover generation failed: {e}")
            raise
    
    def _get_voice_id(self, voice_name: str) -> str:
        """Resolve a generic voice profile to an actual XTTS speaker name.

        Accepts either a generic profile (e.g. ``female_professional``) or a
        concrete speaker name shipped with the model. If no match is found, the
        method falls back to the first available speaker to ensure synthesis
        never raises a ``KeyError``.
        """
        profile_to_speaker = {
            "female_professional": "Ana Florence",
            "male_professional": "Andrew Chipper",
            "female_friendly": "Claribel Dervla",
            "male_authoritative": "Damien Black",
        }

        # 1. Translated generic profile ➜ concrete speaker name
        speaker = profile_to_speaker.get(voice_name)
        if speaker and speaker in self.available_speakers:
            return speaker

        # 2. Caller may have passed the concrete Coqui speaker already
        if voice_name in self.available_speakers:
            return voice_name

        # 3. Fallback – use the first bundled speaker and warn
        logger.warning(
            "Voice '%s' not recognised; defaulting to '%s'.",
            voice_name,
            self.available_speakers[0],
        )
        return self.available_speakers[0]

# Example usage
if __name__ == "__main__":
    node = VoiceoverNode()
    node.generate_voiceover(
        "Building wealth starts with consistent action and financial education.",
        Path("temp/test_voiceover.wav"),
        voice="female_professional",
        emotion="happy"
    )