#!/usr/bin/env python3
"""
Perfect Dynamic Subtitles System for Faceless YouTube Videos
Creates InVideo AI quality word-by-word animated subtitles with precise timing
"""

import os
import sys
import asyncio
import edge_tts
import json
import whisper
import tempfile
from pathlib import Path
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import cv2
import math
import time
from typing import List, Dict, Tuple
import re

class PerfectSubtitleSystem:
    def __init__(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Load Whisper for word-level timing
        print("🎯 Loading Whisper for perfect timing...")
        self.whisper_model = whisper.load_model("base")
        
        # Professional font settings
        self.fonts = self._setup_fonts()
        
        # Animation presets
        self.animation_styles = {
            'modern': {
                'highlight_color': (255, 215, 0),  # Gold
                'glow_color': (255, 255, 255),     # White glow
                'shadow_color': (0, 0, 0),         # Black shadow
                'animation_type': 'pop_glow'
            },
            'professional': {
                'highlight_color': (0, 150, 255),  # Blue
                'glow_color': (200, 200, 255),     # Light blue glow
                'shadow_color': (0, 0, 50),        # Dark blue shadow
                'animation_type': 'smooth_highlight'
            },
            'energetic': {
                'highlight_color': (255, 100, 100), # Red
                'glow_color': (255, 200, 200),      # Pink glow
                'shadow_color': (50, 0, 0),         # Dark red shadow
                'animation_type': 'bounce_scale'
            }
        }
        
        print("✅ Perfect Subtitle System initialized!")
    
    def _setup_fonts(self) -> Dict:
        """Setup professional fonts for subtitles"""
        fonts = {}
        
        # Try to find system fonts
        font_paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "C:\\Windows\\Fonts\\arial.ttf",     # Windows
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                fonts['primary'] = font_path
                break
        
        # Fallback to PIL default
        if 'primary' not in fonts:
            fonts['primary'] = None
            print("⚠️ Using default font - install Liberation or DejaVu fonts for better quality")
        
        return fonts
    
    async def generate_perfect_audio(self, text: str, voice: str = "en-US-AriaNeural") -> str:
        """Generate high-quality audio with Edge TTS"""
        print(f"🎤 Generating perfect audio with voice: {voice}")
        
        audio_file = self.temp_dir / "perfect_audio.wav"
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(audio_file))
        
        print("✅ Perfect audio generated!")
        return str(audio_file)
    
    def get_word_level_timing(self, audio_file: str, text: str) -> List[Dict]:
        """Get precise word-level timing using Whisper"""
        print("⏱️ Analyzing word-level timing with Whisper...")
        
        try:
            # Transcribe with word-level timestamps
            result = self.whisper_model.transcribe(
                audio_file, 
                word_timestamps=True,
                verbose=False
            )
            
            words_timing = []
            
            for segment in result['segments']:
                if 'words' in segment:
                    for word_info in segment['words']:
                        words_timing.append({
                            'word': word_info['word'].strip(),
                            'start': word_info['start'],
                            'end': word_info['end'],
                            'confidence': word_info.get('probability', 1.0)
                        })
            
            print(f"✅ Found timing for {len(words_timing)} words")
            return words_timing
            
        except Exception as e:
            print(f"⚠️ Whisper timing failed: {e}")
            # Fallback to estimated timing
            return self._estimate_word_timing(text, audio_file)
    
    def _estimate_word_timing(self, text: str, audio_file: str) -> List[Dict]:
        """Fallback method for word timing estimation"""
        words = text.split()
        
        # Get audio duration
        try:
            audio_clip = AudioFileClip(audio_file)
            duration = audio_clip.duration
            audio_clip.close()
        except:
            duration = len(words) * 0.5  # Fallback estimate
        
        # Estimate timing
        time_per_word = duration / len(words)
        words_timing = []
        
        for i, word in enumerate(words):
            start_time = i * time_per_word
            end_time = (i + 1) * time_per_word
            
            words_timing.append({
                'word': word,
                'start': start_time,
                'end': end_time,
                'confidence': 0.8
            })
        
        return words_timing
    
    def create_subtitle_frame(self, 
                             frame_size: Tuple[int, int],
                             words_data: List[Dict], 
                             current_time: float,
                             style: str = 'modern') -> Image.Image:
        """Create a single subtitle frame with perfect styling"""
        
        width, height = frame_size
        
        # Create transparent frame
        frame = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Get current words to display (3-4 words context)
        current_words = self._get_words_for_time(words_data, current_time)
        
        if not current_words:
            return frame
        
        # Get style settings
        style_config = self.animation_styles.get(style, self.animation_styles['modern'])
        
        # Setup font
        font_size = int(height * 0.08)  # 8% of video height
        try:
            if self.fonts['primary']:
                font = ImageFont.truetype(self.fonts['primary'], font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text positioning
        text_line = " ".join([w['word'] for w in current_words])
        bbox = draw.textbbox((0, 0), text_line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position text in bottom third of frame
        x_center = width // 2
        y_position = int(height * 0.75)  # 75% down from top
        
        # Draw words with animations
        current_x = x_center - text_width // 2
        
        for word_data in current_words:
            word = word_data['word']
            word_start = word_data['start']
            word_end = word_data['end']
            
            # Calculate word animation progress
            if current_time < word_start:
                progress = 0.0
            elif current_time > word_end:
                progress = 1.0
            else:
                progress = (current_time - word_start) / (word_end - word_start)
            
            # Get word dimensions
            word_bbox = draw.textbbox((0, 0), word, font=font)
            word_width = word_bbox[2] - word_bbox[0]
            
            # Apply animation based on style
            word_color, shadow_offset, scale = self._calculate_word_animation(
                progress, style_config, current_time, word_start, word_end
            )
            
            # Draw shadow first
            shadow_x = current_x + shadow_offset[0]
            shadow_y = y_position + shadow_offset[1]
            draw.text((shadow_x, shadow_y), word, 
                     fill=style_config['shadow_color'] + (150,), font=font)
            
            # Draw main text
            draw.text((current_x, y_position), word, 
                     fill=word_color + (255,), font=font)
            
            # Add glow effect for highlighted words
            if progress > 0.1:
                self._add_glow_effect(frame, word, (current_x, y_position), 
                                    font, style_config['glow_color'])
            
            current_x += word_width + int(font_size * 0.3)  # Space between words
        
        return frame
    
    def _get_words_for_time(self, words_data: List[Dict], current_time: float) -> List[Dict]:
        """Get 3-4 words that should be visible at current time"""
        current_word_idx = None
        
        # Find the current word
        for i, word_data in enumerate(words_data):
            if word_data['start'] <= current_time <= word_data['end']:
                current_word_idx = i
                break
        
        if current_word_idx is None:
            # Find closest word
            for i, word_data in enumerate(words_data):
                if current_time < word_data['start']:
                    current_word_idx = max(0, i - 1)
                    break
            else:
                current_word_idx = len(words_data) - 1
        
        # Get context words (1 before, current, 2 after)
        start_idx = max(0, current_word_idx - 1)
        end_idx = min(len(words_data), current_word_idx + 3)
        
        return words_data[start_idx:end_idx]
    
    def _calculate_word_animation(self, progress: float, style_config: Dict, 
                                current_time: float, word_start: float, word_end: float) -> Tuple:
        """Calculate animation parameters for a word"""
        
        base_color = (255, 255, 255)  # White base
        highlight_color = style_config['highlight_color']
        
        if progress <= 0:
            # Not started - dim
            color = tuple(int(c * 0.6) for c in base_color)
            shadow_offset = (2, 2)
            scale = 1.0
        elif progress >= 1:
            # Finished - normal
            color = base_color
            shadow_offset = (1, 1)
            scale = 1.0
        else:
            # Currently speaking - animated
            animation_type = style_config['animation_type']
            
            if animation_type == 'pop_glow':
                # Pop effect with color transition
                intensity = math.sin(progress * math.pi)
                color = tuple(
                    int(base_color[i] * (1 - intensity) + highlight_color[i] * intensity)
                    for i in range(3)
                )
                shadow_offset = (int(3 * intensity), int(3 * intensity))
                scale = 1.0 + 0.1 * intensity
                
            elif animation_type == 'smooth_highlight':
                # Smooth color transition
                color = tuple(
                    int(base_color[i] * (1 - progress) + highlight_color[i] * progress)
                    for i in range(3)
                )
                shadow_offset = (2, 2)
                scale = 1.0
                
            elif animation_type == 'bounce_scale':
                # Bouncy scale effect
                bounce = math.sin(progress * math.pi * 2) * 0.1
                scale = 1.0 + bounce
                color = highlight_color if progress > 0.5 else base_color
                shadow_offset = (2, 2)
        
        return color, shadow_offset, scale
    
    def _add_glow_effect(self, frame: Image.Image, word: str, position: Tuple[int, int], 
                        font, glow_color: Tuple[int, int, int]):
        """Add glow effect to highlighted words"""
        # Create glow layer
        glow_layer = Image.new('RGBA', frame.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        
        # Draw multiple offset copies for glow
        for offset in [(i, j) for i in range(-2, 3) for j in range(-2, 3) if i != 0 or j != 0]:
            glow_x = position[0] + offset[0]
            glow_y = position[1] + offset[1]
            glow_draw.text((glow_x, glow_y), word, 
                          fill=glow_color + (80,), font=font)
        
        # Blur the glow
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Composite glow under main text
        frame.alpha_composite(glow_layer)
    
    def create_perfect_subtitle_video(self, 
                                    audio_file: str, 
                                    text: str, 
                                    video_size: Tuple[int, int] = (1080, 1920),
                                    style: str = 'modern') -> str:
        """Create complete subtitle video with perfect timing"""
        
        print("🎬 Creating perfect subtitle video...")
        
        # Get word-level timing
        words_timing = self.get_word_level_timing(audio_file, text)
        
        if not words_timing:
            raise Exception("Could not generate word timing")
        
        # Get audio duration
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        
        # Generate subtitle frames
        fps = 30
        total_frames = int(duration * fps)
        
        print(f"📽️ Generating {total_frames} subtitle frames...")
        
        subtitle_frames = []
        for frame_num in range(total_frames):
            current_time = frame_num / fps
            
            # Create subtitle frame
            subtitle_frame = self.create_subtitle_frame(
                video_size, words_timing, current_time, style
            )
            
            # Convert PIL to numpy array for MoviePy
            frame_array = np.array(subtitle_frame)
            subtitle_frames.append(frame_array)
            
            if frame_num % 100 == 0:
                print(f"   Generated {frame_num}/{total_frames} frames...")
        
        print("✅ All subtitle frames generated!")
        
        # Create video from frames
        def make_frame(t):
            frame_idx = min(int(t * fps), len(subtitle_frames) - 1)
            return subtitle_frames[frame_idx][:, :, :3]  # Remove alpha channel for video
        
        # Create subtitle video clip
        subtitle_video = VideoClip(make_frame, duration=duration)
        subtitle_video = subtitle_video.set_fps(fps)
        
        # Add audio
        final_video = subtitle_video.set_audio(audio_clip)
        
        # Save output
        output_file = self.temp_dir / f"perfect_subtitles_{int(time.time())}.mp4"
        
        print("💾 Rendering final video...")
        final_video.write_videofile(
            str(output_file),
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        # Cleanup
        audio_clip.close()
        final_video.close()
        
        print(f"🎉 Perfect subtitle video created: {output_file}")
        return str(output_file)

# Test function
async def test_perfect_subtitles():
    """Test the perfect subtitle system"""
    print("🚀 Testing Perfect Dynamic Subtitles System")
    print("=" * 60)
    
    # Test script
    test_text = """Poor people focus on saving money, while rich people focus on investing money. This single mindset shift can transform your entire financial future."""
    
    subtitle_system = PerfectSubtitleSystem()
    
    try:
        # Generate audio
        audio_file = await subtitle_system.generate_perfect_audio(test_text)
        
        # Create subtitle video
        subtitle_video = subtitle_system.create_perfect_subtitle_video(
            audio_file, test_text, style='modern'
        )
        
        print(f"\n🎉 SUCCESS! Perfect subtitle video created:")
        print(f"📁 File: {subtitle_video}")
        print(f"🎬 Ready for next feature development!")
        
        return subtitle_video
        
    except Exception as e:
        print(f"❌ Error in subtitle system: {e}")
        return None

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_perfect_subtitles())
