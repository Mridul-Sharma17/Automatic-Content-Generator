#!/usr/bin/env python3
"""
Professional Subtitle Node - Creates synchronized subtitles with perfect timing
Uses Whisper for precise audio analysis and generates professional subtitle overlays
"""

import sys
import os
import asyncio
import whisper
import json
from pathlib import Path
from typing import List, Dict, Any
from moviepy.editor import AudioFileClip
import nltk
from nltk.tokenize import sent_tokenize

# Download required NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("📥 Downloading NLTK punkt tokenizer...")
    nltk.download('punkt', quiet=True)

class ProfessionalSubtitleNode:
    """Generates professional subtitles with precise timing"""
    
    def __init__(self):
        """Initialize the Professional Subtitle Node"""
        print("📝 Initializing Professional Subtitle Node...")
        
        # Load optimized Whisper model (force CPU only)
        try:
            print("🎯 Loading Whisper model for subtitle timing (CPU only)...")
            # Force CPU usage for consistency
            self.whisper_model = whisper.load_model("base", device="cpu")
            print("✅ Whisper model loaded successfully on CPU!")
        except Exception as e:
            print(f"⚠️ Whisper loading failed: {e}")
            self.whisper_model = None
        
        print("✅ Professional Subtitle Node ready!")
    
    async def generate_subtitles(self, audio_file: str, script: str) -> Dict[str, Any]:
        """
        Generate professional subtitles with precise timing
        
        Args:
            audio_file: Path to the audio file
            script: Original script text
            
        Returns:
            Dictionary with subtitle segments and timing data
        """
        print("⏱️ Generating precise subtitle timing...")
        
        try:
            # Get precise timing using Whisper
            if self.whisper_model and os.path.exists(audio_file):
                segments = await self._get_whisper_timing(audio_file, script)
            else:
                segments = self._create_fallback_timing(script, audio_file)
            
            print(f"✅ Generated {len(segments)} subtitle segments")
            
            return {
                "success": True,
                "segments": segments,
                "total_segments": len(segments)
            }
            
        except Exception as e:
            print(f"❌ Subtitle generation failed: {e}")
            # Create basic fallback timing
            segments = self._create_basic_fallback(script)
            return {
                "success": False,
                "segments": segments,
                "error": str(e)
            }
    
    async def _get_whisper_timing(self, audio_file: str, script: str) -> List[Dict[str, Any]]:
        """Get precise timing using Whisper transcription"""
        
        try:
            print("🎤 Analyzing audio with Whisper for precise timing...")
            
            # Transcribe with word-level timestamps (CPU only)
            result = await asyncio.to_thread(
                self.whisper_model.transcribe,
                audio_file,
                word_timestamps=True,
                verbose=False,
                language='en'  # Force English for consistency
                # Remove device parameter - it's already set when loading the model
            )
            
            # Extract segments with word-level timing
            segments = []
            for segment in result.get("segments", []):
                segment_data = {
                    "text": segment["text"].strip(),
                    "start": segment["start"],
                    "end": segment["end"],
                    "words": []
                }
                
                # Add word-level timing if available
                if "words" in segment:
                    for word in segment["words"]:
                        word_data = {
                            "word": word["word"].strip(),
                            "start": word["start"],
                            "end": word["end"]
                        }
                        segment_data["words"].append(word_data)
                
                segments.append(segment_data)
            
            print(f"✅ Whisper analysis complete - {len(segments)} segments")
            return segments
            
        except Exception as e:
            print(f"⚠️ Whisper timing failed: {e}")
            return self._create_fallback_timing(script, audio_file)
    
    def _create_fallback_timing(self, script: str, audio_file: str) -> List[Dict[str, Any]]:
        """Create fallback timing when Whisper fails"""
        
        try:
            # Get audio duration
            audio_clip = AudioFileClip(audio_file)
            total_duration = audio_clip.duration
            audio_clip.close()
        except:
            # Estimate duration (150 words per minute)
            word_count = len(script.split())
            total_duration = (word_count / 150) * 60
        
        # Use NLTK for intelligent sentence segmentation
        try:
            sentences = sent_tokenize(script)
        except:
            # Fallback to basic splitting if NLTK fails
            sentences = script.replace('!', '.').replace('?', '.').split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
        
        # Distribute time across sentences
        segments = []
        current_time = 0.0
        
        for i, sentence in enumerate(sentences):
            if not sentence:
                continue
                
            # Estimate duration based on word count
            words = sentence.split()
            sentence_duration = max(2.0, (len(words) / 150) * 60)  # Min 2 seconds
            
            # Don't exceed total duration
            if current_time + sentence_duration > total_duration:
                sentence_duration = total_duration - current_time
            
            segment_data = {
                "text": sentence.strip(),
                "start": current_time,
                "end": current_time + sentence_duration,
                "words": []  # No word-level timing in fallback
            }
            
            segments.append(segment_data)
            current_time += sentence_duration
            
            if current_time >= total_duration:
                break
        
        print(f"✅ Fallback timing created - {len(segments)} segments")
        return segments
    
    def _create_basic_fallback(self, script: str) -> List[Dict[str, Any]]:
        """Create very basic timing as last resort"""
        
        # Use NLTK for sentence splitting if available
        try:
            sentences = sent_tokenize(script)
        except:
            # Fallback to basic splitting
            sentences = script.replace('!', '.').replace('?', '.').split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
        
        segments = []
        current_time = 0.0
        
        for sentence in sentences:
            duration = max(3.0, len(sentence.split()) * 0.5)  # 0.5 seconds per word, min 3s
            
            segments.append({
                "text": sentence.strip(),
                "start": current_time,
                "end": current_time + duration,
                "words": []
            })
            
            current_time += duration
        
        return segments

# Test function
async def test_subtitle_node():
    """Test the subtitle generation"""
    print("🧪 Testing Professional Subtitle Node...")
    
    # This would normally use a real audio file
    test_script = "Did you know that 90% of millionaires invest in real estate? This is a key wealth building strategy."
    
    subtitle_node = ProfessionalSubtitleNode()
    result = await subtitle_node.generate_subtitles("dummy_audio.wav", test_script)
    
    if result["success"]:
        print(f"✅ Test successful! Generated {result['total_segments']} segments")
    else:
        print(f"⚠️ Test completed with fallback - {len(result['segments'])} segments")

if __name__ == "__main__":
    asyncio.run(test_subtitle_node())