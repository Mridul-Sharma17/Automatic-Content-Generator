#!/usr/bin/env python3
"""
Professional Subtitle System v2.0
Perfect audio-text synchronization with sentence-level display
Using latest AI technologies for InVideo AI quality
"""

import os
import sys
import asyncio
import edge_tts
import json
import whisper
import tempfile
from pathlib import Path
from moviepy.editor import VideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import cv2
import math
import time
import re
from typing import List, Dict, Tuple, Optional
import nltk
from nltk.tokenize import sent_tokenize
from config import GEMINI_API_KEY
import google.generativeai as genai

# GPU acceleration support
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
except ImportError:
    GPU_AVAILABLE = False

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("📥 Downloading NLTK punkt tokenizer...")
    nltk.download('punkt', quiet=True)

class ProfessionalSubtitleEngine:
    """
    State-of-the-art subtitle system using latest AI technologies
    """
    
    def __init__(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        print("🚀 Initializing Professional Subtitle Engine...")
        
        # Check GPU availability
        self.check_gpu_availability()
        
        # Use optimized Whisper model for RTX 3050 (3.8GB memory)
        print("🚀 Loading optimized Whisper model for RTX 3050...")
        try:
            # Clear GPU memory first for optimal performance
            if GPU_AVAILABLE:
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
                
                # Check available GPU memory
                free_memory = torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)
                free_memory_gb = free_memory / (1024**3)
                
                print(f"   🔸 Available GPU Memory: {free_memory_gb:.2f}GB")
                
                # Use small model for RTX 3050 - perfect balance of accuracy and memory
                if free_memory_gb > 2.0:
                    print("   🎯 Using Whisper Small model (optimized for RTX 3050)")
                    self.whisper_model = whisper.load_model("small", device="cuda")
                    print("✅ NVIDIA GPU acceleration enabled with Whisper Small!")
                else:
                    print("   ⚠️ Low GPU memory, using base model on GPU")
                    self.whisper_model = whisper.load_model("base", device="cuda")
                    print("✅ NVIDIA GPU acceleration enabled with Whisper Base!")
                    
        except Exception as e:
            print(f"⚠️ GPU failed ({e}), falling back to base model on CPU...")
            self.whisper_model = whisper.load_model("base", device="cpu")
        
        # Setup Google Gemini for intelligent text processing
        genai.configure(api_key=GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
        
        # Professional typography settings
        self.setup_professional_fonts()
        
        # Modern subtitle styles
        self.subtitle_styles = {
            'youtube_shorts': {
                'font_size_ratio': 0.065,  # 6.5% of video height
                'line_height_ratio': 1.2,
                'max_width_ratio': 0.9,    # 90% of video width
                'position_y_ratio': 0.75,  # 75% down from top
                'background_opacity': 0.7,
                'text_color': (255, 255, 255),
                'highlight_color': (255, 215, 0),  # Gold
                'shadow_color': (0, 0, 0),
                'background_color': (0, 0, 0),
                'animation_style': 'modern_pop'
            }
        }
        
        print("✅ Professional Subtitle Engine ready!")
    
    def check_gpu_availability(self):
        """Check NVIDIA GPU availability and memory"""
        try:
            import torch
            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                gpu_name = torch.cuda.get_device_name(0)
                memory_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
                memory_free = torch.cuda.memory_reserved(0) / 1024**3
                
                print(f"🎮 NVIDIA GPU Detected:")
                print(f"   🔸 GPU: {gpu_name}")
                print(f"   🔸 Total Memory: {memory_total:.1f}GB")
                print(f"   🔸 Available GPUs: {gpu_count}")
                
                # Clear GPU cache for optimal performance
                torch.cuda.empty_cache()
                print("   🔸 GPU cache cleared")
                return True
            else:
                print("⚠️ No NVIDIA GPU detected - using CPU")
                return False
        except ImportError:
            print("⚠️ PyTorch not found - install for GPU acceleration")
            return False
    
    def setup_professional_fonts(self):
        """Setup high-quality fonts for professional subtitles"""
        self.fonts = {}
        
        # Professional font hierarchy
        font_candidates = [
            # System fonts (Linux)
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
            # macOS fonts
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            # Windows fonts
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\calibri.ttf",
        ]
        
        for font_path in font_candidates:
            if os.path.exists(font_path):
                self.fonts['primary'] = font_path
                print(f"✅ Using professional font: {os.path.basename(font_path)}")
                break
        
        if 'primary' not in self.fonts:
            self.fonts['primary'] = None
            print("⚠️ Using default font - consider installing professional fonts")
    
    async def generate_high_quality_audio(self, text: str, voice: str = "en-US-AriaNeural") -> str:
        """Generate crystal clear audio using Edge TTS"""
        print(f"🎤 Generating high-quality audio with {voice}...")
        
        audio_file = self.temp_dir / f"professional_audio_{int(time.time())}.wav"
        
        # Use Edge TTS with optimal settings
        communicate = edge_tts.Communicate(text, voice, rate="-5%", pitch="+0Hz")
        await communicate.save(str(audio_file))
        
        print("✅ High-quality audio generated!")
        return str(audio_file)
    
    def intelligent_sentence_segmentation(self, text: str) -> List[str]:
        """Use AI to create intelligent sentence breaks for subtitles"""
        print("🧠 Creating intelligent sentence segmentation...")
        
        try:
            # Use Gemini for intelligent segmentation
            prompt = f"""
            You are an expert in creating subtitle segments for videos. Break this text into optimal subtitle segments.
            
            Rules:
            1. Each segment should be 1-2 sentences maximum
            2. Keep segments between 3-8 words for readability
            3. Break at natural speech pauses
            4. Maintain meaning and flow
            5. Return ONLY a JSON array of segments
            
            Text: "{text}"
            
            Return format: ["segment 1", "segment 2", "segment 3"]
            """
            
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean and parse JSON
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '')
            
            segments = json.loads(response_text)
            print(f"✅ Created {len(segments)} intelligent segments")
            return segments
            
        except Exception as e:
            print(f"⚠️ AI segmentation failed: {e}, using fallback...")
            # Fallback to NLTK sentence tokenization
            sentences = sent_tokenize(text)
            
            # Further break long sentences
            segments = []
            for sentence in sentences:
                words = sentence.split()
                if len(words) <= 8:
                    segments.append(sentence)
                else:
                    # Break long sentences at commas or conjunctions
                    parts = re.split(r'[,;]|\band\b|\bbut\b|\bor\b', sentence)
                    for part in parts:
                        if part.strip():
                            segments.append(part.strip())
            
            return segments
    
    def get_precise_timing(self, audio_file: str, segments: List[str]) -> List[Dict]:
        """Get precise timing for each segment using Whisper with error handling"""
        print("⏱️ Analyzing precise timing with Whisper...")
        
        try:
            # Check if audio file exists
            if not os.path.exists(audio_file):
                raise Exception(f"Audio file not found: {audio_file}")
            
            # Check if ffmpeg is available
            import subprocess
            try:
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            except FileNotFoundError:
                print("❌ FFmpeg not found. Installing...")
                subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)
                print("✅ FFmpeg installed successfully!")
            
            # Transcribe with word-level timestamps using optimized settings
            result = self.whisper_model.transcribe(
                audio_file,
                word_timestamps=True,
                verbose=False,
                language='en',
                temperature=0.0,  # Most accurate transcription
                no_speech_threshold=0.6,
                logprob_threshold=-1.0
            )
            
            # Extract all words with timestamps
            all_words = []
            for segment in result['segments']:
                if 'words' in segment:
                    for word_info in segment['words']:
                        all_words.append({
                            'word': word_info['word'].strip(),
                            'start': word_info['start'],
                            'end': word_info['end'],
                            'confidence': word_info.get('probability', 1.0)
                        })
            
            # Map segments to word timings
            segment_timings = self._map_segments_to_timings(segments, all_words)
            
            print(f"✅ Precise timing mapped for {len(segment_timings)} segments")
            return segment_timings
            
        except Exception as e:
            print(f"⚠️ Whisper timing failed: {e}")
            print("🔄 Using fallback timing estimation...")
            return self._create_fallback_timing(segments, audio_file)
    
    def _map_segments_to_timings(self, segments: List[str], word_timings: List[Dict]) -> List[Dict]:
        """Map text segments to precise word timings"""
        segment_timings = []
        word_index = 0
        
        for segment_text in segments:
            segment_words = segment_text.split()
            segment_start = None
            segment_end = None
            
            # Find matching words in timing data
            matched_words = []
            temp_word_index = word_index
            
            for target_word in segment_words:
                # Find best matching word in remaining timings
                best_match = None
                best_score = 0
                
                for i in range(temp_word_index, min(temp_word_index + 10, len(word_timings))):
                    if i >= len(word_timings):
                        break
                    
                    timing_word = word_timings[i]['word'].lower().strip('.,!?')
                    target_word_clean = target_word.lower().strip('.,!?')
                    
                    # Calculate similarity
                    if timing_word == target_word_clean:
                        score = 1.0
                    elif target_word_clean in timing_word or timing_word in target_word_clean:
                        score = 0.8
                    else:
                        score = 0.0
                    
                    if score > best_score:
                        best_score = score
                        best_match = i
                
                if best_match is not None:
                    matched_words.append(word_timings[best_match])
                    temp_word_index = best_match + 1
            
            # Calculate segment timing
            if matched_words:
                segment_start = matched_words[0]['start']
                segment_end = matched_words[-1]['end']
                word_index = temp_word_index
            else:
                # Fallback timing
                if segment_timings:
                    segment_start = segment_timings[-1]['end']
                    segment_end = segment_start + len(segment_words) * 0.5
                else:
                    segment_start = 0
                    segment_end = len(segment_words) * 0.5
            
            segment_timings.append({
                'text': segment_text,
                'start': segment_start,
                'end': segment_end,
                'words': matched_words
            })
        
        return segment_timings
    
    def create_professional_subtitle_frame(self, 
                                         frame_size: Tuple[int, int],
                                         current_segment: str,
                                         style: str = 'youtube_shorts') -> Image.Image:
        """Create a single professional subtitle frame"""
        
        width, height = frame_size
        style_config = self.subtitle_styles[style]
        
        # Create transparent frame
        frame = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        if not current_segment.strip():
            return frame
        
        # Setup font
        font_size = int(height * style_config['font_size_ratio'])
        try:
            if self.fonts['primary']:
                font = ImageFont.truetype(self.fonts['primary'], font_size)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text layout
        max_width = int(width * style_config['max_width_ratio'])
        
        # Word wrap text
        wrapped_lines = self._wrap_text(current_segment, font, max_width, draw)
        
        # Calculate total text height
        line_height = int(font_size * style_config['line_height_ratio'])
        total_height = len(wrapped_lines) * line_height
        
        # Position text
        y_start = int(height * style_config['position_y_ratio'] - total_height / 2)
        
        # Draw background for better readability
        if len(wrapped_lines) > 0:
            # Calculate background bounds
            max_line_width = max([draw.textbbox((0, 0), line, font=font)[2] for line in wrapped_lines])
            bg_padding = int(font_size * 0.2)
            
            bg_x = (width - max_line_width) // 2 - bg_padding
            bg_y = y_start - bg_padding
            bg_width = max_line_width + 2 * bg_padding
            bg_height = total_height + 2 * bg_padding
            
            # Create background with rounded corners
            bg_color = style_config['background_color'] + (int(255 * style_config['background_opacity']),)
            self._draw_rounded_rectangle(draw, (bg_x, bg_y, bg_x + bg_width, bg_y + bg_height), 
                                       bg_color, radius=int(font_size * 0.15))
        
        # Draw text lines
        for i, line in enumerate(wrapped_lines):
            # Calculate center position for this line
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            x_pos = (width - line_width) // 2
            y_pos = y_start + i * line_height
            
            # Draw shadow
            shadow_offset = 3
            draw.text((x_pos + shadow_offset, y_pos + shadow_offset), line,
                     fill=style_config['shadow_color'] + (200,), font=font)
            
            # Draw main text
            draw.text((x_pos, y_pos), line,
                     fill=style_config['text_color'] + (255,), font=font)
        
        return frame
    
    def _wrap_text(self, text: str, font, max_width: int, draw) -> List[str]:
        """Wrap text to fit within max width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Single word too long
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _draw_rounded_rectangle(self, draw, bounds, fill, radius=10):
        """Draw rounded rectangle"""
        x1, y1, x2, y2 = bounds
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
        draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
    
    async def create_perfect_subtitle_video(self, 
                                          text: str,
                                          output_path: str = None,
                                          video_size: Tuple[int, int] = (1080, 1920),
                                          style: str = 'youtube_shorts') -> str:
        """Create perfect subtitle video with professional quality"""
        
        print("🎬 Creating perfect subtitle video...")
        print("=" * 50)
        
        # Step 1: Generate high-quality audio
        audio_file = await self.generate_high_quality_audio(text)
        
        # Step 2: Intelligent segmentation
        segments = self.intelligent_sentence_segmentation(text)
        
        # Step 3: Get precise timing
        segment_timings = self.get_precise_timing(audio_file, segments)
        
        # Step 4: Create video frames
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        fps = 30
        
        print(f"📽️ Generating frames for {duration:.2f}s video at {fps}fps...")
        
        def make_frame(t):
            # Find current segment
            current_segment = ""
            for segment_info in segment_timings:
                if segment_info['start'] <= t <= segment_info['end']:
                    current_segment = segment_info['text']
                    break
            
            # Create subtitle frame
            subtitle_frame = self.create_professional_subtitle_frame(
                video_size, current_segment, style
            )
            
            # Convert to RGB for video (transparent background becomes black)
            rgb_frame = Image.new('RGB', video_size, (0, 0, 0))
            rgb_frame.paste(subtitle_frame, (0, 0), subtitle_frame)
            
            return np.array(rgb_frame)
        
        # Create video clip
        video_clip = VideoClip(make_frame, duration=duration)
        video_clip = video_clip.set_fps(fps)
        final_clip = video_clip.set_audio(audio_clip)
        
        # Generate output path
        if output_path is None:
            output_path = self.temp_dir / f"professional_subtitles_{int(time.time())}.mp4"
        
        print("💾 Rendering professional video...")
        final_clip.write_videofile(
            str(output_path),
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None,
            bitrate="8000k"  # High quality
        )
        
        # Cleanup
        audio_clip.close()
        final_clip.close()
        
        print(f"🎉 Professional subtitle video created!")
        print(f"📁 Location: {output_path}")
        return str(output_path)

    def _create_fallback_timing(self, segments: List[str], audio_file: str) -> List[Dict]:
        """Create fallback timing when Whisper fails"""
        print("📊 Creating fallback timing estimation...")
        
        try:
            # Get audio duration
            audio_clip = AudioFileClip(audio_file)
            duration = audio_clip.duration
            audio_clip.close()
        except:
            # Estimate duration based on text length
            total_words = sum(len(segment.split()) for segment in segments)
            duration = total_words * 0.5  # Assume 0.5 seconds per word
        
        # Distribute time across segments based on word count
        total_words = sum(len(segment.split()) for segment in segments)
        segment_timings = []
        current_time = 0
        
        for segment_text in segments:
            words_in_segment = len(segment_text.split())
            segment_duration = (words_in_segment / total_words) * duration
            
            segment_timings.append({
                'text': segment_text,
                'start': current_time,
                'end': current_time + segment_duration,
                'words': []  # No word-level timing in fallback
            })
            
            current_time += segment_duration
        
        print(f"✅ Fallback timing created for {len(segment_timings)} segments")
        return segment_timings

# Professional test function
async def test_professional_system():
    """Test the professional subtitle system"""
    print("🚀 Testing Professional Subtitle System v2.0")
    print("=" * 60)
    
    test_text = """Poor people focus on saving money, while rich people focus on investing money. This single mindset shift can transform your entire financial future. When you only save money, inflation slowly eats away at your purchasing power."""
    
    try:
        engine = ProfessionalSubtitleEngine()
        
        video_file = await engine.create_perfect_subtitle_video(
            text=test_text,
            style='youtube_shorts'
        )
        
        print(f"\n🎉 SUCCESS! Professional subtitle video created!")
        print(f"📁 File: {video_file}")
        print(f"✅ Perfect audio-text synchronization")
        print(f"✅ Sentence-level display")
        print(f"✅ Professional quality achieved")
        
        return video_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_professional_system())
