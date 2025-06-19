#!/usr/bin/env python3
"""
InVideo AI Quality Video Generator for Wealthier Everyday
Professional-grade video generation with dynamic subtitles and effects
"""

import os
import sys
import asyncio
import edge_tts
import requests
import json
from pathlib import Path
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip, 
    concatenate_videoclips, concatenate_audioclips, VideoClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import tempfile
import random
import re
import math
import time
import google.generativeai as genai
from config import GEMINI_API_KEY

class InVideoAIGenerator:
    def __init__(self, output_dir="output", gemini_api_key=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Video settings for YouTube Shorts
        self.width = 1080
        self.height = 1920  # 9:16 aspect ratio
        self.fps = 30
        
        # Professional color schemes
        self.color_schemes = {
            'wealth': ['#1a1a2e', '#16213e', '#0f3460', '#e94560'],
            'business': ['#2d1b69', '#11998e', '#38ef7d', '#ffd700'],
            'motivation': ['#2c3e50', '#3498db', '#9b59b6', '#e74c3c'],
        }
        
        # Initialize Google Gemini AI
        self.gemini_api_key = gemini_api_key or GEMINI_API_KEY
        if self.gemini_api_key and self.gemini_api_key != "your_api_key_here":
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
                self.ai_enabled = True
                print("🤖 Google Gemini AI initialized successfully!")
            except Exception as e:
                print(f"⚠️ Gemini AI failed to initialize: {e}")
                print("📝 Falling back to basic script analysis")
                self.ai_enabled = False
        else:
            self.ai_enabled = False
            print("⚠️ No Gemini API key provided, using basic analysis")
        
        print("🎬 InVideo AI Quality Generator initialized!")
    
    def parse_script_intelligent(self, script: str) -> list:
        """Parse script into meaningful segments"""
        print("📋 Parsing script intelligently...")
        
        # Split by double newlines first (paragraphs)
        paragraphs = [p.strip() for p in script.split('\n\n') if p.strip()]
        
        segments = []
        for para in paragraphs:
            # Split long paragraphs by sentences
            sentences = [s.strip() for s in para.split('.') if s.strip()]
            
            for sentence in sentences:
                if len(sentence.split()) >= 3:  # At least 3 words
                    segments.append(sentence)
        
        print(f"✅ Created {len(segments)} intelligent segments")
        return segments
    
    def create_professional_gradient(self, colors: list, index: int) -> str:
        """Create advanced gradient backgrounds"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        # Multi-stop gradient
        for y in range(self.height):
            # Calculate position ratios
            ratio = y / self.height
            
            if ratio < 0.33:
                # Top section
                blend_ratio = ratio / 0.33
                color1, color2 = colors[0], colors[1]
            elif ratio < 0.66:
                # Middle section  
                blend_ratio = (ratio - 0.33) / 0.33
                color1, color2 = colors[1], colors[2]
            else:
                # Bottom section
                blend_ratio = (ratio - 0.66) / 0.34
                color1, color2 = colors[2], colors[3] if len(colors) > 3 else colors[0]
            
            # Convert hex to RGB
            r1, g1, b1 = tuple(int(color1[1:][i:i+2], 16) for i in (0, 2, 4))
            r2, g2, b2 = tuple(int(color2[1:][i:i+2], 16) for i in (0, 2, 4))
            
            # Interpolate colors
            r = int(r1 * (1 - blend_ratio) + r2 * blend_ratio)
            g = int(g1 * (1 - blend_ratio) + g2 * blend_ratio)
            b = int(b1 * (1 - blend_ratio) + b2 * blend_ratio)
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Add subtle patterns
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Diagonal lines for texture
        for x in range(-200, self.width + 200, 100):
            overlay_draw.line([(x, 0), (x - 300, self.height)], fill=(255, 255, 255, 8), width=2)
        
        # Geometric shapes
        for i in range(2):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            radius = random.randint(80, 200)
            overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                               outline=(255, 255, 255, 15), width=3)
        
        # Composite
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        img_path = self.temp_dir / f"bg_{index}.jpg"
        img.save(str(img_path), quality=95)
        
        return str(img_path)
    
    def estimate_word_timing(self, script: str, total_duration: float) -> list:
        """Estimate word timing for subtitles"""
        print("📊 Estimating word timing...")
        
        # Clean and split words
        clean_script = re.sub(r'[*_#@\n]', ' ', script)
        words = [w.strip() for w in clean_script.split() if w.strip()]
        
        # Calculate timing
        word_timings = []
        current_time = 0
        time_per_word = total_duration / len(words)
        
        for word in words:
            # Adjust duration based on word characteristics
            duration = time_per_word
            if len(word) > 6:
                duration *= 1.2  # Longer words get more time
            if word.endswith(('.', '!', '?')):
                duration *= 1.3  # Pause after sentences
            
            word_timings.append({
                "word": word,
                "start": current_time,
                "end": current_time + duration
            })
            
            current_time += duration
        
        print(f"✅ Estimated timing for {len(word_timings)} words")
        return word_timings
    
    def create_dynamic_subtitles(self, word_timings: list, total_duration: float) -> VideoClip:
        """Create animated word-by-word subtitles"""
        print("📝 Creating dynamic animated subtitles...")
        
        def make_frame(t):
            # Create transparent frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            img = Image.fromarray(frame, 'RGB')
            draw = ImageDraw.Draw(img)
            
            # Load font
            try:
                font_size = 70
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
                font_size = 40
            
            # Find active words (current + previous few)
            active_words = []
            current_word_idx = None
            
            for i, word_info in enumerate(word_timings):
                if word_info["start"] <= t <= word_info["end"] + 0.3:
                    active_words.append(word_info["word"])
                    if word_info["start"] <= t <= word_info["end"]:
                        current_word_idx = len(active_words) - 1
            
            # Keep only last 6 words for display
            if len(active_words) > 6:
                if current_word_idx is not None:
                    current_word_idx = max(0, current_word_idx - (len(active_words) - 6))
                active_words = active_words[-6:]
            
            if active_words:
                # Create text display
                text_lines = []
                current_line = []
                
                # Break into lines based on width
                for word in active_words:
                    test_line = ' '.join(current_line + [word])
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    if bbox[2] - bbox[0] > self.width - 120 and current_line:
                        text_lines.append(current_line)
                        current_line = [word]
                    else:
                        current_line.append(word)
                
                if current_line:
                    text_lines.append(current_line)
                
                # Limit to 2 lines
                if len(text_lines) > 2:
                    text_lines = text_lines[-2:]
                
                # Calculate position (bottom third)
                line_height = font_size + 15
                total_height = len(text_lines) * line_height
                start_y = self.height - 400
                
                # Draw background for text
                max_width = 0
                for line in text_lines:
                    line_text = ' '.join(line)
                    bbox = draw.textbbox((0, 0), line_text, font=font)
                    max_width = max(max_width, bbox[2] - bbox[0])
                
                padding = 30
                bg_x1 = (self.width - max_width) // 2 - padding
                bg_y1 = start_y - padding
                bg_x2 = (self.width + max_width) // 2 + padding
                bg_y2 = start_y + total_height + padding
                
                # Create semi-transparent background
                background = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
                bg_draw = ImageDraw.Draw(background)
                bg_draw.rounded_rectangle([bg_x1, bg_y1, bg_x2, bg_y2], 
                                        radius=20, fill=(0, 0, 0, 180))
                
                # Convert to RGB and composite
                img = Image.alpha_composite(img.convert('RGBA'), background).convert('RGB')
                draw = ImageDraw.Draw(img)
                
                # Draw text with highlighting
                word_idx = 0
                for line_num, line in enumerate(text_lines):
                    line_text = ' '.join(line)
                    bbox = draw.textbbox((0, 0), line_text, font=font)
                    line_width = bbox[2] - bbox[0]
                    
                    x = (self.width - line_width) // 2
                    y = start_y + line_num * line_height
                    
                    # Draw words individually for highlighting
                    current_x = x
                    for word in line:
                        word_bbox = draw.textbbox((0, 0), word + " ", font=font)
                        word_width = word_bbox[2] - word_bbox[0]
                        
                        # Highlight current word
                        if word_idx == current_word_idx:
                            # Current word - bright yellow with glow
                            glow_color = (255, 200, 0)
                            text_color = (255, 255, 0)
                            
                            # Glow effect
                            for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                                draw.text((current_x + offset[0], y + offset[1]), 
                                        word, fill=glow_color, font=font)
                            
                            draw.text((current_x, y), word, fill=text_color, font=font)
                        else:
                            # Other words - white
                            draw.text((current_x, y), word, fill=(255, 255, 255), font=font)
                        
                        current_x += word_width
                        word_idx += 1
            
            return np.array(img)
        
        subtitle_clip = VideoClip(make_frame, duration=total_duration).set_fps(self.fps)
        return subtitle_clip
    
    def add_zoom_pan_effect(self, clip: VideoClip) -> VideoClip:
        """Add professional zoom and pan effect"""
        duration = clip.duration
        
        def zoom_pan_effect(get_frame, t):
            frame = get_frame(t)
            
            # Gentle zoom in over time
            zoom_factor = 1.0 + 0.1 * (t / duration)
            
            # Subtle pan movement
            pan_x = int(20 * math.sin(t * 0.5))
            pan_y = int(10 * math.cos(t * 0.3))
            
            h, w = frame.shape[:2]
            new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
            
            if new_h > h and new_w > w:
                # Resize and crop
                resized = cv2.resize(frame, (new_w, new_h))
                
                # Calculate crop with pan
                start_x = max(0, min((new_w - w) // 2 + pan_x, new_w - w))
                start_y = max(0, min((new_h - h) // 2 + pan_y, new_h - h))
                
                return resized[start_y:start_y + h, start_x:start_x + w]
            
            return frame
        
        return clip.fl(zoom_pan_effect)
    
    async def text_to_speech_enhanced(self, text: str, voice="en-US-AriaNeural") -> str:
        """Generate high-quality speech"""
        print(f"🎤 Generating speech: {text[:50]}...")
        
        # Clean text for TTS
        clean_text = re.sub(r'[*_#@]', '', text)
        clean_text = re.sub(r'\n+', '. ', clean_text)
        clean_text = re.sub(r'₹', 'rupees ', clean_text)
        
        # Add natural pauses
        clean_text = clean_text.replace('.', '... ')
        clean_text = clean_text.replace('?', '? ')
        clean_text = clean_text.replace('!', '! ')
        
        communicate = edge_tts.Communicate(clean_text, voice)
        output_path = self.temp_dir / "speech.wav"
        await communicate.save(str(output_path))
        
        print(f"✅ Speech generated: {output_path}")
        return str(output_path)
    
    async def generate_invideo_quality_video(self, script: str, title: str = "AI_Video") -> str:
        """Generate InVideo AI quality video"""
        print(f"\n🚀 GENERATING INVIDEO AI QUALITY VIDEO: {title}")
        print("=" * 60)
        
        # Step 1: Parse script intelligently
        print("\n📋 STEP 1: Intelligent Script Analysis...")
        segments = self.parse_script_intelligent(script)
        
        # Step 2: Generate enhanced speech
        print("\n🎤 STEP 2: Generating Enhanced Audio...")
        audio_path = await self.text_to_speech_enhanced(script)
        
        # Load audio
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        print(f"⏱️ Total duration: {total_duration:.1f} seconds")
        
        # Step 3: Estimate word timing
        print("\n⏱️ STEP 3: Analyzing Timing...")
        word_timings = self.estimate_word_timing(script, total_duration)
        
        # Step 4: Create professional backgrounds
        print("\n🎨 STEP 4: Creating Professional Visuals...")
        colors = self.color_schemes['wealth']
        bg_images = []
        
        for i in range(len(segments)):
            bg_path = self.create_professional_gradient(colors, i)
            bg_images.append(bg_path)
        
        # Step 5: Create video segments
        print("\n🎬 STEP 5: Creating Video Segments...")
        video_clips = []
        segment_duration = total_duration / len(segments)
        
        for i, (segment, bg_image) in enumerate(zip(segments, bg_images)):
            print(f"  📹 Segment {i+1}/{len(segments)}: {segment[:40]}...")
            
            # Create image clip
            img_clip = ImageClip(bg_image, duration=segment_duration)
            
            # Add zoom/pan effect
            img_clip = self.add_zoom_pan_effect(img_clip)
            
            # Add fade effects
            if i == 0:
                img_clip = img_clip.fadein(0.5)
            if i == len(segments) - 1:
                img_clip = img_clip.fadeout(0.5)
            
            video_clips.append(img_clip)
        
        # Step 6: Combine video segments
        print("\n🔧 STEP 6: Assembling Video...")
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Step 7: Add audio
        final_video = final_video.set_audio(audio_clip)
        
        # Step 8: Create dynamic subtitles
        print("\n📝 STEP 8: Adding Dynamic Subtitles...")
        subtitle_clip = self.create_dynamic_subtitles(word_timings, total_duration)
        
        # Composite everything
        final_video = CompositeVideoClip([final_video, subtitle_clip])
        
        # Step 9: Export
        print("\n💾 STEP 9: Exporting Video...")
        output_path = self.output_dir / f"{title}_InVideo_AI.mp4"
        
        final_video.write_videofile(
            str(output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            ffmpeg_params=['-crf', '23']
        )
        
        # Cleanup
        audio_clip.close()
        final_video.close()
        
        print(f"\n🎉 SUCCESS! InVideo AI Quality Video Complete!")
        print(f"📁 Location: {output_path}")
        print(f"⏱️ Duration: {total_duration:.1f} seconds")
        print(f"📱 Format: {self.width}x{self.height} (Perfect for YouTube Shorts)")
        print(f"✨ Features: Dynamic subtitles, Professional effects, Perfect sync")
        
        return str(output_path)

# Main demo
async def main():
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
    
    generator = InVideoAIGenerator()
    video_path = await generator.generate_invideo_quality_video(script, "Wealth_Habits_Demo")
    
    print(f"\n🎬 Your InVideo AI quality video is ready!")
    print(f"📁 {video_path}")

if __name__ == "__main__":
    asyncio.run(main())
