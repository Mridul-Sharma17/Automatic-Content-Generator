#!/usr/bin/env python3
"""
Music Node - Fetches royalty-free background music from Openverse API
Provides instrumental and background music for video content
"""

import asyncio
import aiohttp
import logging
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import quote

logger = logging.getLogger(__name__)

class MusicNode:
    """Fetches and downloads royalty-free background music from Openverse"""
    
    def __init__(self):
        """Initialize the Music Node"""
        self.base_url = "https://api.openverse.org/v1"
        self.temp_dir = Path("temp/music")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
    async def search_background_music(self, 
                                    mood: str = "upbeat",
                                    genre: str = "instrumental", 
                                    duration_preference: str = "medium",
                                    content_theme: str = "business") -> List[Dict[str, Any]]:
        """
        Search for appropriate background music on Openverse
        
        Args:
            mood: Desired mood (upbeat, calm, energetic, professional, etc.)
            genre: Music genre preference (instrumental, electronic, ambient, etc.)
            duration_preference: Length preference (short, medium, long)
            content_theme: Content theme for context (business, education, lifestyle, etc.)
            
        Returns:
            List of music track metadata dictionaries
        """
        try:
            # Build search query with multiple relevant terms
            search_terms = [
                f"{mood} {genre}",
                f"background {genre}",
                f"{content_theme} music",
                "royalty free",
                "instrumental background"
            ]
            
            all_results = []
            
            async with aiohttp.ClientSession() as session:
                for search_term in search_terms[:3]:  # Limit to top 3 search terms
                    encoded_query = quote(search_term)
                    url = f"{self.base_url}/audio/?q={encoded_query}&length=medium&mature=false&page=1&page_size=20"
                    
                    logger.info(f"🎵 Searching Openverse for: {search_term}")
                    
                    try:
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                results = data.get('results', [])
                                logger.info(f"Found {len(results)} tracks for '{search_term}'")
                                all_results.extend(results)
                            else:
                                logger.warning(f"Openverse API returned status {response.status} for query: {search_term}")
                    except Exception as e:
                        logger.warning(f"Error searching for '{search_term}': {e}")
                        continue
            
            # Remove duplicates based on ID
            unique_results = []
            seen_ids = set()
            for result in all_results:
                track_id = result.get('id')
                if track_id and track_id not in seen_ids:
                    seen_ids.add(track_id)
                    unique_results.append(result)
            
            logger.info(f"✅ Found {len(unique_results)} unique music tracks")
            return unique_results[:10]  # Return top 10 tracks
            
        except Exception as e:
            logger.error(f"Error searching background music: {e}")
            return []
    
    def score_music_relevance(self, track: Dict[str, Any], 
                            mood: str, 
                            genre: str, 
                            content_theme: str) -> float:
        """
        Score music track relevance based on metadata
        
        Args:
            track: Track metadata from Openverse
            mood: Desired mood
            genre: Desired genre  
            content_theme: Content theme
            
        Returns:
            Relevance score (0-100)
        """
        score = 0.0
        
        # Get track metadata
        title = track.get('title', '').lower()
        description = track.get('description', '').lower()
        tags = [tag.get('name', '').lower() for tag in track.get('tags', [])]
        all_text = f"{title} {description} {' '.join(tags)}"
        
        # Mood matching (30 points)
        mood_keywords = {
            'upbeat': ['upbeat', 'energetic', 'positive', 'happy', 'bright', 'optimistic'],
            'calm': ['calm', 'peaceful', 'relaxing', 'soft', 'gentle', 'ambient'],
            'professional': ['corporate', 'business', 'clean', 'professional', 'modern'],
            'energetic': ['energetic', 'dynamic', 'powerful', 'driving', 'intense'],
            'inspiring': ['inspiring', 'motivational', 'uplifting', 'hopeful', 'emotional']
        }
        
        if mood.lower() in mood_keywords:
            for keyword in mood_keywords[mood.lower()]:
                if keyword in all_text:
                    score += 5.0
        
        # Genre matching (25 points)
        genre_keywords = {
            'instrumental': ['instrumental', 'background', 'ambient', 'cinematic'],
            'electronic': ['electronic', 'synth', 'digital', 'techno'],
            'acoustic': ['acoustic', 'guitar', 'piano', 'organic'],
            'orchestral': ['orchestral', 'classical', 'symphony', 'strings']
        }
        
        if genre.lower() in genre_keywords:
            for keyword in genre_keywords[genre.lower()]:
                if keyword in all_text:
                    score += 4.0
        
        # Content theme matching (20 points)
        theme_keywords = {
            'business': ['corporate', 'business', 'professional', 'presentation'],
            'education': ['educational', 'learning', 'tutorial', 'academic'],
            'lifestyle': ['lifestyle', 'daily', 'modern', 'contemporary'],
            'finance': ['corporate', 'business', 'professional', 'success']
        }
        
        if content_theme.lower() in theme_keywords:
            for keyword in theme_keywords[content_theme.lower()]:
                if keyword in all_text:
                    score += 3.0
        
        # Quality indicators (15 points)
        quality_keywords = ['royalty free', 'copyright free', 'creative commons', 'high quality', 'professional']
        for keyword in quality_keywords:
            if keyword in all_text:
                score += 3.0
        
        # Background music indicators (10 points) 
        background_keywords = ['background', 'underscore', 'backing', 'ambient']
        for keyword in background_keywords:
            if keyword in all_text:
                score += 2.5
        
        return min(score, 100.0)  # Cap at 100
    
    async def get_direct_audio_url(self, track: Dict[str, Any]) -> Optional[str]:
        """
        Get the direct audio download URL from Openverse track data
        
        Args:
            track: Track metadata from Openverse
            
        Returns:
            Direct download URL or None if not available
        """
        # Get the main URL which should be the direct audio link
        audio_url = track.get('url')
        
        # Validate that it looks like an audio URL
        if audio_url:
            audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac', 'mp32']
            if any(ext in audio_url.lower() for ext in audio_extensions):
                return audio_url
        
        # If no valid audio URL found, return None
        logger.warning(f"No valid audio URL found for track: {track.get('title', 'Unknown')}")
        return None

    async def download_music_track(self, track: Dict[str, Any], filename: Optional[str] = None) -> Optional[str]:
        """
        Download a music track from Openverse (with proper URL handling)
        
        Args:
            track: Track metadata with download URL
            filename: Optional custom filename
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            # Get the direct audio URL
            audio_url = await self.get_direct_audio_url(track)
            if not audio_url:
                return None
            
            # Generate safe filename
            if not filename:
                track_id = track.get('id', 'unknown')
                # Clean track ID for filename (remove problematic characters)
                safe_track_id = "".join(c for c in str(track_id) if c.isalnum() or c in '-_')[:20]
                filename = f"background_music_{safe_track_id}.mp3"
            
            file_path = self.temp_dir / filename
            
            title = track.get('title', 'Unknown')
            logger.info(f"🎵 Downloading: {title}")
            logger.debug(f"📁 URL: {audio_url}")
            
            # Download with proper timeout and error handling
            timeout = aiohttp.ClientTimeout(total=45)  # 45 second timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(audio_url, allow_redirects=True) as response:
                        if response.status == 200:
                            # Read the content
                            content = await response.read()
                            
                            # Validate minimum file size (avoid empty/error files)
                            if len(content) < 1024:  # Less than 1KB is suspicious
                                logger.warning(f"Downloaded file very small ({len(content)} bytes), skipping")
                                return None
                            
                            # Check content type if available
                            content_type = response.headers.get('content-type', '').lower()
                            if content_type and 'text/html' in content_type:
                                logger.warning(f"Received HTML content instead of audio, skipping")
                                return None
                            
                            # Save the file
                            with open(file_path, 'wb') as f:
                                f.write(content)
                            
                            file_size = len(content) / (1024 * 1024)  # Size in MB
                            logger.info(f"✅ Downloaded: {filename} ({file_size:.1f} MB)")
                            return str(file_path)
                            
                        else:
                            logger.warning(f"HTTP {response.status} for {audio_url}")
                            return None
                            
                except asyncio.TimeoutError:
                    logger.warning(f"Download timeout for {title}")
                    return None
                except Exception as e:
                    logger.warning(f"Download error for {title}: {e}")
            return None
                    
        except Exception as e:
            logger.error(f"Error downloading music track: {e}")
            return None
    
    async def fetch_background_music(self, 
                                   mood: str = "upbeat",
                                   genre: str = "instrumental",
                                   content_theme: str = "business",
                                   duration_preference: str = "medium") -> Optional[str]:
        """
        Main method to fetch and download appropriate background music
        
        Args:
            mood: Desired mood for the music
            genre: Music genre preference
            content_theme: Content theme for matching
            duration_preference: Length preference
            
        Returns:
            Path to downloaded music file or None if failed
        """
        try:
            logger.info(f"🎵 Fetching background music - Mood: {mood}, Genre: {genre}, Theme: {content_theme}")
            
            # Search for music tracks
            tracks = await self.search_background_music(mood, genre, duration_preference, content_theme)
            
            if not tracks:
                logger.warning("No music tracks found on Openverse")
                return None
            
            # Score and sort tracks by relevance
            scored_tracks = []
            for track in tracks:
                score = self.score_music_relevance(track, mood, genre, content_theme)
                scored_tracks.append((score, track))
            
            # Sort by score (highest first)
            scored_tracks.sort(key=lambda x: x[0], reverse=True)
            
            logger.info("🎯 Top music tracks by relevance:")
            for i, (score, track) in enumerate(scored_tracks[:5], 1):
                title = track.get('title', 'Unknown Title')
                logger.info(f"  {i}. {title} (Score: {score:.1f})")
            
            # Try to download the best tracks (try top 3 in case of download failures)
            for score, track in scored_tracks[:3]:
                title = track.get('title', 'Unknown Title')
                logger.info(f"🎵 Attempting to download: {title} (Score: {score:.1f})")
                
                downloaded_path = await self.download_music_track(track)
                if downloaded_path and os.path.exists(downloaded_path):
                    logger.info(f"✅ Successfully downloaded background music: {downloaded_path}")
                    return downloaded_path
                else:
                    logger.warning(f"Failed to download: {title}")
            
            logger.error("Failed to download any music tracks")
            return None
            
        except Exception as e:
            logger.error(f"Error in fetch_background_music: {e}")
            return None

# Test function for standalone testing
async def test_music_node():
    """Test the music node functionality"""
    print("🎵 Testing Music Node with Openverse API...")
    print("=" * 60)
    
    music_node = MusicNode()
    
    # Test cases
    test_cases = [
        {
            "mood": "upbeat",
            "genre": "instrumental", 
            "content_theme": "business",
            "description": "Business/Finance content"
        },
        {
            "mood": "calm",
            "genre": "ambient",
            "content_theme": "education", 
            "description": "Educational content"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['description']}")
        print("-" * 40)
        
        result = await music_node.fetch_background_music(
            mood=test_case["mood"],
            genre=test_case["genre"], 
            content_theme=test_case["content_theme"]
        )
        
        if result:
            print(f"✅ SUCCESS: Downloaded music to {result}")
            file_size = os.path.getsize(result) / (1024 * 1024)
            print(f"📁 File size: {file_size:.1f} MB")
        else:
            print("❌ FAILED: Could not download music")
    
    print("\n" + "=" * 60)
    print("🎵 Music Node testing completed!")

# Simple test function to examine Openverse API responses
async def test_openverse_api():
    """Test function to examine what Openverse actually returns"""
    print("🔍 Testing Openverse API responses...")
    
    import aiohttp
    import json
    from urllib.parse import quote
    
    search_term = "instrumental background"
    encoded_query = quote(search_term)
    url = f"https://api.openverse.org/v1/audio/?q={encoded_query}&page=1&page_size=5"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    
                    print(f"Found {len(results)} results")
                    
                    for i, track in enumerate(results[:3], 1):
                        print(f"\n--- Track {i} ---")
                        print(f"Title: {track.get('title', 'Unknown')}")
                        print(f"Creator: {track.get('creator', 'Unknown')}")
                        print(f"License: {track.get('license', 'Unknown')}")
                        print(f"URL: {track.get('url', 'No URL')}")
                        print(f"Foreign Landing URL: {track.get('foreign_landing_url', 'No foreign URL')}")
                        print(f"Detail URL: {track.get('detail_url', 'No detail URL')}")
                        print(f"Source: {track.get('source', 'Unknown')}")
                        print(f"File type: {track.get('filetype', 'Unknown')}")
                        print(f"Audio Set: {track.get('audio_set', {})}")
                        
                        # Check if there are any direct download links
                        audio_set = track.get('audio_set', {})
                        if audio_set:
                            print(f"Audio Set URLs: {audio_set}")
                else:
                    print(f"API returned status: {response.status}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run the full music node test
    asyncio.run(test_music_node())
