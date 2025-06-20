#!/usr/bin/env python3
"""
Voiceover Node - AI voice generation using Edge-TTS
Creates high-quality realistic voiceovers for videos
"""

import sys
import os
import asyncio
import edge_tts
from pathlib import Path
from moviepy.editor import AudioFileClip

class VoiceoverNode:
    """Generates high-quality AI voiceovers using Edge-TTS"""
    
    def __init__(self):
        """Initialize the Voiceover Node"""
        print("🎙️ Initializing Voiceover Node...")
        
        # Create temp directory for audio
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Professional voice settings
        self.voice_options = {
            "male_professional": "en-US-DavisNeural",
            "female_professional": "en-US-AriaNeural", 
            "male_authoritative": "en-US-BrianNeural",
            "female_friendly": "en-US-JennyNeural"
        }
        
        print("✅ Voiceover Node ready!")
    
    async def generate_voiceover(self, script: str, voice_type: str = "female_professional") -> dict:
        """
        Generate high-quality voiceover from script
        
        Args:
            script: The text to convert to speech
            voice_type: Type of voice to use
            
        Returns:
            Dictionary with audio file path and metadata
        """
        print("🎤 Generating AI voiceover with Edge-TTS...")
        
        try:
            # Select voice
            voice = self.voice_options.get(voice_type, "en-US-AriaNeural")
            
            # Create output filename
            audio_filename = "latest_generated_audio.wav"
            audio_path = self.temp_dir / audio_filename
            
            # Generate speech with optimal settings
            communicate = edge_tts.Communicate(script, voice)
            await communicate.save(str(audio_path))
            
            # Get audio duration
            audio_clip = AudioFileClip(str(audio_path))
            duration = audio_clip.duration
            audio_clip.close()
            
            print(f"✅ Voiceover generated successfully!")
            print(f"   🎵 Voice: {voice}")
            print(f"   ⏱️  Duration: {duration:.2f} seconds")
            print(f"   📁 File: {audio_path}")
            
            return {
                "success": True,
                "audio_file": str(audio_path),
                "duration": duration,
                "voice_used": voice,
                "script_length": len(script)
            }
            
        except Exception as e:
            print(f"❌ Voiceover generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_file": None,
                "duration": 0.0
            }

# Test function
async def test_voiceover():
    """Test the voiceover generation"""
    print("🧪 Testing Voiceover Node...")
    
    test_script = "Did you know that 90% of millionaires invest in real estate? Here's why property investment is the secret to building lasting wealth."
    
    voiceover = VoiceoverNode()
    result = await voiceover.generate_voiceover(test_script)
    
    if result["success"]:
        print(f"✅ Test successful! Generated {result['duration']:.1f}s audio")
    else:
        print(f"❌ Test failed: {result['error']}")

if __name__ == "__main__":
    asyncio.run(test_voiceover())