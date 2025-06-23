#!/usr/bin/env python3
"""
Enhanced Prompt Generator for Wealthier Everyday Financial Content
Creates brand-aware, context-rich search queries optimized for financial education videos
Focuses on aspirational, actionable, and engaging visual storytelling for wealth building content
"""

import sys
import os
import asyncio
from typing import List, Dict, Any

class PromptGeneratorNode:
    """
    Intelligent prompt generator for Wealthier Everyday financial education content.
    Creates contextually-aware search queries that align with brand identity and content goals.
    """
    
    def __init__(self):
        """Initialize the Enhanced Prompt Generator with full project context"""
        print("🔍 Initializing Enhanced Prompt Generator for Wealthier Everyday...")
        
        # PROJECT CONTEXT - Wealthier Everyday Brand Identity
        self.brand_context = {
            "name": "Wealthier Everyday",
            "mission": "Practical financial education for building wealth and financial freedom",
            "audience": "Young professionals, millennials, Gen Z interested in wealth building",
            "tone": "Inspiring, actionable, accessible, aspirational",
            "visual_style": "Modern, diverse, dynamic, growth-oriented, professional yet relatable"
        }
        
        # CONTENT GOALS for YouTube Shorts
        self.content_goals = {
            "primary": "Educate viewers about wealth building and smart investing",
            "engagement": "Create viral, high-retention content that motivates action",
            "emotional_arc": "Problem → Solution → Inspiration → Call to Action",
            "visual_focus": "Progress, growth, success, accessibility, modern lifestyle"
        }
        
        # FINANCIAL CONCEPT VISUAL MAPPINGS
        self.financial_concept_visuals = {
            # Core Investment Concepts
            "investing": ["upward trending graph", "planting seeds growing", "building blocks stacking", "mountain climbing success"],
            "compound_interest": ["snowball effect rolling", "tree growing exponentially", "staircase ascending infinite", "rocket launching upward"],
            "wealth_building": ["skyscraper construction timelapse", "golden coins multiplying stack", "ladder climbing success story", "bridge building connection"],
            "passive_income": ["water flowing stream continuous", "solar panels generating energy", "rent collection modern apartment", "dividend checks arriving mailbox"],
            "financial_freedom": ["bird flying open sky", "keys unlocking golden door", "person walking beach sunset", "mountain peak achievement view"],
            
            # Investment Vehicles
            "real_estate": ["modern apartment building exterior", "house keys handover ceremony", "property value rising chart", "rental income calculation"],
            "stocks": ["stock market green arrows", "portfolio diversification display", "trading floor energy buzz", "dividend growth visualization"],
            "savings": ["piggy bank gold coins", "emergency fund safety net", "bank account growing numbers", "financial security peace mind"],
            
            # Financial Behaviors
            "start_investing": ["finger pressing start button", "first step journey path", "seed planting rich soil", "door opening bright future"],
            "money_growth": ["plant growing time lapse", "graph exponential curve up", "wealth accumulation visual", "success celebration achievement"],
            "beat_inflation": ["arrow piercing through barrier", "runner overtaking competitor", "shield protecting value", "growth outpacing decline"],
            
            # Aspirational Lifestyle
            "financial_success": ["young professional celebrating", "modern office success story", "diverse team winning together", "achievement milestone reached"],
            "future_wealth": ["sunrise over city skyline", "horizon golden opportunity", "pathway leading success", "vision board dreams reality"],
            "smart_decisions": ["crossroads choosing right path", "lightbulb moment inspiration", "puzzle pieces fitting together", "strategy planning success"]
        }
        
        # EMOTIONAL TONE VISUAL MAPPINGS
        self.emotional_tone_visuals = {
            "motivational": ["athlete crossing finish line", "mountain peak conquer flag", "sunrise new beginning hope", "person raising arms victory"],
            "educational": ["teacher explaining concept clearly", "infographic visual learning", "lightbulb understanding moment", "book knowledge gaining wisdom"],
            "aspirational": ["luxury lifestyle achievable dream", "success story inspiration", "goal achievement celebration", "dream home becoming reality"],
            "urgent": ["clock ticking time importance", "opportunity door closing", "train departing station", "limited time action needed"],
            "reassuring": ["safe secure vault protection", "professional advisor guidance", "steady hands building future", "confidence trust reliability"],
            "exciting": ["rocket launch exponential growth", "celebration success achievement", "breakthrough moment discovery", "energy dynamic movement forward"]
        }
        
        # TARGET DEMOGRAPHIC PREFERENCES
        self.demographic_preferences = {
            "age_group": "25-40 years old",
            "representation": "diverse, inclusive, modern professionals",
            "settings": "urban environments, modern offices, contemporary homes",
            "technology": "smartphones, laptops, modern apps, digital interfaces",
            "lifestyle": "work-life balance, career growth, lifestyle improvement"
        }
        
        print("✅ Enhanced Prompt Generator ready with full brand context!")
    
    async def generate_search_queries(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate brand-aware, contextually rich search queries for each scene
        
        Args:
            scenes: List of scene dictionaries from scene analyzer
            
        Returns:
            List of enhanced search query dictionaries with intelligent visual strategies
        """
        print("🎯 Generating enhanced search queries for Wealthier Everyday content...")
        
        search_queries = []
        total_scenes = len(scenes)
        
        for i, scene in enumerate(scenes):
            # Extract scene information
            keywords = scene.get('keywords', ['investing', 'wealth'])
            mood = scene.get('mood', 'motivational')
            action_type = scene.get('action_type', 'visualization')
            description = scene.get('description', '')
            scene_text = scene.get('text', '')
            
            # ENHANCED CONTEXT ANALYSIS
            narrative_position = self._analyze_narrative_position(i, total_scenes)
            financial_concepts = self._extract_financial_concepts(scene_text, keywords)
            emotional_intent = self._determine_emotional_intent(scene_text, mood, narrative_position)
            target_energy = self._determine_energy_level(narrative_position, scene_text)
            
            # INTELLIGENT QUERY GENERATION
            primary_query = self._create_context_aware_query(
                scene_text, financial_concepts, emotional_intent, target_energy
            )
            
            # STRATEGIC FALLBACK SYSTEM
            fallback_queries = self._create_intelligent_fallbacks(
                financial_concepts, emotional_intent, keywords, narrative_position
            )
            
            # BRAND-ALIGNED CATEGORY CLASSIFICATION
            content_category = self._classify_financial_content(scene_text, keywords)
            
            # VISUAL STRATEGY SELECTION
            visual_strategy = self._select_visual_strategy(
                financial_concepts, emotional_intent, narrative_position
            )
            
            query_data = {
                "scene_id": i + 1,
                "scene_text": scene_text,
                "primary_query": primary_query,
                "fallback_queries": fallback_queries,
                "content_category": content_category,
                "visual_strategy": visual_strategy,
                "keywords": keywords,
                "mood": mood,
                "action_type": action_type,
                "narrative_position": narrative_position,
                "financial_concepts": financial_concepts,
                "emotional_intent": emotional_intent,
                "target_energy": target_energy,
                "brand_context": {
                    "channel": "Wealthier Everyday",
                    "content_type": "Financial Education",
                    "target_audience": self.demographic_preferences["age_group"],
                    "visual_style": self.brand_context["visual_style"]
                }
            }
            
            search_queries.append(query_data)
            
            print(f"  🎯 Scene {i+1}/{total_scenes}: '{primary_query}' ({emotional_intent}, {target_energy})")
            print(f"     💡 Concepts: {', '.join(financial_concepts)}")
        
        print(f"✅ Generated {len(search_queries)} enhanced brand-aware search strategies")
        return search_queries
    
    def _analyze_narrative_position(self, scene_index: int, total_scenes: int) -> str:
        """Analyze where this scene falls in the narrative arc"""
        position_ratio = scene_index / max(total_scenes - 1, 1)
        
        if position_ratio <= 0.25:
            return "hook"  # Opening, grab attention
        elif position_ratio <= 0.5:
            return "problem"  # Present the challenge/need
        elif position_ratio <= 0.75:
            return "solution"  # Explain the solution
        else:
            return "call_to_action"  # Motivate action
    
    def _extract_financial_concepts(self, scene_text: str, keywords: List[str]) -> List[str]:
        """Extract specific financial concepts from scene content"""
        text_lower = scene_text.lower()
        all_terms = text_lower + ' ' + ' '.join(keywords).lower()
        
        detected_concepts = []
        
        # Check for financial concepts
        for concept, patterns in self.financial_concept_visuals.items():
            # Create search terms for this concept
            concept_terms = concept.replace('_', ' ').split()
            
            # Check if concept terms appear in text
            if any(term in all_terms for term in concept_terms):
                detected_concepts.append(concept)
            
            # Check for specific patterns
            if concept == "investing" and any(word in all_terms for word in ["invest", "investment", "portfolio"]):
                detected_concepts.append(concept)
            elif concept == "compound_interest" and any(word in all_terms for word in ["compound", "exponential", "grow over time"]):
                detected_concepts.append(concept)
            elif concept == "wealth_building" and any(word in all_terms for word in ["build wealth", "financial future", "long term"]):
                detected_concepts.append(concept)
            elif concept == "passive_income" and any(word in all_terms for word in ["passive", "rental", "dividend"]):
                detected_concepts.append(concept)
            elif concept == "financial_freedom" and any(word in all_terms for word in ["financial freedom", "independence", "secure"]):
                detected_concepts.append(concept)
        
        # If no specific concepts detected, infer from keywords
        if not detected_concepts:
            if any(word in all_terms for word in ["money", "invest", "wealth", "financial"]):
                detected_concepts.append("investing")
            if any(word in all_terms for word in ["grow", "future", "time"]):
                detected_concepts.append("wealth_building")
        
        return detected_concepts[:3]  # Limit to top 3 concepts
    
    def _determine_emotional_intent(self, scene_text: str, mood: str, narrative_position: str) -> str:
        """Determine the emotional intent based on content and position"""
        text_lower = scene_text.lower()
        
        # Check for emotional indicators in text
        if any(word in text_lower for word in ["did you know", "secret", "surprising"]):
            return "educational"
        elif any(word in text_lower for word in ["start", "begin", "today", "now"]):
            return "urgent"
        elif any(word in text_lower for word in ["grow", "build", "achieve", "success"]):
            return "aspirational"
        elif any(word in text_lower for word in ["safe", "secure", "protect"]):
            return "reassuring"
        elif any(word in text_lower for word in ["exciting", "amazing", "incredible"]):
            return "exciting"
        
        # Use narrative position as fallback
        position_emotion_map = {
            "hook": "exciting",
            "problem": "educational", 
            "solution": "aspirational",
            "call_to_action": "motivational"
        }
        
        return position_emotion_map.get(narrative_position, "motivational")
    
    def _determine_energy_level(self, narrative_position: str, scene_text: str) -> str:
        """Determine the energy level needed for this scene"""
        text_lower = scene_text.lower()
        
        # High energy indicators
        if any(word in text_lower for word in ["start", "begin", "action", "now", "today"]):
            return "high_energy"
        elif any(word in text_lower for word in ["grow", "build", "achieve", "success"]):
            return "medium_energy"
        else:
            return "calm_professional"
    
    def _create_context_aware_query(self, scene_text: str, financial_concepts: List[str], 
                                   emotional_intent: str, target_energy: str) -> str:
        """Create intelligent, context-aware search query"""
        text_lower = scene_text.lower()
        
        # SPECIFIC FINANCIAL CONTENT ANALYSIS
        if "money sit idle" in text_lower or "sitting idle" in text_lower:
            return "cash pile sitting still motionless stagnant money"
        elif "build wealth" in text_lower or "building wealth" in text_lower:
            return "skyscraper construction growing upward success building"
        elif "beat inflation" in text_lower or "beating inflation" in text_lower:
            return "arrow breaking through red barrier growth winning"
        elif "compound" in text_lower and ("return" in text_lower or "interest" in text_lower):
            return "snowball effect exponential growth rolling bigger"
        elif "start invest" in text_lower or "begin invest" in text_lower:
            return "person pressing green start button beginning journey"
        elif "financial future" in text_lower or "secure future" in text_lower:
            return "bright golden sunrise horizon new beginning hope"
        elif "passive income" in text_lower:
            return "money flowing stream continuous rental income"
        elif "real estate" in text_lower:
            return "modern apartment building investment property success"
        elif "portfolio" in text_lower or "diversif" in text_lower:
            return "multiple investment charts growing portfolio balance"
        elif "single step" in text_lower or "first step" in text_lower:
            return "foot taking first step path journey beginning"
        elif "grow over time" in text_lower or "time" in text_lower and "grow" in text_lower:
            return "plant growing timelapse seeds to tree success"
        elif "smart investment" in text_lower or "smart money" in text_lower:
            return "lightbulb idea moment intelligent decision making"
        elif "opportunity" in text_lower:
            return "door opening bright future golden opportunities"
        elif "millionaire" in text_lower or "wealthy" in text_lower:
            return "successful professional celebrating achievement wealth"
        elif "today" in text_lower and ("start" in text_lower or "begin" in text_lower):
            return "calendar today date circled action starting now"
        
        # CONCEPT-BASED QUERIES
        if financial_concepts:
            primary_concept = financial_concepts[0]
            if primary_concept in self.financial_concept_visuals:
                visual_options = self.financial_concept_visuals[primary_concept]
                
                # Select based on emotional intent
                if emotional_intent == "exciting" and len(visual_options) > 3:
                    return visual_options[3]  # Most dynamic option
                elif emotional_intent == "aspirational" and len(visual_options) > 1:
                    return visual_options[1]  # Growth-focused option
                else:
                    return visual_options[0]  # Primary option
        
        # EMOTIONAL INTENT FALLBACK
        if emotional_intent in self.emotional_tone_visuals:
            emotional_visuals = self.emotional_tone_visuals[emotional_intent]
            return emotional_visuals[0]
        
        # ULTIMATE FALLBACK - Brand-appropriate financial visuals
        return "upward trending graph success financial growth investment"
    
    def _create_intelligent_fallbacks(self, financial_concepts: List[str], 
                                     emotional_intent: str, keywords: List[str], 
                                     narrative_position: str) -> List[str]:
        """Create strategic fallback queries based on context"""
        
        fallback_queries = []
        
        # CONCEPT-BASED FALLBACKS
        for concept in financial_concepts[:2]:  # Use top 2 concepts
            if concept in self.financial_concept_visuals:
                visuals = self.financial_concept_visuals[concept]
                # Add different visual options for the same concept
                fallback_queries.extend(visuals[1:3])  # Skip the primary one
        
        # EMOTIONAL TONE FALLBACKS
        if emotional_intent in self.emotional_tone_visuals:
            emotional_visuals = self.emotional_tone_visuals[emotional_intent]
            fallback_queries.extend(emotional_visuals[1:3])
        
        # NARRATIVE POSITION FALLBACKS
        position_fallbacks = {
            "hook": ["attention grabbing visual surprise", "eye catching dynamic movement", "compelling visual statement"],
            "problem": ["frustrated person money problems", "challenging financial situation", "concern worry financial stress"],
            "solution": ["lightbulb moment understanding clarity", "solution discovery breakthrough", "path forward clear direction"],
            "call_to_action": ["person taking action decisively", "starting journey first step", "motivated individual beginning"]
        }
        
        if narrative_position in position_fallbacks:
            fallback_queries.extend(position_fallbacks[narrative_position])
        
        # BRAND-SPECIFIC FALLBACKS (Wealthier Everyday)
        brand_fallbacks = [
            "young professional financial success story",
            "modern diverse people achieving goals",
            "aspirational lifestyle financial freedom",
            "millennial generation building wealth",
            "contemporary office financial planning",
            "smart money decisions young adults",
            "investment growth success celebration",
            "financial education learning moment"
        ]
        fallback_queries.extend(brand_fallbacks[:3])
        
        # KEYWORD-BASED FALLBACKS (Enhanced)
        for keyword in keywords[:3]:
            fallback_queries.append(f"professional {keyword} success story")
            fallback_queries.append(f"modern {keyword} achievement")
        
        # Remove duplicates and limit
        unique_fallbacks = list(dict.fromkeys(fallback_queries))
        return unique_fallbacks[:10]  # Limit to 10 strategic fallbacks
    
    def _classify_financial_content(self, scene_text: str, keywords: List[str]) -> str:
        """Classify content into financial education categories"""
        
        text_to_analyze = ' '.join([scene_text] + keywords).lower()
        
        # Specific financial categories
        if any(word in text_to_analyze for word in ['real estate', 'property', 'rental', 'house']):
            return 'real_estate_investing'
        elif any(word in text_to_analyze for word in ['stock', 'share', 'portfolio', 'dividend']):
            return 'stock_market_investing'
        elif any(word in text_to_analyze for word in ['save', 'saving', 'emergency', 'fund']):
            return 'personal_savings'
        elif any(word in text_to_analyze for word in ['retire', 'retirement', '401k', 'pension']):
            return 'retirement_planning'
        elif any(word in text_to_analyze for word in ['budget', 'expense', 'spending', 'debt']):
            return 'personal_finance'
        elif any(word in text_to_analyze for word in ['passive', 'income', 'stream', 'rental']):
            return 'passive_income'
        elif any(word in text_to_analyze for word in ['compound', 'interest', 'exponential', 'growth']):
            return 'compound_growth'
        elif any(word in text_to_analyze for word in ['start', 'begin', 'first', 'young']):
            return 'getting_started'
        elif any(word in text_to_analyze for word in ['wealthy', 'rich', 'millionaire', 'success']):
            return 'wealth_building'
        else:
            return 'general_investing'
    
    def _select_visual_strategy(self, financial_concepts: List[str], 
                               emotional_intent: str, narrative_position: str) -> str:
        """Select the optimal visual strategy for this scene"""
        
        # Strategy matrix based on content and position
        if narrative_position == "hook":
            if emotional_intent == "exciting":
                return "high_impact_attention_grabber"
            else:
                return "compelling_visual_statement"
        
        elif narrative_position == "problem":
            if "financial_freedom" in financial_concepts:
                return "aspirational_contrast"
            else:
                return "relatable_challenge_presentation"
        
        elif narrative_position == "solution":
            if emotional_intent == "aspirational":
                return "inspiring_transformation_visual"
            else:
                return "clear_solution_demonstration"
        
        else:  # call_to_action
            if emotional_intent == "urgent":
                return "immediate_action_motivation"
            else:
                return "empowering_next_step_visual"

# Enhanced Test function
async def test_prompt_generator():
    """Test the enhanced prompt generator with Wealthier Everyday content"""
    print("🧪 Testing Enhanced Prompt Generator for Wealthier Everyday...")
    
    # Sample scenes from actual financial education content
    test_scenes = [
        {
            "scene_number": 1,
            "text": "Investing is the key to building wealth and securing your financial future.",
            "keywords": ["investing", "wealth", "financial future"],
            "mood": "motivational",
            "action_type": "talking_head"
        },
        {
            "scene_number": 2,
            "text": "Instead of letting your money sit idle, smart investments help your savings grow over time.",
            "keywords": ["money", "investments", "savings", "growth"],
            "mood": "educational", 
            "action_type": "visualization"
        },
        {
            "scene_number": 3,
            "text": "The earlier you invest, the more you benefit from compounding returns.",
            "keywords": ["invest", "compounding", "returns"],
            "mood": "aspirational",
            "action_type": "visualization"
        },
        {
            "scene_number": 4,
            "text": "Start investing today for a wealthier tomorrow!",
            "keywords": ["start", "investing", "today"],
            "mood": "urgent",
            "action_type": "call_to_action"
        }
    ]
    
    generator = PromptGeneratorNode()
    queries = await generator.generate_search_queries(test_scenes)
    
    print(f"\n✅ Enhanced Test Complete! Generated {len(queries)} intelligent search strategies:")
    print(f"📊 Brand Context: {generator.brand_context['name']} - {generator.brand_context['mission']}")
    print(f"🎯 Target Audience: {generator.demographic_preferences['age_group']}")
    
    for query in queries:
        print(f"\n� Scene {query['scene_id']}: {query['narrative_position'].upper()}")
        print(f"   💭 Text: {query['scene_text'][:60]}...")
        print(f"   🎯 Primary Query: '{query['primary_query']}'")
        print(f"   🧠 Concepts: {', '.join(query['financial_concepts'])}")
        print(f"   💫 Intent: {query['emotional_intent']} | Energy: {query['target_energy']}")
        print(f"   📂 Category: {query['content_category']}")
        print(f"   🎨 Strategy: {query['visual_strategy']}")
        print(f"   🔄 Fallbacks: {len(query['fallback_queries'])} strategic alternatives")

if __name__ == "__main__":
    asyncio.run(test_prompt_generator())