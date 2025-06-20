#!/usr/bin/env python3
"""
Scene Analyzer Node - AI-powered script analysis for video generation
Uses Google Gemini to intelligently break scripts into timed scenes
"""

import sys
import os
import asyncio
import json
from typing import List, Dict, Any
import google.generativeai as genai

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GEMINI_API_KEY

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
    
    async def analyze_scenes(self, script: str) -> List[Dict[str, Any]]:
        """
        Analyze script and break it into intelligent scenes for video generation
        
        Args:
            script: The input script text
            
        Returns:
            List of scene dictionaries with timing, descriptions, and keywords
        """
        print("🧠 Analyzing script with AI for optimal scene breakdown...")
        
        try:
            prompt = f"""
            You are an expert video producer analyzing a script for a YouTube Short. Break this script into 4-6 optimal scenes for video production.

            For each scene, provide:
            1. The exact text segment
            2. Visual description for video search
            3. Keywords for finding relevant stock videos
            4. Mood/tone (energetic, serious, motivational, etc.)
            5. Estimated duration in seconds
            6. Action type (talking_head, demonstration, visualization, etc.)

            Script: "{script}"

            Return ONLY a JSON array in this exact format:
            [
                {{
                    "scene_number": 1,
                    "text": "exact text from script",
                    "description": "detailed visual description for this scene",
                    "keywords": ["keyword1", "keyword2", "keyword3"],
                    "mood": "energetic",
                    "duration": 8.5,
                    "action_type": "talking_head",
                    "timing": {{
                        "start": 0.0,
                        "end": 8.5
                    }}
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
            
            # Validate and enhance scenes
            validated_scenes = self._validate_and_enhance_scenes(scenes, script)
            
            print(f"✅ Scene analysis complete! Generated {len(validated_scenes)} scenes")
            
            # Log scene breakdown
            for i, scene in enumerate(validated_scenes, 1):
                print(f"  🎬 Scene {i}: {scene['text'][:50]}...")
                print(f"     📝 Keywords: {', '.join(scene['keywords'][:3])}")
                print(f"     ⏱️  Duration: {scene['duration']:.1f}s")
            
            return validated_scenes
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            return self._fallback_scene_analysis(script)
        except Exception as e:
            print(f"⚠️ Gemini AI failed: {e}")
            return self._fallback_scene_analysis(script)
    
    def _validate_and_enhance_scenes(self, scenes: List[Dict], script: str) -> List[Dict[str, Any]]:
        """Validate and enhance the AI-generated scenes"""
        
        if not scenes or len(scenes) == 0:
            return self._fallback_scene_analysis(script)
        
        enhanced_scenes = []
        current_time = 0.0
        
        for i, scene in enumerate(scenes):
            # Ensure required fields exist
            enhanced_scene = {
                "scene_number": i + 1,
                "text": scene.get("text", "").strip(),
                "description": scene.get("description", f"Scene {i+1} visuals"),
                "keywords": scene.get("keywords", ["business", "professional", "success"]),
                "mood": scene.get("mood", "motivational"),
                "duration": float(scene.get("duration", 8.0)),
                "action_type": scene.get("action_type", "talking_head"),
                "timing": {
                    "start": current_time,
                    "end": current_time + float(scene.get("duration", 8.0))
                }
            }
            
            # Ensure keywords is a list and has at least 3 items
            if not isinstance(enhanced_scene["keywords"], list):
                enhanced_scene["keywords"] = ["business", "professional", "success"]
            elif len(enhanced_scene["keywords"]) < 3:
                enhanced_scene["keywords"].extend(["business", "professional", "success"])
                enhanced_scene["keywords"] = enhanced_scene["keywords"][:5]  # Limit to 5
            
            enhanced_scenes.append(enhanced_scene)
            current_time = enhanced_scene["timing"]["end"]
        
        return enhanced_scenes
    
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