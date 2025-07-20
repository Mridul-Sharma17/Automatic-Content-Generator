#!/usr/bin/env python3
"""
Viral Script Generator Node - AI-Powered Script Creation with Quality Control
Uses Gemini 2.0 Thinking + Viral Research + Iterative Quality Scoring

APPROACH:
1. Generator AI creates script using viral research patterns
2. Rater AI scores script and provides detailed critique  
3. Feedback loop improves subsequent attempts
4. Progressive quality thresholds with max iteration safety
5. Variety tracking to prevent repetitive patterns
"""

import sys
import os
import asyncio
import json
from typing import Dict, Any, List, Optional, Tuple
import google.generativeai as genai
from datetime import datetime
import logging
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure detailed logging
logger = logging.getLogger(__name__)

class ViralScriptGeneratorNode:
    """AI-powered viral script generator with quality control system"""
    
    def __init__(self):
        """Initialize the Viral Script Generator Node"""
        print("🔥 Initializing Viral Script Generator Node...")
        print("📊 Loading viral content research for AI training...")
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.generator_model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
            self.rater_model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
            print("✅ Gemini 2.0 Thinking models initialized successfully!")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini AI: {e}")
            raise
        
        # Load viral content research
        self.viral_research = self._load_viral_research()
        
        # Quality thresholds (progressive)
        self.quality_thresholds = [80, 85, 90, 95]
        self.max_attempts = 10
        
        # Pattern tracking for variety
        self.used_patterns = []
        self.used_hooks = []
        
        print("✅ Viral Script Generator Node ready!")
    
    def _load_viral_research(self) -> str:
        """Load the viral content research document"""
        try:
            viral_research_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'VIRAL_CONTENT_RESEARCH.md'
            )
            
            with open(viral_research_path, 'r', encoding='utf-8') as f:
                research_content = f.read()
            
            print(f"📚 Loaded {len(research_content)} characters of viral research")
            return research_content
            
        except Exception as e:
            print(f"⚠️ Failed to load viral research: {e}")
            return ""
    
    async def generate_viral_script(self, 
                                  topic: str = "investing", 
                                  target_duration: int = 45,
                                  audience: str = "young professionals interested in wealth building") -> Dict[str, Any]:
        """
        Generate a viral script using AI with iterative quality improvement
        
        Args:
            topic: Main topic for the script
            target_duration: Target duration in seconds
            audience: Target audience description
            
        Returns:
            Dictionary with final script and generation metadata
        """
        print(f"\n🚀 STARTING VIRAL SCRIPT GENERATION")
        print(f"📝 Topic: {topic}")
        print(f"⏱️ Target Duration: {target_duration} seconds")
        print(f"👥 Audience: {audience}")
        print("=" * 80)
        
        generation_session = {
            "topic": topic,
            "target_duration": target_duration,
            "audience": audience,
            "attempts": [],
            "final_script": None,
            "final_score": 0,
            "total_attempts": 0,
            "started_at": datetime.now().isoformat(),
            "success": False
        }
        
        # Progressive quality improvement
        for threshold_index, target_score in enumerate(self.quality_thresholds):
            print(f"\n🎯 ATTEMPTING QUALITY THRESHOLD: {target_score}%")
            print(f"📊 Phase {threshold_index + 1}/4")
            
            success, script_data = await self._attempt_quality_threshold(
                topic, target_duration, audience, target_score, threshold_index
            )
            
            generation_session["attempts"].extend(script_data["attempts"])
            generation_session["total_attempts"] = len(generation_session["attempts"])
            
            if success:
                generation_session["final_script"] = script_data["best_script"]
                generation_session["final_score"] = script_data["best_score"]
                generation_session["success"] = True
                print(f"🎉 SUCCESS! Achieved {script_data['best_score']}% quality score!")
                break
            else:
                print(f"⚠️ Failed to reach {target_score}% threshold. Best: {script_data['best_score']}%")
        
        # If all thresholds failed, use the best attempt
        if not generation_session["success"] and generation_session["attempts"]:
            best_attempt = max(generation_session["attempts"], key=lambda x: x["score"])
            generation_session["final_script"] = best_attempt["script"]
            generation_session["final_score"] = best_attempt["score"]
            print(f"🔄 Using best attempt with {best_attempt['score']}% score")
        
        generation_session["completed_at"] = datetime.now().isoformat()
        
        # Save generation session for debugging
        self._save_generation_session(generation_session)
        
        print(f"\n✅ VIRAL SCRIPT GENERATION COMPLETE!")
        print(f"🎯 Final Score: {generation_session['final_score']}%")
        print(f"🔢 Total Attempts: {generation_session['total_attempts']}")
        print("=" * 80)
        
        return generation_session
    
    async def _attempt_quality_threshold(self, 
                                       topic: str, 
                                       target_duration: int, 
                                       audience: str, 
                                       target_score: int,
                                       phase: int) -> Tuple[bool, Dict[str, Any]]:
        """Attempt to reach a specific quality threshold"""
        
        attempts = []
        best_script = None
        best_score = 0
        previous_feedback = []
        
        print(f"🎭 Starting attempts for {target_score}% threshold...")
        
        for attempt in range(1, self.max_attempts + 1):
            print(f"\n🎬 ATTEMPT {attempt}/{self.max_attempts} (Target: {target_score}%)")
            
            # Generate script
            print("🤖 Generating script with AI...")
            script_result = await self._generate_single_script(
                topic, target_duration, audience, previous_feedback, attempt
            )
            
            if not script_result["success"]:
                print(f"❌ Script generation failed: {script_result['error']}")
                continue
            
            script = script_result["script"]
            print(f"📝 Generated script ({len(script.split())} words)")
            print(f"🎯 Hook: {script[:100]}...")
            
            # Rate script
            print("🔍 Rating script quality...")
            rating_result = await self._rate_script(script, topic, target_duration)
            
            if not rating_result["success"]:
                print(f"❌ Script rating failed: {rating_result['error']}")
                continue
            
            score = rating_result["score"]
            feedback = rating_result["feedback"]
            
            print(f"📊 SCORE: {score}%")
            print(f"💭 Feedback: {feedback[:150]}...")
            
            # Track attempt
            attempt_data = {
                "attempt_number": attempt,
                "phase": phase,
                "script": script,
                "score": score,
                "feedback": feedback,
                "word_count": len(script.split()),
                "hook": script[:100],
                "pattern_hash": self._get_pattern_hash(script),
                "generated_at": datetime.now().isoformat()
            }
            attempts.append(attempt_data)
            
            # Update best score
            if score > best_score:
                best_score = score
                best_script = script
                print(f"🏆 NEW BEST SCORE: {score}%!")
            
            # Check if target reached
            if score >= target_score:
                print(f"🎉 TARGET REACHED! {score}% >= {target_score}%")
                return True, {
                    "attempts": attempts,
                    "best_script": best_script,
                    "best_score": best_score
                }
            
            # Add feedback for next iteration
            previous_feedback.append({
                "attempt": attempt,
                "score": score,
                "feedback": feedback,
                "improvements_needed": rating_result.get("improvements", [])
            })
            
            print(f"⏭️ Continuing to next attempt...")
        
        print(f"⚠️ Failed to reach {target_score}% after {self.max_attempts} attempts")
        return False, {
            "attempts": attempts,
            "best_script": best_script,
            "best_score": best_score
        }
    
    async def _generate_single_script(self, 
                                    topic: str, 
                                    target_duration: int, 
                                    audience: str, 
                                    previous_feedback: List[Dict], 
                                    attempt_number: int) -> Dict[str, Any]:
        """Generate a single script using Gemini 2.0 Thinking"""
        
        try:
            # Build comprehensive prompt
            prompt = self._build_generation_prompt(
                topic, target_duration, audience, previous_feedback, attempt_number
            )
            
            print(f"🧠 Sending generation prompt to Gemini 2.0 Thinking...")
            print(f"📏 Prompt length: {len(prompt)} characters")
            
            response = await asyncio.to_thread(self.generator_model.generate_content, prompt)
            script = response.text.strip()
            
            # Clean up script
            script = self._clean_script(script)
            
            print(f"✅ Script generated successfully")
            print(f"📊 Script stats: {len(script)} chars, {len(script.split())} words")
            
            return {
                "success": True,
                "script": script,
                "attempt_number": attempt_number
            }
            
        except Exception as e:
            print(f"❌ Script generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "attempt_number": attempt_number
            }
    
    async def _rate_script(self, script: str, topic: str, target_duration: int) -> Dict[str, Any]:
        """Rate script quality using separate AI rater"""
        
        try:
            # Build rating prompt
            prompt = self._build_rating_prompt(script, topic, target_duration)
            
            print(f"🎯 Sending rating prompt to Gemini 2.0 Thinking...")
            
            response = await asyncio.to_thread(self.rater_model.generate_content, prompt)
            rating_text = response.text.strip()
            
            # Parse rating response
            rating_result = self._parse_rating_response(rating_text)
            
            print(f"✅ Script rated successfully")
            
            return {
                "success": True,
                **rating_result
            }
            
        except Exception as e:
            print(f"❌ Script rating error: {e}")
            return {
                "success": False,
                "error": str(e),
                "score": 0,
                "feedback": "Rating failed"
            }
    
    def _build_generation_prompt(self, 
                               topic: str, 
                               target_duration: int, 
                               audience: str, 
                               previous_feedback: List[Dict], 
                               attempt_number: int) -> str:
        """Build comprehensive prompt for script generation"""
        
        feedback_section = ""
        if previous_feedback:
            feedback_section = f"""
            
            **PREVIOUS ATTEMPTS & FEEDBACK:**
            You have made {len(previous_feedback)} previous attempts. Learn from this feedback:
            
            """
            for i, fb in enumerate(previous_feedback[-3:], 1):  # Last 3 attempts
                feedback_section += f"""
                Attempt {fb['attempt']}: Score {fb['score']}%
                Feedback: {fb['feedback']}
                Improvements Needed: {', '.join(fb.get('improvements_needed', []))}
                
                """
        
        variety_section = ""
        if self.used_patterns:
            variety_section = f"""
            
            **AVOID REPETITION:**
            You have used these patterns before. Create something DIFFERENT:
            - Used hooks: {', '.join(self.used_hooks[-5:])}
            - Used patterns: {', '.join(self.used_patterns[-5:])}
            """
        
        prompt = f"""
        You are a VIRAL CONTENT EXPERT creating YouTube Shorts scripts for "Wealthier Everyday" - a financial education channel.
        
        **MISSION:** Create a script that will go VIRAL and get millions of views while educating about {topic}.
        
        **CONSTRAINTS:**
        - Topic: {topic}
        - Target Duration: {target_duration} seconds (~{target_duration * 3} words at 3 words/second)
        - Audience: {audience}
        - Platform: YouTube Shorts (vertical video, max 60 seconds)
        - Attempt: #{attempt_number}
        
        **VIRAL RESEARCH DATA TO FOLLOW:**
        {self.viral_research}
        
        {feedback_section}
        {variety_section}
        
        **CRITICAL REQUIREMENTS:**
        1. **HOOK WITHIN 3 SECONDS**: Must stop scrolling immediately
        2. **EMOTIONAL PROGRESSION**: Hook → Problem → Agitation → Solution → Proof → Action
        3. **SPECIFIC NUMBERS**: Use exact statistics, percentages, dollar amounts
        4. **CONTRARIAN ANGLE**: Challenge common beliefs about {topic}
        5. **CALL TO ACTION**: Clear next step for viewers
        6. **RETENTION TACTICS**: Questions, cliffhangers, surprising facts
        7. **BRAND ALIGNMENT**: Focus on practical wealth building for young professionals
        
        **SCRIPT STRUCTURE:**
        - Seconds 0-3: VIRAL HOOK (question, contradiction, or shocking statement)
        - Seconds 3-15: PROBLEM/PAIN POINT (relatable struggle)
        - Seconds 15-25: AGITATION (make problem urgent/painful)
        - Seconds 25-35: SOLUTION (contrarian insight)
        - Seconds 35-40: PROOF (credibility/example)
        - Seconds 40-45: CALL TO ACTION (follow, engage, implement)
        
        Generate a script that will get MILLIONS of views. Be bold, specific, and contrarian.
        Return ONLY the script text, no explanations or formatting.
        """
        
        return prompt
    
    def _build_rating_prompt(self, script: str, topic: str, target_duration: int) -> str:
        """Build comprehensive prompt for script rating"""
        
        prompt = f"""
        You are a VIRAL CONTENT ANALYSIS EXPERT. Rate this YouTube Shorts script for viral potential.
        
        **SCRIPT TO ANALYZE:**
        "{script}"
        
        **CONTEXT:**
        - Topic: {topic}
        - Target Duration: {target_duration} seconds
        - Platform: YouTube Shorts
        - Channel: Wealthier Everyday (financial education)
        
        **VIRAL RESEARCH CRITERIA:**
        {self.viral_research}
        
        **RATING CRITERIA (Rate 0-100):**
        
        1. **HOOK STRENGTH (25 points):**
        - Stops scrolling within 3 seconds? 
        - Creates curiosity gap?
        - Uses proven viral patterns (question, contradiction, urgency)?
        - Specific numbers/statistics?
        
        2. **EMOTIONAL PROGRESSION (25 points):**
        - Clear problem → agitation → solution flow?
        - Relatable pain points?
        - Satisfying resolution?
        - Maintains engagement throughout?
        
        3. **CONTENT QUALITY (25 points):**
        - Contrarian/surprising insights?
        - Actionable advice?
        - Credible information?
        - Brand alignment with wealth building?
        
        4. **VIRAL MECHANICS (25 points):**
        - Encourages shares/comments?
        - Clear call to action?
        - Optimal length for retention?
        - Uses engagement tactics?
        
        **RESPONSE FORMAT:**
        Score: [0-100]
        
        Hook Analysis: [Detailed analysis of opening 3 seconds]
        
        Progression Analysis: [How well does emotional arc work]
        
        Viral Potential: [What makes this shareable or not]
        
        Improvements Needed: [Specific fixes to increase score]
        
        Example Fix: [Rewrite one section to show improvement]
        
        Provide detailed, actionable feedback to improve the script.
        """
        
        return prompt
    
    def _parse_rating_response(self, rating_text: str) -> Dict[str, Any]:
        """Parse AI rating response to extract score and feedback"""
        
        try:
            # Extract score
            score = 0
            lines = rating_text.split('\n')
            
            for line in lines:
                if line.startswith('Score:'):
                    score_text = line.replace('Score:', '').strip()
                    # Extract number from score text
                    import re
                    score_match = re.search(r'(\d+)', score_text)
                    if score_match:
                        score = int(score_match.group(1))
                    break
            
            # Extract improvements needed
            improvements = []
            in_improvements = False
            for line in lines:
                if 'Improvements Needed:' in line:
                    in_improvements = True
                    improvements.append(line.replace('Improvements Needed:', '').strip())
                elif in_improvements and line.strip():
                    if line.startswith('Example Fix:'):
                        break
                    improvements.append(line.strip())
            
            return {
                "score": score,
                "feedback": rating_text,
                "improvements": improvements
            }
            
        except Exception as e:
            print(f"⚠️ Failed to parse rating response: {e}")
            return {
                "score": 0,
                "feedback": rating_text,
                "improvements": []
            }
    
    def _clean_script(self, script: str) -> str:
        """Clean up generated script"""
        
        # Remove markdown formatting
        script = script.replace('```', '').replace('**', '')
        
        # Remove common AI prefixes
        prefixes_to_remove = [
            "Here's a viral script:",
            "Script:",
            "Here's the script:",
            "Viral script:"
        ]
        
        for prefix in prefixes_to_remove:
            if script.startswith(prefix):
                script = script[len(prefix):].strip()
        
        # Clean up extra whitespace
        script = ' '.join(script.split())
        
        return script
    
    def _get_pattern_hash(self, script: str) -> str:
        """Generate hash to track script patterns"""
        
        # Extract first 50 characters as pattern identifier
        pattern = script[:50].lower()
        return hashlib.md5(pattern.encode()).hexdigest()[:8]
    
    def _save_generation_session(self, session: Dict[str, Any]) -> None:
        """Save generation session for debugging"""
        
        try:
            os.makedirs("debug/script_generation", exist_ok=True)
            
            session_file = f"debug/script_generation/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(session_file, 'w') as f:
                json.dump(session, f, indent=2)
            
            print(f"💾 Generation session saved: {session_file}")
            
        except Exception as e:
            print(f"⚠️ Failed to save generation session: {e}")

# Test function for debugging
async def test_viral_script_generator():
    """Test the viral script generator"""
    
    generator = ViralScriptGeneratorNode()
    
    print("🧪 TESTING VIRAL SCRIPT GENERATOR")
    print("=" * 50)
    
    result = await generator.generate_viral_script(
        topic="passive income investing",
        target_duration=45,
        audience="millennials with 9-5 jobs who want financial freedom"
    )
    
    if result["success"] and result["final_script"]:
        print(f"\n🎉 FINAL SCRIPT (Score: {result['final_score']}%):")
        print("=" * 50)
        print(result["final_script"])
        print("=" * 50)
        print(f"📊 Generation took {result['total_attempts']} attempts")
    else:
        print("❌ Script generation failed")

if __name__ == "__main__":
    asyncio.run(test_viral_script_generator())
