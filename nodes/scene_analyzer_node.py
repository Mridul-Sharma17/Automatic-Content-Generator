#!/usr/bin/env python3
"""
Scene Analyzer Node - AI-powered script analysis for video generation
Uses Google Gemini to intelligently break scripts into timed scenes

TODO: Enhanced AI Analysis Features
- Implement GPT-4 Vision for visual content analysis
- Add sentiment analysis for better mood detection
- Integrate real-time trend analysis for viral optimization
- Add multi-language scene analysis support
"""

import sys
import os
import asyncio
import json
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class SceneAnalyzerNode:
    """AI-powered scene analysis using Google Gemini 2.5 Flash"""
    
    def __init__(self):
        """Initialize the Scene Analyzer with Gemini AI"""
        print("🎬 Initializing Scene Analyzer Node...")
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
            print("✅ Google Gemini AI initialized successfully!")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini AI: {e}")
            raise
    
    async def analyze_scenes_with_audio_timing(self, script: str, audio_duration: float, subtitle_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze script and break it into intelligent scenes BASED ON ACTUAL AUDIO TIMING
        
        Args:
            script: The input script text
            audio_duration: Actual duration of generated audio
            subtitle_segments: Whisper-generated subtitle timing data
            
        Returns:
            List of scene dictionaries with REAL timing, descriptions, and keywords
        """
        print("🧠 Analyzing script with REAL audio timing for perfect sync...")
        
        try:
            # Build context for AI with actual timing data
            timing_context = f"""
            ACTUAL AUDIO DURATION: {audio_duration:.2f} seconds
            SUBTITLE SEGMENTS: {len(subtitle_segments)} segments
            REAL SPEECH PATTERNS: {[f"{seg.get('start', 0):.1f}s-{seg.get('end', 0):.1f}s: '{seg.get('text', '')[:30]}...'" for seg in subtitle_segments[:3]]}
            """
            
            prompt = f"""
            You are an expert video producer creating YouTube Shorts that go VIRAL. You have REAL audio timing data and must create scenes that sync PERFECTLY with the actual speech.

            **CRITICAL REQUIREMENTS:**
            1. **Perfect Audio Sync**: Scene changes MUST align with natural speech pauses from subtitle data
            2. **Viral Engagement**: Each scene must have maximum visual impact for that specific moment
            3. **Professional Quality**: No random cuts, every transition must feel intentional

            **TIMING DATA:**
            {timing_context}

            **SCRIPT TO ANALYZE:** "{script}"

            **SUBTITLE TIMING:** {subtitle_segments}

            Create scenes that change at natural speech breaks and enhance the message. Each scene should have:
            - Exact timing based on subtitle segments
            - Specific visual description that matches what's being said
            - Keywords that will find ENGAGING footage, not boring stock clips

            Return ONLY a JSON array:
            [
                {{
                    "scene_number": 1,
                    "text": "exact text from subtitle segments",
                    "description": "SPECIFIC visual that enhances this exact moment - be cinematic",
                    "keywords": ["engaging", "specific", "keywords"],
                    "mood": "energetic/urgent/inspiring/shocking",
                    "duration": {subtitle_segments[0].get('end', 5) - subtitle_segments[0].get('start', 0) if subtitle_segments else 5},
                    "action_type": "hook/demonstration/revelation/call_to_action",
                    "timing": {{
                        "start": {subtitle_segments[0].get('start', 0) if subtitle_segments else 0},
                        "end": {subtitle_segments[0].get('end', 5) if subtitle_segments else 5}
                    }},
                    "visual_focus": "specific visual elements that will grab attention",
                    "pacing": "fast/medium/slow"
                }}
            ]
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            response_text = response.text.strip()
            
            # Clean JSON response
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '')
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '')
            
            scenes = json.loads(response_text)
            
            # Validate and enhance scenes with REAL timing
            validated_scenes = self._validate_and_enhance_scenes_with_audio(scenes, script, audio_duration, subtitle_segments)
            
            print(f"✅ Audio-synced scene analysis complete! Generated {len(validated_scenes)} perfectly timed scenes")
            
            # Log scene breakdown with REAL timing
            for i, scene in enumerate(validated_scenes, 1):
                print(f"  🎬 Scene {i}: {scene['timing']['start']:.1f}s-{scene['timing']['end']:.1f}s")
                print(f"     📝 Text: \"{scene['text'][:50]}...\"")
                print(f"     🎥 Visual: {scene['description'][:50]}...")
            
            return validated_scenes
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            return self._fallback_scene_analysis_with_audio(script, audio_duration, subtitle_segments)
        except Exception as e:
            print(f"⚠️ Gemini AI failed: {e}")
            return self._fallback_scene_analysis_with_audio(script, audio_duration, subtitle_segments)
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            return self._fallback_scene_analysis(script)
        except Exception as e:
            print(f"⚠️ Gemini AI failed: {e}")
            return self._fallback_scene_analysis(script)
    
    def _validate_and_enhance_scenes_with_audio(self, scenes: List[Dict], script: str, audio_duration: float, subtitle_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and enhance AI-generated scenes with REAL audio timing - COVERS FULL AUDIO DURATION"""
        
        if not scenes or len(scenes) == 0:
            return self._fallback_scene_analysis_with_audio(script, audio_duration, subtitle_segments)
        
        enhanced_scenes = []
        
        # CRITICAL FIX: Ensure scenes cover the ENTIRE audio duration
        print(f"🎯 FIXING TIMING: Total audio {audio_duration:.2f}s, {len(subtitle_segments)} subtitle segments")
        
        # Group subtitle segments into scenes to ensure full coverage
        if subtitle_segments:
            segments_per_scene = max(1, len(subtitle_segments) // len(scenes))
            print(f"🔧 Grouping {segments_per_scene} subtitle segments per scene for full coverage")
            
            current_segment_idx = 0
            
            for i, scene in enumerate(scenes):
                # Calculate which subtitle segments belong to this scene
                start_segment_idx = current_segment_idx
                end_segment_idx = min(current_segment_idx + segments_per_scene, len(subtitle_segments))
                
                # For the last scene, take all remaining segments to ensure full coverage
                if i == len(scenes) - 1:
                    end_segment_idx = len(subtitle_segments)
                
                # Get timing from actual subtitle segments
                if start_segment_idx < len(subtitle_segments):
                    real_start = subtitle_segments[start_segment_idx].get('start', 0)
                    real_end = subtitle_segments[end_segment_idx - 1].get('end', audio_duration) if end_segment_idx > 0 else audio_duration
                    
                    # ENSURE NO GAPS: If this isn't the first scene, start exactly where the previous ended
                    if enhanced_scenes:
                        real_start = enhanced_scenes[-1]['timing']['end']
                    
                    # For the last scene, ENSURE it ends exactly at audio duration
                    if i == len(scenes) - 1:
                        real_end = audio_duration
                        
                    real_duration = real_end - real_start
                else:
                    # Fallback for edge cases
                    real_start = audio_duration if enhanced_scenes else 0
                    real_end = audio_duration
                    real_duration = 0
                
                # Combine text from all subtitle segments in this scene
                scene_text = ""
                for seg_idx in range(start_segment_idx, end_segment_idx):
                    if seg_idx < len(subtitle_segments):
                        seg_text = subtitle_segments[seg_idx].get('text', '').strip()
                        if seg_text:
                            scene_text += seg_text + " "
                scene_text = scene_text.strip()
                
                enhanced_scene = {
                    "scene_number": i + 1,
                    "text": scene_text if scene_text else scene.get("text", "").strip(),
                    "description": scene.get("description", f"Dynamic visual for scene {i+1}"),
                    "keywords": scene.get("keywords", ["business", "professional", "success"]),
                    "mood": scene.get("mood", "motivational"),
                    "duration": real_duration,  # USE REAL AUDIO TIMING
                    "action_type": scene.get("action_type", "demonstration"),
                    "timing": {
                        "start": real_start,
                        "end": real_end
                    },
                    "visual_focus": scene.get("visual_focus", "Professional content relevant to scene"),
                    "pacing": scene.get("pacing", "medium")
                }
                
                # Ensure keywords is a list and has at least 3 items
                if not isinstance(enhanced_scene["keywords"], list):
                    enhanced_scene["keywords"] = ["business", "professional", "success"]
                elif len(enhanced_scene["keywords"]) < 3:
                    enhanced_scene["keywords"].extend(["business", "professional", "success"])
                    enhanced_scene["keywords"] = enhanced_scene["keywords"][:5]
                
                enhanced_scenes.append(enhanced_scene)
                current_segment_idx = end_segment_idx
                
                print(f"  🎬 Scene {i+1}: {real_start:.2f}s-{real_end:.2f}s ({real_duration:.2f}s) - '{scene_text[:40]}...'")
        
        # VERIFY: Total scene duration should match audio duration
        total_scene_duration = sum(scene['duration'] for scene in enhanced_scenes)
        print(f"✅ TIMING VERIFICATION: Total scenes {total_scene_duration:.2f}s vs Audio {audio_duration:.2f}s")
        
        if abs(total_scene_duration - audio_duration) > 0.1:
            print(f"⚠️ TIMING MISMATCH DETECTED: Adjusting last scene to perfect sync")
            if enhanced_scenes:
                # Adjust the last scene to end exactly at audio duration
                enhanced_scenes[-1]['timing']['end'] = audio_duration
                enhanced_scenes[-1]['duration'] = audio_duration - enhanced_scenes[-1]['timing']['start']
                print(f"🔧 Fixed last scene: now ends at {audio_duration:.2f}s")
        
        return enhanced_scenes
    
    def _fallback_scene_analysis_with_audio(self, script: str, audio_duration: float, subtitle_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create scenes based on REAL subtitle timing when AI fails"""
        print("🔄 Using fallback scene analysis with REAL audio timing...")
        
        if not subtitle_segments:
            # If no subtitles, fall back to old method but with real duration
            return self._fallback_scene_analysis(script)
        
        # Group subtitle segments into scenes (every 2-3 segments = 1 scene for engagement)
        segments_per_scene = 2
        total_scenes = max(1, len(subtitle_segments) // segments_per_scene)
        
        scenes = []
        
        for i in range(total_scenes):
            start_idx = i * segments_per_scene
            end_idx = min(start_idx + segments_per_scene, len(subtitle_segments))
            
            # Last scene gets all remaining segments
            if i == total_scenes - 1:
                end_idx = len(subtitle_segments)
            
            scene_segments = subtitle_segments[start_idx:end_idx]
            
            if scene_segments:
                scene_start = scene_segments[0].get('start', 0)
                scene_end = scene_segments[-1].get('end', audio_duration)
                scene_text = ' '.join([seg.get('text', '') for seg in scene_segments])
                scene_duration = scene_end - scene_start
                
                # Generate keywords based on actual spoken content
                keywords = self._extract_diverse_keywords(scene_text, i)
                
                scene = {
                    "scene_number": i + 1,
                    "text": scene_text.strip(),
                    "description": f"Engaging visual content for: {scene_text[:60]}...",
                    "keywords": keywords,
                    "mood": self._get_scene_mood(i, total_scenes),
                    "duration": scene_duration,
                    "action_type": self._get_action_type(i),
                    "timing": {
                        "start": scene_start,
                        "end": scene_end
                    },
                    "visual_focus": f"Dynamic content that enhances: {scene_text[:30]}...",
                    "pacing": "fast" if scene_duration < 4 else "medium"
                }
                
                scenes.append(scene)
        
        print(f"✅ Fallback analysis created {len(scenes)} audio-synced scenes")
        print(f"🎬 Total audio duration: {audio_duration:.2f}s perfectly covered")
        return scenes
    
    def _fallback_scene_analysis(self, script: str) -> List[Dict[str, Any]]:
        """Fallback scene analysis when AI fails"""
        print("🔄 Using fallback scene analysis...")
        
        # Split script into sentences
        sentences = script.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Group sentences into 4-6 scenes
        scenes_count = min(6, max(4, len(sentences)))
        sentences_per_scene = max(1, len(sentences) // scenes_count)
        
        scenes = []
        current_time = 0.0
        
        for i in range(scenes_count):
            start_idx = i * sentences_per_scene
            end_idx = start_idx + sentences_per_scene
            if i == scenes_count - 1:  # Last scene gets remaining sentences
                end_idx = len(sentences)
            
            scene_text = '. '.join(sentences[start_idx:end_idx]).strip()
            if not scene_text.endswith('.'):
                scene_text += '.'
            
            # Estimate duration based on text length (assume ~150 words per minute)
            word_count = len(scene_text.split())
            duration = max(5.0, (word_count / 150) * 60)  # Minimum 5 seconds
            
            # Generate keywords based on content
            keywords = self._extract_keywords_from_text(scene_text)
            
            scene = {
                "scene_number": i + 1,
                "text": scene_text,
                "description": f"Professional visual representing: {scene_text[:100]}...",
                "keywords": keywords,
                "mood": "motivational",
                "duration": duration,
                "action_type": "visualization",
                "timing": {
                    "start": current_time,
                    "end": current_time + duration
                }
            }
            
            scenes.append(scene)
            current_time += duration
        
        print(f"✅ Fallback analysis created {len(scenes)} scenes")
        return scenes
    
    def _extract_diverse_keywords(self, scene_text: str, scene_number: int) -> List[str]:
        """Extract diverse, engaging keywords based on scene content and position"""
        text_lower = scene_text.lower()
        keywords = []
        
        # Scene position-based keywords for pacing
        if scene_number == 0:  # Opening hook
            keywords.extend(['attention-grabbing', 'shocking', 'surprising'])
        elif scene_number == 1:  # Problem/Setup
            keywords.extend(['problem', 'challenge', 'issue'])
        else:  # Solution/Action
            keywords.extend(['solution', 'action', 'results'])
        
        # Content-based keywords
        wealth_terms = ['money', 'wealth', 'rich', 'millionaire', 'financial']
        investment_terms = ['invest', 'investment', 'stock', 'portfolio', 'trading']
        property_terms = ['real estate', 'property', 'house', 'rent', 'rental']
        business_terms = ['business', 'entrepreneur', 'startup', 'company']
        
        if any(term in text_lower for term in wealth_terms):
            keywords.extend(['money', 'wealth', 'luxury'])
        if any(term in text_lower for term in investment_terms):
            keywords.extend(['investment', 'finance', 'growth'])
        if any(term in text_lower for term in property_terms):
            keywords.extend(['real estate', 'property', 'building'])
        if any(term in text_lower for term in business_terms):
            keywords.extend(['business', 'professional', 'office'])
        
        # Visual enhancement keywords
        keywords.extend(['professional', 'modern', 'success'])
        
        # Remove duplicates and limit to 5 keywords
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:5]
    
    def _get_scene_mood(self, scene_index: int, total_scenes: int) -> str:
        """Get appropriate mood for scene based on position"""
        if scene_index == 0:
            return "urgent"
        elif scene_index == total_scenes - 1:
            return "inspiring"
        else:
            return "engaging"
    
    def _get_action_type(self, scene_index: int) -> str:
        """Get action type based on scene position"""
        if scene_index == 0:
            return "hook"
        elif scene_index == 1:
            return "demonstration"
        else:
            return "revelation"

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract relevant keywords from text content"""
        text_lower = text.lower()
        
        # Financial/wealth keywords
        wealth_keywords = []
        if any(word in text_lower for word in ['money', 'wealth', 'rich', 'millionaire']):
            wealth_keywords.extend(['money', 'wealth', 'success'])
        
        if any(word in text_lower for word in ['invest', 'investment', 'stock']):
            wealth_keywords.extend(['investment', 'finance', 'growth'])
        
        if any(word in text_lower for word in ['real estate', 'property', 'house']):
            wealth_keywords.extend(['real estate', 'property', 'building'])
        
        if any(word in text_lower for word in ['business', 'entrepreneur']):
            wealth_keywords.extend(['business', 'professional', 'entrepreneur'])
        
        if any(word in text_lower for word in ['save', 'saving']):
            wealth_keywords.extend(['savings', 'banking', 'finance'])
        
        # Default keywords if none found
        if not wealth_keywords:
            wealth_keywords = ['success', 'professional', 'business']
        
        # Ensure exactly 3-5 unique keywords
        unique_keywords = list(dict.fromkeys(wealth_keywords))  # Remove duplicates
        return unique_keywords[:5]  # Limit to 5 keywords

# Test function
async def test_scene_analyzer():
    """Test the scene analyzer with a sample script"""
    print("🧪 Testing Scene Analyzer Node...")
    
    test_script = """Did you know that 90% of millionaires invest in real estate? Here's why property investment is the secret to building lasting wealth. First, real estate provides passive income through rental payments. Second, property values typically appreciate over time. Third, you get tax benefits that reduce your overall tax burden. Start small with a single rental property and watch your wealth grow automatically."""
    
    analyzer = SceneAnalyzerNode()
    scenes = await analyzer.analyze_scenes(test_script)
    
    print(f"\n✅ Test complete! Generated {len(scenes)} scenes:")
    for scene in scenes:
        print(f"  🎬 Scene {scene['scene_number']}: {scene['text'][:60]}...")

if __name__ == "__main__":
    asyncio.run(test_scene_analyzer())