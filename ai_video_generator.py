#!/usr/bin/env python3
"""
Professional AI Video Generator for Wealthier Everyday YouTube Channel
InVideo AI Quality - Generates perfectly synced faceless AI videos completely free
Uses Google Gemini for AI intelligence and creates professional quality videos
"""

import os
import sys
import asyncio
import edge_tts
import requests
import json
from pathlib import Path
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import cv2
import tempfile
import random
import re
import math
from urllib.parse import quote
import time
from typing import List, Dict, Tuple

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Gemini not available, using fallback analysis")

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper not available, using estimated timing")

class ProfessionalAIVideoGenerator:
    def __init__(self, output_dir="output", gemini_api_key=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Video settings for YouTube Shorts (InVideo AI quality)
        self.width = 1080
        self.height = 1920  # 9:16 aspect ratio
        self.fps = 30
        
        # Professional color schemes for different moods
        self.color_schemes = {
            'wealth': {
                'primary': '#2E8B57',    # Sea Green
                'secondary': '#FFD700',  # Gold
                'accent': '#FF6B35',     # Orange Red
                'text': '#FFFFFF',       # White
                'bg_start': '#1A1A1A',   # Dark
                'bg_end': '#2E8B57'      # Green
            },
            'business': {
                'primary': '#1E3A8A',    # Deep Blue
                'secondary': '#3B82F6',  # Blue
                'accent': '#10B981',     # Emerald
                'text': '#FFFFFF',
                'bg_start': '#0F172A',   # Slate
                'bg_end': '#1E3A8A'
            },
            'motivation': {
                'primary': '#DC2626',    # Red
                'secondary': '#F59E0B',  # Amber
                'accent': '#EF4444',     # Red
                'text': '#FFFFFF',
                'bg_start': '#1F2937',   # Gray
                'bg_end': '#DC2626'
            }
        }
        
        # Initialize Google Gemini if API key provided
        self.gemini_enabled = False
        if gemini_api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                self.gemini_enabled = True
                print("🤖 Google Gemini AI initialized!")
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
        
        # Load Whisper for precise audio timing
        if WHISPER_AVAILABLE:
            try:
                print("🎤 Loading Whisper for audio timing...")
                self.whisper_model = whisper.load_model("base")
                print("✅ Whisper loaded successfully!")
            except Exception as e:
                print(f"⚠️ Whisper loading failed: {e}")
                self.whisper_model = None
        else:
            self.whisper_model = None
        
        print("🎬 Professional AI Video Generator initialized!")
        print("🎯 InVideo AI quality video generation ready!")
    
    async def analyze_script_with_gemini(self, script: str) -> Dict:
        """Use Google Gemini to analyze script and suggest visuals"""
        if not self.gemini_enabled:
            return self.fallback_script_analysis(script)
        
        try:
            prompt = f"""
            Analyze this YouTube Shorts script about wealth/finance and provide:
            1. Main theme/mood (wealth, business, motivation, etc.)
            2. Key segments (break into 5-8 parts for a 60-second video)
            3. Visual descriptions for each segment
            4. Emotional tone for each segment
            
            Script: {script}
            
            Return as JSON format:
            {{
                "theme": "wealth",
                "segments": [
                    {{
                        "text": "segment text",
                        "visual_description": "description of what visuals should show",
                        "mood": "serious/exciting/motivational",
                        "duration_weight": 1.0
                    }}
                ]
            }}
            """
            
            response = self.gemini_model.generate_content(prompt)
            result = json.loads(response.text.strip())
            print("🤖 Gemini script analysis complete!")
            return result
            
        except Exception as e:
            print(f"⚠️ Gemini analysis failed: {e}")
            return self.fallback_script_analysis(script)
    
    def fallback_script_analysis(self, script: str) -> Dict:
        """Fallback script analysis without Gemini"""
        print("📋 Using fallback script analysis...")
        
        # Split script into meaningful segments
        lines = [line.strip() for line in script.split('\n') if line.strip()]
        segments = []
        
        current_segment = []
        for line in lines:
            if not line:
                if current_segment:
                    segments.append(' '.join(current_segment))
                    current_segment = []
            else:
                current_segment.append(line)
        
        if current_segment:
            segments.append(' '.join(current_segment))
        
        # Filter out very short segments
        filtered_segments = []
        for segment in segments:
            if len(segment.split()) >= 3:  # At least 3 words
                visual_desc = self.generate_visual_description(segment)
                filtered_segments.append({
                    "text": segment,
                    "visual_description": visual_desc,
                    "mood": "motivational",
                    "duration_weight": 1.0
                })
        
        return {
            "theme": "wealth",
            "segments": filtered_segments
        }
    
    def generate_visual_description(self, text: str) -> str:
        """Generate visual descriptions based on text content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['money', 'salary', 'earn', 'income']):
            return "professional financial concept with money and income symbols"
        elif any(word in text_lower for word in ['invest', 'investment']):
            return "investment and growth charts with upward trending graphics"
        elif any(word in text_lower for word in ['habit', 'habits']):
            return "lifestyle and daily habits visualization"
        elif any(word in text_lower for word in ['spend', 'shopping']):
            return "spending and consumer behavior graphics"
        elif any(word in text_lower for word in ['save', 'saving']):
            return "savings and financial planning visuals"
        else:
            return "modern financial success and wealth building concept"
    
    def create_professional_backgrounds(self, count: int, theme: str = "wealth") -> List[str]:
        """Create professional gradient backgrounds"""
        print("🎨 Creating professional gradient backgrounds...")
        
        images = []
        # Get color scheme based on theme
        colors = self.color_schemes.get(theme, self.color_schemes['wealth'])
        
        gradients = [
            (colors['bg_start'], colors['primary'], colors['secondary']),
            (colors['primary'], colors['bg_end'], colors['accent']),
            ('#1a1a2e', '#16213e', '#0f3460'),
            ('#2d1b69', '#11998e', '#38ef7d'),
            ('#2c3e50', '#3498db', '#9b59b6'),
        ]
        
        for i in range(count):
            gradient_colors = gradients[i % len(gradients)]
            img = self.create_advanced_gradient(gradient_colors, i)
            images.append(img)
        
        return images
    
    def create_advanced_gradient(self, colors: Tuple, index: int) -> str:
        """Create advanced gradient with professional effects"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        # Create multi-color gradient
        for y in range(self.height):
            if y < self.height * 0.4:
                # Top section
                ratio = y / (self.height * 0.4)
                r1, g1, b1 = tuple(int(colors[0][1:][i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(colors[1][1:][i:i+2], 16) for i in (0, 2, 4))
            elif y < self.height * 0.7:
                # Middle section
                ratio = (y - self.height * 0.4) / (self.height * 0.3)
                r1, g1, b1 = tuple(int(colors[1][1:][i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(colors[2][1:][i:i+2], 16) for i in (0, 2, 4))
            else:
                # Bottom section
                ratio = (y - self.height * 0.7) / (self.height * 0.3)
                r1, g1, b1 = tuple(int(colors[2][1:][i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(colors[0][1:][i:i+2], 16) for i in (0, 2, 4))
            
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Add subtle geometric patterns
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Add diagonal lines for texture
        for x in range(0, self.width + 200, 150):
            overlay_draw.line([(x, 0), (x - 300, self.height)], 
                            fill=(255, 255, 255, 8), width=2)
        
        # Add circles for visual interest
        for i in range(3):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            radius = random.randint(100, 300)
            overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                               outline=(255, 255, 255, 20), width=3)
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        img_path = self.temp_dir / f"gradient_bg_{index}.jpg"
        img.save(str(img_path), quality=95)
        
        return str(img_path)
    
    async def get_precise_audio_timing(self, audio_path: str, script: str) -> List[Dict]:
        """Get precise word-level timing using Whisper or fallback"""
        print("🎤 Analyzing audio for precise word timing...")
        
        if self.whisper_model:
            try:
                # Use Whisper for precise timing
                result = self.whisper_model.transcribe(audio_path, word_timestamps=True)
                
                word_timings = []
                for segment in result.get("segments", []):
                    for word_info in segment.get("words", []):
                        word_timings.append({
                            "word": word_info["word"].strip(),
                            "start": word_info["start"],
                            "end": word_info["end"],
                            "confidence": 1.0
                        })
                
                print(f"✅ Extracted timing for {len(word_timings)} words")
                return word_timings
                
            except Exception as e:
                print(f"⚠️ Whisper timing failed: {e}")
        
        # Fallback to estimated timing
        return self.estimate_word_timing(script, AudioFileClip(audio_path).duration)
    
    def estimate_word_timing(self, script: str, total_duration: float) -> List[Dict]:
        """Fallback method to estimate word timing"""
        print("📊 Using estimated word timing...")
        
        # Clean script and split into words
        clean_script = re.sub(r'[*_#@\n]', ' ', script)
        words = [w.strip() for w in clean_script.split() if w.strip()]
        
        # Calculate timing
        words_per_second = len(words) / total_duration
        
        word_timings = []
        current_time = 0
        
        for word in words:
            # Adjust duration based on word length
            base_duration = 1.0 / words_per_second
            word_duration = base_duration * (0.8 + 0.4 * len(word) / 10)
            
            word_timings.append({
                "word": word,
                "start": current_time,
                "end": current_time + word_duration,
                "confidence": 1.0
            })
            
            current_time += word_duration
        
        print(f"✅ Estimated timing for {len(word_timings)} words")
        return word_timings
    
    def create_dynamic_subtitle_clip(self, word_timings: List[Dict], total_duration: float) -> VideoClip:
        """Create dynamic animated subtitles that appear word by word"""
        print("📝 Creating dynamic animated subtitles...")
        
        def make_frame(t):
            # Create transparent frame
            frame = np.zeros((self.height, self.width, 4), dtype=np.uint8)
            img = Image.fromarray(frame, 'RGBA')
            draw = ImageDraw.Draw(img)
            
            # Load font
            try:
                font_size = 72
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
                font_size = 40
            
            # Find words to display (show last 4-6 words)
            display_words = []
            highlight_word = None
            
            for word_info in word_timings:
                if word_info["start"] <= t <= word_info["end"] + 0.5:
                    if word_info["start"] <= t <= word_info["end"]:
                        highlight_word = len(display_words)
                    display_words.append(word_info["word"])
            
            # Keep only last 6 words maximum
            if len(display_words) > 6:
                if highlight_word is not None:
                    highlight_word = max(0, highlight_word - (len(display_words) - 6))
                display_words = display_words[-6:]
            
            if display_words:
                # Create text lines (max 2 lines)
                text_lines = []
                current_line = []
                
                for word in display_words:
                    test_line = ' '.join(current_line + [word])
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    if bbox[2] - bbox[0] > self.width - 100 and current_line:
                        text_lines.append(current_line)
                        current_line = [word]
                    else:
                        current_line.append(word)
                
                if current_line:
                    text_lines.append(current_line)
                
                # Limit to 2 lines
                if len(text_lines) > 2:
                    text_lines = text_lines[-2:]
                
                # Calculate position
                total_height = len(text_lines) * (font_size + 10)
                start_y = self.height - 350  # Bottom area
                
                # Draw background
                max_width = 0
                for line in text_lines:
                    line_text = ' '.join(line)
                    bbox = draw.textbbox((0, 0), line_text, font=font)
                    max_width = max(max_width, bbox[2] - bbox[0])
                
                # Background rectangle
                padding = 25
                rect_x1 = (self.width - max_width) // 2 - padding
                rect_y1 = start_y - padding
                rect_x2 = (self.width + max_width) // 2 + padding
                rect_y2 = start_y + total_height + padding
                
                draw.rounded_rectangle([rect_x1, rect_y1, rect_x2, rect_y2], 
                                     radius=20, fill=(0, 0, 0, 200))
                
                # Draw text
                word_index = 0
                for line_idx, line in enumerate(text_lines):
                    line_text = ' '.join(line)
                    bbox = draw.textbbox((0, 0), line_text, font=font)
                    line_width = bbox[2] - bbox[0]
                    
                    x = (self.width - line_width) // 2
                    y = start_y + line_idx * (font_size + 10)
                    
                    # Draw each word
                    current_x = x
                    for word in line:
                        word_bbox = draw.textbbox((0, 0), word + " ", font=font)
                        word_width = word_bbox[2] - word_bbox[0]
                        
                        # Choose color based on highlight
                        if word_index == highlight_word:
                            color = (255, 255, 0, 255)  # Yellow for current word
                            # Add glow effect
                            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                                draw.text((current_x + offset[0], y + offset[1]), 
                                        word, fill=(255, 200, 0, 100), font=font)
                        else:
                            color = (255, 255, 255, 255)  # White for other words
                        
                        draw.text((current_x, y), word, fill=color, font=font)
                        current_x += word_width
                        word_index += 1
            
            return np.array(img)
        
        subtitle_clip = VideoClip(make_frame, duration=total_duration).set_fps(self.fps)
        return subtitle_clip
    
    def add_professional_effects(self, clip: VideoClip, effect_type: str = "zoom_pan") -> VideoClip:
        """Add professional effects to video clips"""
        duration = clip.duration
        
        if effect_type == "zoom_pan":
            def zoom_pan_effect(get_frame, t):
                frame = get_frame(t)
                
                # Gentle zoom and pan
                zoom_factor = 1.0 + 0.15 * (t / duration)
                pan_x = int(30 * math.sin(t * 0.3))
                pan_y = int(15 * math.cos(t * 0.2))
                
                h, w = frame.shape[:2]
                new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
                
                if new_h > h and new_w > w:
                    resized = cv2.resize(frame, (new_w, new_h))
                    
                    start_x = max(0, min((new_w - w) // 2 + pan_x, new_w - w))
                    start_y = max(0, min((new_h - h) // 2 + pan_y, new_h - h))
                    
                    return resized[start_y:start_y + h, start_x:start_x + w]
                
                return frame
            
            return clip.fl(zoom_pan_effect)
        
        elif effect_type == "fade_in":
            return clip.fadein(0.8)
        
        elif effect_type == "fade_out":
            return clip.fadeout(0.8)
        
        return clip
    
    async def text_to_speech_with_timing(self, text: str, voice="en-US-AriaNeural") -> str:
        """Generate speech with high quality"""
        print(f"🎤 Generating high-quality speech: {text[:50]}...")
        
        # Clean text for TTS
        clean_text = re.sub(r'[*_#@]', '', text)
        clean_text = re.sub(r'\n+', '. ', clean_text)
        clean_text = re.sub(r'₹', 'rupees ', clean_text)  # Convert currency symbol
        
        # Generate speech
        communicate = edge_tts.Communicate(clean_text, voice)
        output_path = self.temp_dir / "full_speech.wav"
        await communicate.save(str(output_path))
        
        print(f"✅ High-quality speech generated: {output_path}")
        return str(output_path)
    
    async def generate_professional_video(self, script: str, title: str = "AI Generated Video") -> str:
        """Generate InVideo AI quality professional video"""
        print(f"\n🚀 GENERATING INVIDEO AI QUALITY VIDEO: {title}")
        print("=" * 60)
        
        # Step 1: Analyze script with AI
        print("\n🤖 STEP 1: AI Script Analysis...")
        analysis = await self.analyze_script_with_gemini(script)
        theme = analysis.get("theme", "wealth")
        segments = analysis["segments"]
        
        print(f"📊 Theme: {theme}")
        print(f"📋 Segments: {len(segments)}")
        
        # Step 2: Generate high-quality speech
        print("\n🎤 STEP 2: Generating Professional Audio...")
        audio_path = await self.text_to_speech_with_timing(script)
        
        # Step 3: Get precise word timing
        print("\n⏱️ STEP 3: Analyzing Audio Timing...")
        word_timings = await self.get_precise_audio_timing(audio_path, script)
        
        # Load audio clip
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        # Step 4: Create professional visuals
        print("\n🎨 STEP 4: Creating Professional Visuals...")
        bg_images = self.create_professional_backgrounds(len(segments), theme)
        
        # Step 5: Create video segments with effects
        print("\n🎬 STEP 5: Creating Professional Video Segments...")
        video_clips = []
        segment_duration = total_duration / len(segments)
        
        for i, (segment, bg_image) in enumerate(zip(segments, bg_images)):
            print(f"  📹 Creating segment {i+1}/{len(segments)}: {segment['text'][:40]}...")
            
            # Create base video clip from image
            img_clip = ImageClip(bg_image, duration=segment_duration)
            
            # Add professional effects
            img_clip = self.add_professional_effects(img_clip, "zoom_pan")
            
            # Add fade transitions
            if i == 0:
                img_clip = self.add_professional_effects(img_clip, "fade_in")
            if i == len(segments) - 1:
                img_clip = self.add_professional_effects(img_clip, "fade_out")
            
            video_clips.append(img_clip)
        
        # Step 6: Combine all video segments
        print("\n🔧 STEP 6: Professional Video Assembly...")
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Step 7: Add synchronized audio
        final_video = final_video.set_audio(audio_clip)
        
        # Step 8: Create and add dynamic subtitles
        print("\n📝 STEP 8: Adding Dynamic Subtitles...")
        subtitle_clip = self.create_dynamic_subtitle_clip(word_timings, total_duration)
        
        # Composite video with subtitles
        final_video = CompositeVideoClip([final_video, subtitle_clip])
        
        # Step 9: Export professional video
        print("\n💾 STEP 9: Exporting Professional Video...")
        output_path = self.output_dir / f"{title.replace(' ', '_')}_Professional.mp4"
        
        print(f"📁 Output: {output_path}")
        print("⏳ This may take a few minutes for professional quality...")
        
        final_video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            preset='medium',
            ffmpeg_params=[
                '-crf', '20',  # High quality
                '-pix_fmt', 'yuv420p',  # Compatibility
                '-movflags', '+faststart'  # Fast streaming
            ]
        )
        
        # Cleanup
        audio_clip.close()
        final_video.close()
        
        print(f"\n🎉 PROFESSIONAL VIDEO COMPLETE!")
        print(f"📁 Location: {output_path}")
        print(f"⏱️ Duration: {total_duration:.2f} seconds")
        print(f"📱 Format: {self.width}x{self.height} (Perfect for YouTube Shorts)")
        print(f"🎯 Quality: InVideo AI Professional Grade")
        print(f"✨ Features: Dynamic subtitles, Professional effects, Perfect sync")
        
        return str(output_path)

# Demo with your script
async def main():
    """Demo the professional video generator"""
    
    script = """You're not poor because of your salary.  
You're poor because of your habits.

Let me explain.

You earn ₹30,000 a month...  
But spend ₹35,000.  
How?  
EMIs, subscriptions, impulse shopping.  
Death by a thousand cuts.

Now imagine investing just ₹5,000 every month.  
That's ₹60,000 a year.  
Invested for 10 years at 12%?  
You'd have over ₹11 lakhs.

But most people never start.  
They wait for "more money".  
But it's not about how much you earn.  
It's about how much you **keep**.

Track your expenses.  
Cut the crap.  
Invest early.  
And watch your future self thank you.

Follow @WealthierEveryday for real money talk that actually makes you richer."""
    
    # Initialize generator (add your Gemini API key for enhanced features)
    generator = ProfessionalAIVideoGenerator(gemini_api_key=None)
    
    # Generate professional video
    video_path = await generator.generate_professional_video(
        script, 
        "Poor_Habits_vs_Rich_Habits_Professional"
    )
    
    print(f"\n🎬 Your InVideo AI quality video is ready!")
    print(f"📁 Location: {video_path}")
    print(f"🚀 Ready to upload to YouTube Shorts!")

if __name__ == "__main__":
    asyncio.run(main())
    def __init__(self, output_dir="output", gemini_api_key=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Video settings for YouTube Shorts (InVideo AI quality)
        self.width = 1080
        self.height = 1920  # 9:16 aspect ratio
        self.fps = 30
        
        # Professional color schemes for different moods
        self.color_schemes = {
            'wealth': {
                'primary': '#2E8B57',    # Sea Green
                'secondary': '#FFD700',  # Gold
                'accent': '#FF6B35',     # Orange Red
                'text': '#FFFFFF',       # White
                'bg_start': '#1A1A1A',   # Dark
                'bg_end': '#2E8B57'      # Green
            },
            'business': {
                'primary': '#1E3A8A',    # Deep Blue
                'secondary': '#3B82F6',  # Blue
                'accent': '#10B981',     # Emerald
                'text': '#FFFFFF',
                'bg_start': '#0F172A',   # Slate
                'bg_end': '#1E3A8A'
            },
            'motivation': {
                'primary': '#DC2626',    # Red
                'secondary': '#F59E0B',  # Amber
                'accent': '#EF4444',     # Red
                'text': '#FFFFFF',
                'bg_start': '#1F2937',   # Gray
                'bg_end': '#DC2626'
            }
        }
        
        # Initialize Google Gemini if API key provided
        self.gemini_enabled = False
        if gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                self.gemini_enabled = True
                print("🤖 Google Gemini AI initialized!")
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
        
        # Initialize Stable Diffusion for image generation
        self.sd_pipe = None
        self.init_stable_diffusion()
        
        # Load Whisper for precise audio timing
        print("🎤 Loading Whisper for audio timing...")
        self.whisper_model = whisper.load_model("base")
        
        print("🎬 Professional AI Video Generator initialized!")
        print("🎯 InVideo AI quality video generation ready!")
    
    def init_stable_diffusion(self):
        """Initialize Stable Diffusion for AI image generation"""
        try:
            print("🎨 Loading Stable Diffusion for AI image generation...")
            self.sd_pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            if torch.cuda.is_available():
                self.sd_pipe = self.sd_pipe.to("cuda")
                print("🚀 Stable Diffusion loaded on GPU!")
            else:
                print("💻 Stable Diffusion loaded on CPU (slower but works)")
                
        except Exception as e:
            print(f"⚠️ Stable Diffusion not available: {e}")
            print("📝 Will use gradient backgrounds instead")
    
    async def analyze_script_with_gemini(self, script: str) -> Dict:
        """Use Google Gemini to analyze script and suggest visuals"""
        if not self.gemini_enabled:
            return self.fallback_script_analysis(script)
        
        try:
            prompt = f"""
            Analyze this YouTube Shorts script about wealth/finance and provide:
            1. Main theme/mood (wealth, business, motivation, etc.)
            2. Key segments (break into 5-8 parts)
            3. Visual descriptions for each segment (for AI image generation)
            4. Emotional tone for each segment
            5. Keywords for visuals
            
            Script: {script}
            
            Return as JSON format:
            {{
                "theme": "wealth",
                "segments": [
                    {{
                        "text": "segment text",
                        "visual_prompt": "AI image prompt",
                        "mood": "serious/exciting/motivational",
                        "duration_weight": 1.0
                    }}
                ]
            }}
            """
            
            response = self.gemini_model.generate_content(prompt)
            result = json.loads(response.text.strip())
            print("🤖 Gemini script analysis complete!")
            return result
            
        except Exception as e:
            print(f"⚠️ Gemini analysis failed: {e}")
            return self.fallback_script_analysis(script)
    
    def fallback_script_analysis(self, script: str) -> Dict:
        """Fallback script analysis without Gemini"""
        print("📋 Using fallback script analysis...")
        
        # Split script into segments
        lines = [line.strip() for line in script.split('\n') if line.strip()]
        segments = []
        
        for line in lines:
            if len(line.split()) >= 3:  # At least 3 words
                # Generate visual prompts based on keywords
                visual_prompt = self.generate_visual_prompt(line)
                segments.append({
                    "text": line,
                    "visual_prompt": visual_prompt,
                    "mood": "motivational",
                    "duration_weight": 1.0
                })
        
        return {
            "theme": "wealth",
            "segments": segments
        }
    
    def generate_visual_prompt(self, text: str) -> str:
        """Generate AI image prompts based on text content"""
        text_lower = text.lower()
        
        # Financial/wealth related prompts
        if any(word in text_lower for word in ['money', 'salary', 'earn', 'income']):
            return "professional business person counting money, modern office, financial success, cinematic lighting"
        elif any(word in text_lower for word in ['invest', 'investment', 'portfolio']):
            return "stock market charts, investment graphs, financial growth, professional trader workspace"
        elif any(word in text_lower for word in ['habit', 'habits', 'behavior']):
            return "person making good financial decisions, organized life, productivity, minimalist lifestyle"
        elif any(word in text_lower for word in ['spend', 'shopping', 'expense']):
            return "shopping mall, credit cards, consumerism, retail therapy, financial stress"
        elif any(word in text_lower for word in ['save', 'saving', 'budget']):
            return "piggy bank, savings account, budgeting app, financial planning, money jar"
        else:
            return "modern financial concept, wealth building, success mindset, professional atmosphere"
    
    async def generate_ai_images(self, segments: List[Dict]) -> List[str]:
        """Generate AI images for each segment using Stable Diffusion"""
        print("🎨 Generating AI images for each segment...")
        images = []
        
        if not self.sd_pipe:
            print("📝 Using gradient backgrounds (SD not available)")
            return self.create_professional_backgrounds(len(segments))
        
        for i, segment in enumerate(segments):
            try:
                print(f"  🖼️ Generating image {i+1}/{len(segments)}: {segment['visual_prompt'][:50]}...")
                
                # Enhanced prompt for better quality
                enhanced_prompt = f"{segment['visual_prompt']}, professional photography, high quality, 4K, cinematic, detailed"
                
                # Generate image
                with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
                    image = self.sd_pipe(
                        enhanced_prompt,
                        height=self.height,
                        width=self.width,
                        num_inference_steps=20,  # Faster generation
                        guidance_scale=7.5
                    ).images[0]
                
                # Save image
                img_path = self.temp_dir / f"ai_image_{i}.jpg"
                image.save(str(img_path), quality=95)
                images.append(str(img_path))
                
            except Exception as e:
                print(f"⚠️ Failed to generate image {i}: {e}")
                # Fallback to gradient
                gradient_path = self.create_single_gradient(i)
                images.append(gradient_path)
        
        print(f"✅ Generated {len(images)} AI images")
        return images
    
    def create_professional_backgrounds(self, count: int) -> List[str]:
        """Create professional gradient backgrounds"""
        print("🎨 Creating professional gradient backgrounds...")
        
        images = []
        gradients = [
            ('#1a1a2e', '#16213e', '#0f3460'),  # Deep blue gradient
            ('#2d1b69', '#11998e', '#38ef7d'),  # Purple to teal
            ('#8b5a3c', '#f4a261', '#e76f51'),  # Warm golden
            ('#2c3e50', '#3498db', '#9b59b6'),  # Corporate blue
            ('#1e3c72', '#2a5298', '#7b68ee'),  # Professional blue
        ]
        
        for i in range(count):
            colors = gradients[i % len(gradients)]
            img = self.create_advanced_gradient(colors, i)
            images.append(img)
        
        return images
    
    def create_advanced_gradient(self, colors: Tuple, index: int) -> str:
        """Create advanced gradient with effects"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        # Create multi-color gradient
        for y in range(self.height):
            ratio1 = y / (self.height * 0.5)
            ratio2 = (y - self.height * 0.5) / (self.height * 0.5)
            
            if y < self.height * 0.5:
                # First half gradient
                ratio = min(ratio1, 1.0)
                r1, g1, b1 = tuple(int(colors[0][1:][i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(colors[1][1:][i:i+2], 16) for i in (0, 2, 4))
            else:
                # Second half gradient
                ratio = max(min(ratio2, 1.0), 0.0)
                r1, g1, b1 = tuple(int(colors[1][1:][i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(colors[2][1:][i:i+2], 16) for i in (0, 2, 4))
            
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Add subtle pattern overlay
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Add diagonal lines for texture
        for x in range(0, self.width + 100, 100):
            overlay_draw.line([(x, 0), (x - 200, self.height)], fill=(255, 255, 255, 10), width=2)
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        img_path = self.temp_dir / f"gradient_bg_{index}.jpg"
        img.save(str(img_path), quality=95)
        
        return str(img_path)
    
    def create_single_gradient(self, index: int) -> str:
        """Create a single gradient background"""
        gradients = [
            ('#2E8B57', '#1A1A1A'),  # Green to dark
            ('#FFD700', '#FF6B35'),  # Gold to orange
            ('#4A90E2', '#1A1A1A'),  # Blue to dark
            ('#9B59B6', '#2C3E50'),  # Purple to dark blue
            ('#E74C3C', '#1A1A1A'),  # Red to dark
        ]
        return self.create_advanced_gradient(gradients[index % len(gradients)], index)
    
    async def get_precise_audio_timing(self, audio_path: str, script: str) -> List[Dict]:
        """Get precise word-level timing using Whisper"""
        print("🎤 Analyzing audio for precise word timing...")
        
        try:
            # Load audio and get transcription with timestamps
            audio = whisper.load_audio(audio_path)
            result = whisper.transcribe(self.whisper_model, audio, language="en")
            
            word_timings = []
            for segment in result.get("segments", []):
                for word_info in segment.get("words", []):
                    word_timings.append({
                        "word": word_info["text"].strip(),
                        "start": word_info["start"],
                        "end": word_info["end"],
                        "confidence": word_info.get("confidence", 1.0)
                    })
            
            print(f"✅ Extracted timing for {len(word_timings)} words")
            return word_timings
            
        except Exception as e:
            print(f"⚠️ Whisper timing failed: {e}")
            # Fallback to estimated timing
            return self.estimate_word_timing(script, AudioFileClip(audio_path).duration)
    
    def estimate_word_timing(self, script: str, total_duration: float) -> List[Dict]:
        """Fallback method to estimate word timing"""
        words = script.split()
        word_duration = total_duration / len(words)
        
        word_timings = []
        for i, word in enumerate(words):
            start_time = i * word_duration
            end_time = (i + 1) * word_duration
            word_timings.append({
                "word": word,
                "start": start_time,
                "end": end_time,
                "confidence": 1.0
            })
        
        return word_timings
    
    def create_dynamic_subtitle_clip(self, word_timings: List[Dict], total_duration: float) -> VideoClip:
        """Create dynamic animated subtitles that appear word by word"""
        print("📝 Creating dynamic animated subtitles...")
        
        def make_frame(t):
            # Create transparent frame
            frame = np.zeros((self.height, self.width, 4), dtype=np.uint8)
            img = Image.fromarray(frame, 'RGBA')
            draw = ImageDraw.Draw(img)
            
            # Load font
            try:
                font_size = 80
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Find current words to display
            current_words = []
            for word_info in word_timings:
                if word_info["start"] <= t <= word_info["end"] + 0.3:  # Show word slightly longer
                    current_words.append(word_info)
            
            if current_words:
                # Create text line
                text_line = " ".join([w["word"] for w in current_words[-5:]])  # Show last 5 words
                
                # Calculate position
                bbox = draw.textbbox((0, 0), text_line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (self.width - text_width) // 2
                y = self.height - 300  # Bottom third
                
                # Add background rectangle
                padding = 20
                rect_coords = [
                    x - padding, y - padding,
                    x + text_width + padding, y + text_height + padding
                ]
                draw.rounded_rectangle(rect_coords, radius=15, fill=(0, 0, 0, 180))
                
                # Add text with animation effect
                for i, word_info in enumerate(current_words[-5:]):
                    word = word_info["word"]
                    word_start_x = x + sum([draw.textbbox((0, 0), w["word"] + " ", font=font)[2] 
                                          for w in current_words[-5:][:i]])
                    
                    # Highlight current word
                    if word_info["start"] <= t <= word_info["end"]:
                        # Current word - yellow highlight
                        draw.text((word_start_x, y), word, fill=(255, 255, 0, 255), font=font)
                    else:
                        # Previous words - white
                        draw.text((word_start_x, y), word, fill=(255, 255, 255, 255), font=font)
            
            return np.array(img)
        
        subtitle_clip = VideoClip(make_frame, duration=total_duration).set_fps(self.fps)
        return subtitle_clip
    
    def add_professional_effects(self, clip: VideoClip, effect_type: str = "zoom_pan") -> VideoClip:
        """Add professional effects to video clips"""
        duration = clip.duration
        
        if effect_type == "zoom_pan":
            def zoom_pan_effect(get_frame, t):
                frame = get_frame(t)
                
                # Zoom factor varies over time
                zoom_factor = 1.0 + 0.1 * (t / duration)  # Slight zoom in
                
                # Pan factor for subtle movement
                pan_x = int(20 * math.sin(t * 0.5))  # Subtle horizontal movement
                pan_y = int(10 * math.cos(t * 0.3))  # Subtle vertical movement
                
                h, w = frame.shape[:2]
                new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
                
                if new_h > h and new_w > w:
                    resized = cv2.resize(frame, (new_w, new_h))
                    
                    # Calculate crop with pan
                    start_x = max(0, min((new_w - w) // 2 + pan_x, new_w - w))
                    start_y = max(0, min((new_h - h) // 2 + pan_y, new_h - h))
                    
                    return resized[start_y:start_y + h, start_x:start_x + w]
                
                return frame
            
            return clip.fl(zoom_pan_effect)
        
        elif effect_type == "fade_in":
            return clip.fadein(0.5)
        
        elif effect_type == "fade_out":
            return clip.fadeout(0.5)
        
        return clip
    
    async def text_to_speech_with_timing(self, text: str, voice="en-US-AriaNeural") -> str:
        """Generate speech with precise timing data"""
        print(f"🎤 Generating high-quality speech: {text[:50]}...")
        
        # Clean text for TTS
        clean_text = re.sub(r'[*_#@]', '', text)
        clean_text = re.sub(r'\n+', '. ', clean_text)
        
        # Generate speech
        communicate = edge_tts.Communicate(clean_text, voice)
        output_path = self.temp_dir / "full_speech.wav"
        await communicate.save(str(output_path))
        
        print(f"✅ High-quality speech generated: {output_path}")
        return str(output_path)
    
    async def generate_professional_video(self, script: str, title: str = "AI Generated Video") -> str:
        """Generate InVideo AI quality professional video"""
        print(f"\n🚀 GENERATING INVIDEO AI QUALITY VIDEO: {title}")
        print("=" * 60)
        
        # Step 1: Analyze script with AI
        print("\n🤖 STEP 1: AI Script Analysis...")
        analysis = await self.analyze_script_with_gemini(script)
        theme = analysis.get("theme", "wealth")
        segments = analysis["segments"]
        
        print(f"📊 Theme: {theme}")
        print(f"📋 Segments: {len(segments)}")
        
        # Step 2: Generate high-quality speech
        print("\n🎤 STEP 2: Generating Professional Audio...")
        audio_path = await self.text_to_speech_with_timing(script)
        
        # Step 3: Get precise word timing
        print("\n⏱️ STEP 3: Analyzing Audio Timing...")
        word_timings = await self.get_precise_audio_timing(audio_path, script)
        
        # Load audio clip
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        # Step 4: Generate AI visuals
        print("\n🎨 STEP 4: Generating AI Visuals...")
        bg_images = await self.generate_ai_images(segments)
        
        # Step 5: Create video segments with effects
        print("\n🎬 STEP 5: Creating Professional Video Segments...")
        video_clips = []
        segment_duration = total_duration / len(segments)
        
        for i, (segment, bg_image) in enumerate(zip(segments, bg_images)):
            print(f"  📹 Creating segment {i+1}/{len(segments)}: {segment['text'][:40]}...")
            
            # Create base video clip from image
            img_clip = ImageClip(bg_image, duration=segment_duration)
            
            # Add professional effects
            img_clip = self.add_professional_effects(img_clip, "zoom_pan")
            
            # Add fade transitions
            if i == 0:
                img_clip = self.add_professional_effects(img_clip, "fade_in")
            if i == len(segments) - 1:
                img_clip = self.add_professional_effects(img_clip, "fade_out")
            
            video_clips.append(img_clip)
        
        # Step 6: Combine all video segments
        print("\n🔧 STEP 6: Professional Video Assembly...")
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Step 7: Add synchronized audio
        final_video = final_video.set_audio(audio_clip)
        
        # Step 8: Create and add dynamic subtitles
        print("\n📝 STEP 8: Adding Dynamic Subtitles...")
        subtitle_clip = self.create_dynamic_subtitle_clip(word_timings, total_duration)
        
        # Composite video with subtitles
        final_video = CompositeVideoClip([final_video, subtitle_clip])
        
        # Step 9: Export professional video
        print("\n💾 STEP 9: Exporting Professional Video...")
        output_path = self.output_dir / f"{title.replace(' ', '_')}_Professional.mp4"
        
        print(f"📁 Output: {output_path}")
        print("⏳ This may take a few minutes for professional quality...")
        
        final_video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            preset='medium',
            ffmpeg_params=[
                '-crf', '18',  # High quality
                '-pix_fmt', 'yuv420p',  # Compatibility
                '-movflags', '+faststart'  # Fast streaming
            ]
        )
        
        # Cleanup
        audio_clip.close()
        final_video.close()
        
        print(f"\n🎉 PROFESSIONAL VIDEO COMPLETE!")
        print(f"📁 Location: {output_path}")
        print(f"⏱️ Duration: {total_duration:.2f} seconds")
        print(f"📱 Format: {self.width}x{self.height} (Perfect for YouTube Shorts)")
        print(f"🎯 Quality: InVideo AI Professional Grade")
        
        return str(output_path)

# Demo with your script
async def main():
    """Demo the professional video generator"""
    
    script = """You're not poor because of your salary.  
You're poor because of your habits.

Let me explain.

You earn ₹30,000 a month...  
But spend ₹35,000.  
How?  
EMIs, subscriptions, impulse shopping.  
Death by a thousand cuts.

Now imagine investing just ₹5,000 every month.  
That's ₹60,000 a year.  
Invested for 10 years at 12%?  
You'd have over ₹11 lakhs.

But most people never start.  
They wait for "more money".  
But it's not about how much you earn.  
It's about how much you **keep**.

Track your expenses.  
Cut the crap.  
Invest early.  
And watch your future self thank you.

Follow @WealthierEveryday for real money talk that actually makes you richer."""
    
    # Initialize generator (add your Gemini API key here)
    generator = ProfessionalAIVideoGenerator(gemini_api_key=None)  # Add your key
    
    # Generate professional video
    video_path = await generator.generate_professional_video(
        script, 
        "Poor_Habits_vs_Rich_Habits_Professional"
    )
    
    print(f"\n🎬 Your InVideo AI quality video is ready!")
    print(f"📁 Location: {video_path}")
    print(f"🚀 Ready to upload to YouTube Shorts!")

if __name__ == "__main__":
    asyncio.run(main())
    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Video settings for YouTube Shorts
        self.width = 1080
        self.height = 1920  # 9:16 aspect ratio
        self.fps = 30
        
        # Colors for Wealthier Everyday brand
        self.colors = {
            'primary': '#2E8B57',     # Sea Green
            'secondary': '#FFD700',   # Gold
            'accent': '#FF6B35',      # Orange Red
            'text': '#FFFFFF',        # White
            'bg': '#1A1A1A'          # Dark background
        }
        
        print("🎬 AI Video Generator initialized!")
    
    async def text_to_speech(self, text, voice="en-US-AriaNeural", output_file="speech.wav"):
        """Convert text to speech using Edge TTS (Microsoft's free TTS)"""
        print(f"🎤 Generating speech for: {text[:50]}...")
        
        # Clean text for TTS
        clean_text = re.sub(r'[*_#@]', '', text)
        clean_text = re.sub(r'\n+', '. ', clean_text)
        
        communicate = edge_tts.Communicate(clean_text, voice)
        output_path = self.temp_dir / output_file
        await communicate.save(str(output_path))
        
        print(f"✅ Speech generated: {output_path}")
        return str(output_path)
    
    def get_free_stock_images(self, keywords, count=5):
        """Get free stock images from Unsplash API"""
        print(f"🖼️  Fetching stock images for: {keywords}")
        
        # Unsplash API (free tier - 50 requests/hour)
        # You can get a free API key from https://unsplash.com/developers
        # For demo, we'll use a fallback method
        
        images = []
        try:
            # Using Picsum for demo (random beautiful images)
            for i in range(count):
                url = f"https://picsum.photos/{self.width}/{self.height}?random={random.randint(1, 1000)}"
                response = requests.get(url)
                if response.status_code == 200:
                    img_path = self.temp_dir / f"stock_image_{i}.jpg"
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                    images.append(str(img_path))
        except Exception as e:
            print(f"⚠️  Could not fetch stock images: {e}")
            # Create gradient backgrounds as fallback
            images = self.create_gradient_backgrounds(count)
        
        print(f"✅ Retrieved {len(images)} background images")
        return images
    
    def create_gradient_backgrounds(self, count=5):
        """Create beautiful gradient backgrounds"""
        print("🎨 Creating gradient backgrounds...")
        
        images = []
        gradients = [
            ('#2E8B57', '#1A1A1A'),  # Green to dark
            ('#FFD700', '#FF6B35'),  # Gold to orange
            ('#4A90E2', '#1A1A1A'),  # Blue to dark
            ('#9B59B6', '#2C3E50'),  # Purple to dark blue
            ('#E74C3C', '#1A1A1A'),  # Red to dark
        ]
        
        for i in range(count):
            color1, color2 = gradients[i % len(gradients)]
            
            # Create gradient
            img = Image.new('RGB', (self.width, self.height))
            draw = ImageDraw.Draw(img)
            
            for y in range(self.height):
                # Calculate color blend ratio
                ratio = y / self.height
                
                # Convert hex to RGB
                r1, g1, b1 = tuple(int(color1[1:][i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(color2[1:][i:i+2], 16) for i in (0, 2, 4))
                
                # Interpolate colors
                r = int(r1 * (1 - ratio) + r2 * ratio)
                g = int(g1 * (1 - ratio) + g2 * ratio)
                b = int(b1 * (1 - ratio) + b2 * ratio)
                
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))
            
            img_path = self.temp_dir / f"gradient_bg_{i}.jpg"
            img.save(str(img_path), quality=95)
            images.append(str(img_path))
        
        print(f"✅ Created {len(images)} gradient backgrounds")
        return images
    
    def create_text_overlay(self, text, duration, bg_image=None):
        """Create animated text overlay"""
        print(f"📝 Creating text overlay: {text[:30]}...")
        
        # Create base image
        if bg_image:
            base = Image.open(bg_image).resize((self.width, self.height))
        else:
            base = Image.new('RGB', (self.width, self.height), self.colors['bg'])
        
        draw = ImageDraw.Draw(base)
        
        # Try to load a good font, fallback to default
        try:
            font_size = 80
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Wrap text for better display
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > self.width - 100:  # Leave margin
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate text position
        total_height = len(lines) * (font_size + 20)
        start_y = (self.height - total_height) // 2
        
        # Add semi-transparent background for text
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.width - text_width) // 2
            y = start_y + i * (font_size + 20)
            
            # Draw text shadow
            draw.text((x + 3, y + 3), line, fill='#000000', font=font)
            # Draw main text
            draw.text((x, y), line, fill=self.colors['text'], font=font)
        
        # Save the image
        img_path = self.temp_dir / f"text_overlay_{random.randint(1000, 9999)}.jpg"
        base.save(str(img_path), quality=95)
        
        print(f"✅ Text overlay created: {img_path}")
        return str(img_path)
    
    def parse_script(self, script):
        """Parse script into segments for video"""
        print("📋 Parsing script into segments...")
        
        # Split script into meaningful segments
        segments = []
        lines = script.strip().split('\n')
        
        current_segment = []
        for line in lines:
            line = line.strip()
            if not line:
                if current_segment:
                    segments.append(' '.join(current_segment))
                    current_segment = []
            else:
                current_segment.append(line)
        
        if current_segment:
            segments.append(' '.join(current_segment))
        
        # Filter out very short segments and combine if needed
        filtered_segments = []
        for segment in segments:
            if len(segment.split()) >= 3:  # At least 3 words
                filtered_segments.append(segment)
        
        print(f"✅ Script parsed into {len(filtered_segments)} segments")
        return filtered_segments
    
    async def generate_video(self, script, title="AI Generated Video"):
        """Main function to generate complete video"""
        print(f"\n🚀 Starting video generation for: {title}")
        print("=" * 50)
        
        # Parse script
        segments = self.parse_script(script)
        
        # Generate speech for entire script
        print("\n🎤 STEP 1: Generating AI Voice...")
        audio_path = await self.text_to_speech(script, output_file="full_speech.wav")
        
        # Load audio to get duration
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        segment_duration = total_duration / len(segments)
        
        print(f"📊 Total duration: {total_duration:.2f}s, Segments: {len(segments)}")
        
        # Get background images
        print("\n🖼️  STEP 2: Creating Visual Content...")
        keywords = "money finance wealth investment business"
        bg_images = self.get_free_stock_images(keywords, len(segments))
        
        # Create video clips for each segment
        print("\n🎬 STEP 3: Assembling Video Clips...")
        video_clips = []
        
        for i, (segment, bg_image) in enumerate(zip(segments, bg_images)):
            print(f"  Creating clip {i+1}/{len(segments)}: {segment[:40]}...")
            
            # Create text overlay
            text_image = self.create_text_overlay(segment, segment_duration, bg_image)
            
            # Create video clip
            clip = ImageClip(text_image, duration=segment_duration)
            video_clips.append(clip)
        
        # Concatenate all clips
        print("\n🔧 STEP 4: Final Video Assembly...")
        final_video = concatenate_videoclips(video_clips)
        
        # Add audio
        final_video = final_video.set_audio(audio_clip)
        
        # Add subtle zoom effect for engagement
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            zoom_factor = 1 + 0.1 * (t / total_duration)  # Slight zoom over time
            h, w = frame.shape[:2]
            new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
            
            if new_h > h and new_w > w:
                # Resize and crop to center
                resized = cv2.resize(frame, (new_w, new_h))
                start_x = (new_w - w) // 2
                start_y = (new_h - h) // 2
                return resized[start_y:start_y + h, start_x:start_x + w]
            return frame
        
        final_video = final_video.fl(zoom_effect)
        
        # Export video
        output_path = self.output_dir / f"{title.replace(' ', '_')}.mp4"
        print(f"\n💾 STEP 5: Exporting Video...")
        print(f"📁 Output: {output_path}")
        
        final_video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            preset='medium',
            ffmpeg_params=['-crf', '23']  # Good quality, reasonable file size
        )
        
        # Cleanup
        audio_clip.close()
        final_video.close()
        
        print(f"\n🎉 SUCCESS! Video generated: {output_path}")
        print(f"📊 Duration: {total_duration:.2f} seconds")
        print(f"📱 Format: {self.width}x{self.height} (9:16 - Perfect for YouTube Shorts)")
        
        return str(output_path)

# Demo script
async def main():
    """Demo function to show video generation"""
    
    script = """You're not poor because of your salary.  
You're poor because of your habits.

Let me explain.

You earn ₹30,000 a month...  
But spend ₹35,000.  
How?  
EMIs, subscriptions, impulse shopping.  
Death by a thousand cuts.

Now imagine investing just ₹5,000 every month.  
That's ₹60,000 a year.  
Invested for 10 years at 12%?  
You'd have over ₹11 lakhs.

But most people never start.  
They wait for "more money".  
But it's not about how much you earn.  
It's about how much you **keep**.

Track your expenses.  
Cut the crap.  
Invest early.  
And watch your future self thank you.

Follow @WealthierEveryday for real money talk that actually makes you richer."""
    
    generator = AIVideoGenerator()
    video_path = await generator.generate_video(script, "Poor_Habits_vs_Rich_Habits")
    
    print(f"\n🎬 Your AI-generated video is ready!")
    print(f"📁 Location: {video_path}")
    print(f"🚀 Ready to upload to YouTube Shorts!")

if __name__ == "__main__":
    asyncio.run(main())
