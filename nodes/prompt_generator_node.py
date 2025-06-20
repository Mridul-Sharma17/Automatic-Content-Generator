#!/usr/bin/env python3
"""
Prompt Generator Node - Creates optimized search queries for Pexels API
Generates primary and fallback search strategies for video fetching
"""

import sys
import os
import asyncio
from typing import List, Dict, Any

class PromptGeneratorNode:
    """Generates optimized search queries for video fetching"""
    
    def __init__(self):
        """Initialize the Prompt Generator"""
        print("🔍 Initializing Prompt Generator Node...")
        
        # Pexels category mappings for better search results
        self.category_mappings = {
            'business': ['business', 'office', 'professional', 'meeting', 'handshake'],
            'finance': ['money', 'finance', 'banking', 'investment', 'charts'],
            'real_estate': ['house', 'building', 'property', 'home', 'architecture'],
            'success': ['success', 'achievement', 'celebration', 'growth', 'winning'],
            'technology': ['computer', 'smartphone', 'technology', 'digital', 'data'],
            'lifestyle': ['lifestyle', 'people', 'living', 'modern', 'urban']
        }
        
        print("✅ Prompt Generator Node ready!")
    
    async def generate_search_queries(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate optimized search queries for each scene
        
        Args:
            scenes: List of scene dictionaries from scene analyzer
            
        Returns:
            List of search query dictionaries with primary/fallback strategies
        """
        print("🎯 Generating optimized search queries for video fetching...")
        
        search_queries = []
        
        for i, scene in enumerate(scenes):
            # Extract scene information
            keywords = scene.get('keywords', ['business', 'professional'])
            mood = scene.get('mood', 'professional')
            action_type = scene.get('action_type', 'talking_head')
            description = scene.get('description', '')
            
            # Generate primary query
            primary_query = self._create_primary_query(keywords, mood, action_type)
            
            # Generate fallback queries
            fallback_queries = self._create_fallback_queries(keywords, mood)
            
            # Classify content category
            category = self._classify_content_category(keywords, description)
            
            query_data = {
                "scene_id": i + 1,
                "scene_text": scene.get('text', ''),
                "primary_query": primary_query,
                "fallback_queries": fallback_queries,
                "category": category,
                "keywords": keywords,
                "mood": mood,
                "action_type": action_type,
                "search_strategy": "keyword_optimized"
            }
            
            search_queries.append(query_data)
            
            print(f"  🔍 Scene {i+1}: '{primary_query}' + {len(fallback_queries)} fallbacks")
        
        print(f"✅ Generated {len(search_queries)} optimized search strategies")
        return search_queries
    
    def _create_primary_query(self, keywords: List[str], mood: str, action_type: str) -> str:
        """Create the primary search query"""
        
        # Start with the most specific keyword
        primary_keyword = keywords[0] if keywords else 'business'
        
        # Add mood-based modifiers
        mood_modifiers = {
            'energetic': ['dynamic', 'active', 'vibrant'],
            'serious': ['professional', 'corporate', 'formal'],
            'motivational': ['inspiring', 'uplifting', 'positive'],
            'modern': ['contemporary', 'sleek', 'innovative']
        }
        
        modifier = mood_modifiers.get(mood, ['professional'])[0]
        
        # Create optimized query
        if action_type == 'talking_head':
            query = f"{modifier} {primary_keyword} person speaking"
        elif action_type == 'demonstration':
            query = f"{primary_keyword} demonstration tutorial"
        elif action_type == 'visualization':
            query = f"{modifier} {primary_keyword} concept visualization"
        else:
            query = f"{modifier} {primary_keyword} professional"
        
        return query
    
    def _create_fallback_queries(self, keywords: List[str], mood: str) -> List[str]:
        """Create fallback search queries"""
        
        fallback_queries = []
        
        # Use remaining keywords for fallbacks
        for keyword in keywords[1:4]:  # Use up to 3 additional keywords
            fallback_queries.append(f"professional {keyword}")
            fallback_queries.append(f"{keyword} business")
        
        # Add mood-based fallbacks
        mood_fallbacks = {
            'energetic': ['dynamic business', 'active professional', 'vibrant office'],
            'serious': ['corporate meeting', 'business formal', 'professional office'],
            'motivational': ['success achievement', 'growth progress', 'inspiring business'],
            'modern': ['contemporary office', 'modern business', 'sleek professional']
        }
        
        if mood in mood_fallbacks:
            fallback_queries.extend(mood_fallbacks[mood])
        
        # Generic high-quality fallbacks
        fallback_queries.extend([
            'professional business meeting',
            'modern office environment',
            'business success concept',
            'corporate professional'
        ])
        
        return fallback_queries[:8]  # Limit to 8 fallbacks
    
    def _classify_content_category(self, keywords: List[str], description: str) -> str:
        """Classify content into Pexels categories"""
        
        text_to_analyze = ' '.join(keywords + [description]).lower()
        
        # Check for specific categories
        if any(word in text_to_analyze for word in ['money', 'invest', 'finance', 'bank']):
            return 'finance'
        elif any(word in text_to_analyze for word in ['real estate', 'property', 'house', 'building']):
            return 'real_estate'
        elif any(word in text_to_analyze for word in ['tech', 'computer', 'digital', 'app']):
            return 'technology'
        elif any(word in text_to_analyze for word in ['success', 'achieve', 'goal', 'win']):
            return 'success'
        elif any(word in text_to_analyze for word in ['lifestyle', 'life', 'people', 'personal']):
            return 'lifestyle'
        else:
            return 'business'

# Test function
async def test_prompt_generator():
    """Test the prompt generator with sample scenes"""
    print("🧪 Testing Prompt Generator Node...")
    
    # Sample scenes data
    test_scenes = [
        {
            "scene_number": 1,
            "text": "Did you know that 90% of millionaires invest in real estate?",
            "keywords": ["real estate", "millionaire", "investment"],
            "mood": "serious",
            "action_type": "talking_head"
        },
        {
            "scene_number": 2,
            "text": "Property investment provides passive income through rental payments",
            "keywords": ["property", "income", "rental"],
            "mood": "professional",
            "action_type": "visualization"
        }
    ]
    
    generator = PromptGeneratorNode()
    queries = await generator.generate_search_queries(test_scenes)
    
    print(f"\n✅ Test complete! Generated {len(queries)} search strategies:")
    for query in queries:
        print(f"  🎯 Scene {query['scene_id']}: {query['primary_query']}")

if __name__ == "__main__":
    asyncio.run(test_prompt_generator())