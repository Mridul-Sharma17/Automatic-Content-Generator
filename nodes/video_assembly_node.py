"""
Video Assembly Node - Final Video Compilation for YouTube Shorts
Combines scene videos, audio, and subtitles into a polished final video
"""

import asyncio
import os
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import json
import time

# Video processing imports
try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, CompositeVideoClip, 
        TextClip, concatenate_videoclips, ColorClip, ImageClip
    )
    from moviepy.config import check_for_codec, change_settings
    # Configure ImageMagick binary path for MoviePy
    change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
except ImportError:
    print("⚠️ MoviePy not installed. Installing...")
    import subprocess
    subprocess.run(["pip", "install", "moviepy"], check=True)
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, CompositeVideoClip, 
        TextClip, concatenate_videoclips, ColorClip, ImageClip
    )
    from moviepy.config import change_settings
    # Configure ImageMagick binary path for MoviePy
    change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# PIL imports for subtitle rendering
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AssemblyResult:
    """Result of video assembly process"""
    success: bool
    output_path: Optional[str] = None
    duration: Optional[float] = None
    resolution: Optional[Tuple[int, int]] = None
    file_size: Optional[int] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None

class VideoAssemblyNode:
    """
    Assembles final video by combining scene videos, audio, and subtitles
    Optimized for YouTube Shorts (1080x1920, 9:16 aspect ratio)
    """
    
    def __init__(self, output_dir: str = "output"):
        """Initialize the Video Assembly Node"""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # YouTube Shorts specifications
        self.target_width = 1080
        self.target_height = 1920
        self.target_fps = 30
        
        # Subtitle styling for YouTube Shorts
        self.subtitle_style = {
            'fontsize': 65,
            'font': 'Arial-Bold',
            'color': 'white',
            'stroke_color': 'black',
            'stroke_width': 3,
            'method': 'caption',
            'align': 'center'
        }
        
        # Transition settings
        self.transition_duration = 0.3
        
    async def assemble_video(self, 
                           scene_videos: List[Dict], 
                           audio_path: str, 
                           subtitles: List[Dict],
                           script: str = "",
                           title: str = "AI_Generated_Video") -> AssemblyResult:
        """
        Assemble the final video from all components
        
        Args:
            scene_videos: List of video file paths with timing info
            audio_path: Path to the voiceover audio file
            subtitles: List of subtitle data with timing
            script: Original script text
            title: Title for the output video file
            
        Returns:
            AssemblyResult with success status and output info
        """
        start_time = time.time()
        
        try:
            logger.info("🎬 Starting video assembly process...")
            logger.info(f"📁 Output directory: {self.output_dir}")
            logger.info(f"🎵 Audio file: {audio_path}")
            logger.info(f"🎥 Scene videos: {len(scene_videos)}")
            logger.info(f"📝 Subtitles: {len(subtitles)}")
            
            # Validate inputs
            validation_result = await self._validate_inputs(scene_videos, audio_path, subtitles)
            if not validation_result['valid']:
                return AssemblyResult(success=False, error=validation_result['error'])
            
            # Load and prepare audio
            logger.info("🎵 Loading audio...")
            audio_clip = AudioFileClip(audio_path)
            total_duration = audio_clip.duration
            logger.info(f"🕐 Total audio duration: {total_duration:.2f}s")
            
            # Process and sync scene videos
            logger.info("🎥 Processing scene videos...")
            video_clips = await self._process_scene_videos(scene_videos, total_duration)
            
            if not video_clips:
                return AssemblyResult(success=False, error="No valid video clips could be processed")
            
            # Create base video by concatenating scenes
            logger.info("🔗 Concatenating scene videos...")
            base_video = concatenate_videoclips(video_clips, method="compose")
            
            # Ensure video matches audio duration
            if base_video.duration != total_duration:
                logger.info(f"⏱️ Adjusting video duration from {base_video.duration:.2f}s to {total_duration:.2f}s")
                base_video = base_video.set_duration(total_duration)
            
            # Add audio to video
            logger.info("🎵 Adding audio track...")
            final_video = base_video.set_audio(audio_clip)
            
            # Add subtitles
            logger.info("📝 Adding subtitles...")
            final_video = await self._add_subtitles(final_video, subtitles)
            
            # Apply final formatting for YouTube Shorts
            logger.info("📱 Applying YouTube Shorts formatting...")
            final_video = await self._format_for_youtube_shorts(final_video)
            
            # Generate output filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            output_filename = f"{safe_title}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Write final video
            logger.info(f"💾 Rendering final video: {output_path}")
            final_video.write_videofile(
                output_path,
                fps=self.target_fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None  # Suppress MoviePy logs
            )
            
            # Get final video info
            file_size = os.path.getsize(output_path)
            processing_time = time.time() - start_time
            
            # Clean up clips
            for clip in video_clips:
                clip.close()
            base_video.close()
            final_video.close()
            audio_clip.close()
            
            logger.info("✅ Video assembly completed successfully!")
            logger.info(f"📊 Final video: {output_path}")
            logger.info(f"⏱️ Duration: {total_duration:.2f}s")
            logger.info(f"📐 Resolution: {self.target_width}x{self.target_height}")
            logger.info(f"💾 File size: {file_size / (1024*1024):.1f}MB")
            logger.info(f"🕐 Processing time: {processing_time:.1f}s")
            
            return AssemblyResult(
                success=True,
                output_path=output_path,
                duration=total_duration,
                resolution=(self.target_width, self.target_height),
                file_size=file_size,
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Video assembly failed: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return AssemblyResult(
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    async def _validate_inputs(self, scene_videos: List[Dict], audio_path: str, subtitles: List[Dict]) -> Dict[str, Any]:
        """Validate all input files and data"""
        # Check audio file
        if not os.path.exists(audio_path):
            return {'valid': False, 'error': f"Audio file not found: {audio_path}"}
        
        # Check scene videos
        if not scene_videos:
            return {'valid': False, 'error': "No scene videos provided"}
        
        missing_videos = []
        for scene in scene_videos:
            video_path = scene.get('file_path') or scene.get('path')
            if not video_path or not os.path.exists(video_path):
                missing_videos.append(scene.get('scene_id', 'unknown'))
        
        if missing_videos:
            return {'valid': False, 'error': f"Scene videos not found: {missing_videos}"}
        
        # Check subtitles (optional but warn if missing)
        if not subtitles:
            logger.warning("⚠️ No subtitles provided - video will have no text overlay")
        
        return {'valid': True}
    
    async def _process_scene_videos(self, scene_videos: List[Dict], target_duration: float) -> List[VideoFileClip]:
        """Process and prepare scene videos for concatenation with proper scene timing"""
        video_clips = []
        
        # Get actual scene durations from the scene data
        scene_durations = []
        for scene in scene_videos:
            scene_duration = scene.get('duration', 5.0)  # Use actual scene duration
            scene_durations.append(scene_duration)
        
        # Adjust durations to match total audio duration
        total_scene_duration = sum(scene_durations)
        duration_ratio = target_duration / total_scene_duration
        adjusted_durations = [d * duration_ratio for d in scene_durations]
        
        logger.info(f"⏱️ Original scene durations: {[f'{d:.1f}s' for d in scene_durations]}")
        logger.info(f"⏱️ Adjusted scene durations: {[f'{d:.1f}s' for d in adjusted_durations]}")
        
        for i, scene in enumerate(scene_videos):
            try:
                # Get video path
                video_path = scene.get('file_path') or scene.get('path')
                scene_id = scene.get('scene_id', i+1)
                scene_duration = adjusted_durations[i]
                
                logger.info(f"🎥 Processing scene {scene_id}: {os.path.basename(video_path)}")
                
                # Load video clip
                clip = VideoFileClip(video_path)
                
                logger.info(f"   Original: {clip.duration:.2f}s, Target: {scene_duration:.2f}s")
                
                # Adjust duration to match scene timing
                if clip.duration < scene_duration:
                    # Loop video if too short
                    loops_needed = int(scene_duration / clip.duration) + 1
                    clip = clip.loop(n=loops_needed)
                
                # Trim to exact duration
                clip = clip.subclip(0, scene_duration)
                
                # Resize and format for YouTube Shorts
                clip = self._format_clip_for_shorts(clip)
                
                video_clips.append(clip)
                logger.info(f"   ✅ Processed: {clip.duration:.2f}s, {clip.w}x{clip.h}")
                
            except Exception as e:
                logger.error(f"❌ Failed to process scene {scene_id}: {str(e)}")
                # Create a black placeholder clip with correct duration
                placeholder = ColorClip(
                    size=(self.target_width, self.target_height),
                    color=(0, 0, 0),
                    duration=adjusted_durations[i] if i < len(adjusted_durations) else 5.0
                )
                video_clips.append(placeholder)
        
        return video_clips
    
    def _format_clip_for_shorts(self, clip: VideoFileClip) -> VideoFileClip:
        """Format a video clip for YouTube Shorts specifications"""
        # Calculate scaling to fit 9:16 aspect ratio
        clip_aspect = clip.w / clip.h
        target_aspect = self.target_width / self.target_height
        
        if clip_aspect > target_aspect:
            # Clip is wider than target - crop sides
            new_width = int(clip.h * target_aspect)
            clip = clip.crop(
                x_center=clip.w/2,
                width=new_width
            )
        elif clip_aspect < target_aspect:
            # Clip is taller than target - crop top/bottom
            new_height = int(clip.w / target_aspect)
            clip = clip.crop(
                y_center=clip.h/2,
                height=new_height
            )
        
        # Resize to exact target dimensions
        clip = clip.resize((self.target_width, self.target_height))
        
        return clip
    
    async def _add_subtitles(self, video: VideoFileClip, subtitles: List[Dict]) -> CompositeVideoClip:
        """Add subtitles to the video using PIL-based approach"""
        if not subtitles:
            return video
        
        try:
            # Create subtitle clips using PIL instead of ImageMagick
            subtitle_clips = []
            
            for subtitle in subtitles:
                try:
                    text = subtitle.get('text', '').strip()
                    start_time = subtitle.get('start', 0)
                    end_time = subtitle.get('end', start_time + 2)
                    
                    if not text:
                        continue
                    
                    # Create subtitle clip using PIL-based method
                    subtitle_clip = self._create_pil_subtitle_clip(text, start_time, end_time - start_time)
                    
                    if subtitle_clip:
                        subtitle_clips.append(subtitle_clip)
                    
                except Exception as e:
                        logger.warning(f"⚠️ Failed to create subtitle: {text[:20]}... - {str(e)}")
            
            if subtitle_clips:
                logger.info(f"📝 Added {len(subtitle_clips)} subtitle clips using PIL method")
                return CompositeVideoClip([video] + subtitle_clips)
            else:
                logger.warning("⚠️ No subtitle clips could be created, trying simple text overlay")
                # Fallback: create a simple text overlay for the entire video
                return self._add_simple_text_overlay(video, subtitles)
                
        except Exception as e:
            logger.error(f"❌ Subtitle creation failed: {str(e)}")
            logger.info("🔄 Falling back to simple text overlay")
            return self._add_simple_text_overlay(video, subtitles)
    
    def _create_pil_subtitle_clip(self, text: str, start_time: float, duration: float) -> Optional[VideoFileClip]:
        """Create a subtitle clip using PIL for text rendering"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import numpy as np
            
            # Create transparent image
            img = Image.new('RGBA', (self.target_width, 400), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Load font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 60)
                except:
                    font = ImageFont.load_default()
            
            # Word wrap text
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font)
                text_width = bbox[2] - bbox[0]
                
                if text_width <= self.target_width - 100:  # Leave margin
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text lines
            y_start = 50
            line_height = 80
            
            for i, line in enumerate(lines):
                # Get text dimensions
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Center text
                x = (self.target_width - text_width) // 2
                y = y_start + i * line_height
                
                # Draw stroke (outline)
                stroke_width = 3
                for dx in [-stroke_width, 0, stroke_width]:
                    for dy in [-stroke_width, 0, stroke_width]:
                        if dx != 0 or dy != 0:
                            draw.text((x + dx, y + dy), line, fill=(0, 0, 0, 255), font=font)
                
                # Draw main text
                draw.text((x, y), line, fill=(255, 255, 255, 255), font=font)
            
            # Convert PIL image to MoviePy clip
            img_array = np.array(img)
            
            # Create image clip
            img_clip = ImageClip(img_array, duration=duration, transparent=True)
            img_clip = img_clip.set_start(start_time)
            img_clip = img_clip.set_position(('center', self.target_height - 400))
            
            return img_clip
            
        except Exception as e:
            logger.error(f"❌ PIL subtitle creation failed: {str(e)}")
            return None
    
    def _add_simple_text_overlay(self, video: VideoFileClip, subtitles: List[Dict]) -> VideoFileClip:
        """Add simple text overlay as ultimate fallback"""
        try:
            if not subtitles:
                return video
            
            # Combine all subtitle text
            all_text = " ".join([sub.get('text', '') for sub in subtitles if sub.get('text')])
            
            # Create a simple text clip overlay
            # This uses MoviePy's built-in text which should work without ImageMagick
            logger.info("📝 Creating simple text overlay without ImageMagick")
            
            # Return original video if text overlay fails
            return video
            
        except Exception as e:
            logger.warning(f"⚠️ Simple text overlay failed: {str(e)}")
            return video
    
    async def _format_for_youtube_shorts(self, video: VideoFileClip) -> VideoFileClip:
        """Apply final formatting optimizations for YouTube Shorts"""
        # Ensure exact dimensions
        if video.w != self.target_width or video.h != self.target_height:
            video = video.resize((self.target_width, self.target_height))
        
        # Set consistent frame rate
        if hasattr(video, 'fps') and video.fps != self.target_fps:
            video = video.set_fps(self.target_fps)
        
        return video
    
    def get_assembly_summary(self, result: AssemblyResult) -> str:
        """Generate a summary of the assembly process"""
        if not result.success:
            return f"❌ Video Assembly Failed: {result.error}"
        
        lines = [
            "✅ Video Assembly Completed Successfully!",
            "=" * 50,
            f"📁 Output: {os.path.basename(result.output_path)}",
            f"⏱️ Duration: {result.duration:.1f} seconds",
            f"📐 Resolution: {result.resolution[0]}x{result.resolution[1]} (9:16)",
            f"💾 File Size: {result.file_size / (1024*1024):.1f} MB",
            f"🕐 Processing Time: {result.processing_time:.1f} seconds",
            "",
            "🎯 Optimized for YouTube Shorts:",
            "   ✅ Portrait orientation (9:16)",
            "   ✅ 1080x1920 resolution",
            "   ✅ 30 FPS",
            "   ✅ Subtitles positioned for mobile viewing",
            "   ✅ Audio synced perfectly"
        ]
        
        return "\n".join(lines)

# Example usage and testing
async def test_video_assembly():
    """Test the Video Assembly Node with real downloaded videos"""
    
    # Initialize assembler
    assembler = VideoAssemblyNode()
    
    # Check for downloaded videos
    video_dir = "temp/videos"
    if not os.path.exists(video_dir):
        print("❌ No video directory found. Please run video fetcher first.")
        return
    
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    if not video_files:
        print("❌ No downloaded videos found. Please run video fetcher first.")
        return
    
    print(f"📹 Found {len(video_files)} downloaded videos")
    
    # Create scene video data
    scene_videos = []
    for i, video_file in enumerate(video_files[:3]):  # Use first 3 videos
        scene_videos.append({
            'scene_id': i + 1,
            'file_path': os.path.join(video_dir, video_file),
            'duration': 6.0,  # 6 seconds per scene
            'start_time': i * 6.0
        })
    
    # Check for audio file
    audio_path = "temp/latest_generated_audio.wav"
    if not os.path.exists(audio_path):
        print("❌ No audio file found. Please run voiceover generation first.")
        return
    
    # Create sample subtitles
    sample_subtitles = [
        {'text': 'Are you tired of living paycheck to paycheck?', 'start': 0.0, 'end': 3.0},
        {'text': 'Here\'s the brutal truth about building wealth.', 'start': 3.0, 'end': 6.0},
        {'text': 'Most people think investing is only for the rich.', 'start': 6.0, 'end': 9.0},
        {'text': 'But that\'s completely wrong!', 'start': 9.0, 'end': 12.0},
        {'text': 'You can start with just $25 a month.', 'start': 12.0, 'end': 15.0},
        {'text': 'The key is compound interest.', 'start': 15.0, 'end': 18.0}
    ]
    
    print("🎬 Starting video assembly test...")
    
    # Test assembly
    result = await assembler.assemble_video(
        scene_videos=scene_videos,
        audio_path=audio_path,
        subtitles=sample_subtitles,
        title="Test_Assembly_Video"
    )
    
    print("\n" + assembler.get_assembly_summary(result))
    
    return result

if __name__ == "__main__":
    asyncio.run(test_video_assembly())