"""
Video Fetcher Node - Semantic Video Selection with Pixabay API

This node searches for and selects the most relevant stock videos using Pixabay's API,
which provides rich semantic metadata (tags, categories) for intelligent video selection.
Pixabay offers superior content curation compared to Pexels.
"""

import requests
import os
import random
import logging
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_semantic_score(video: Dict, keywords: List[str], prompt: str) -> float:
    """
    Calculate a comprehensive semantic relevance score for a video.
    Uses Pixabay's tags, popularity metrics, and technical specs.
    
    Returns score from 0-100 where 100 is perfect match.
    """
    score = 0.0
    
    # Extract video metadata
    tags = video.get('tags', '').lower().split(', ') if video.get('tags') else []
    page_url = video.get('pageURL', '').lower()
    video_type = video.get('type', '').lower()
    duration = video.get('duration', 0)
    views = video.get('views', 0)
    downloads = video.get('downloads', 0) 
    likes = video.get('likes', 0)
    
    logger.info(f"Scoring video {video.get('id')}: tags={tags}, type={video_type}, duration={duration}s")
    
    # 1. TAG MATCHING (40% of score) - Most important for semantic relevance
    tag_score = 0.0
    if tags and tags != ['']:
        keyword_matches = 0
        for keyword in keywords:
            keyword = keyword.lower().strip()
            for tag in tags:
                tag = tag.strip()
                if keyword in tag or tag in keyword:
                    keyword_matches += 1
                    logger.info(f"Tag match: '{keyword}' <-> '{tag}'")
                elif SequenceMatcher(None, keyword, tag).ratio() > 0.7:
                    keyword_matches += 0.5
                    logger.info(f"Fuzzy tag match: '{keyword}' <-> '{tag}' (ratio: {SequenceMatcher(None, keyword, tag).ratio():.2f})")
        
        tag_score = min(keyword_matches / len(keywords) * 100, 40.0)
        logger.info(f"Tag score: {tag_score:.1f}/40.0 ({keyword_matches} matches)")
    
    score += tag_score
    
    # 2. PROMPT RELEVANCE (25% of score) - Semantic matching against full prompt
    prompt_score = 0.0
    prompt_lower = prompt.lower()
    
    # Check tags against full prompt
    for tag in tags:
        if tag and tag in prompt_lower:
            prompt_score += 5.0
    
    # Check if video type matches prompt context
    if any(word in prompt_lower for word in ['animation', 'cartoon', 'animated']) and video_type == 'animation':
        prompt_score += 5.0
    elif video_type == 'film':
        prompt_score += 2.0
        
    prompt_score = min(prompt_score, 25.0)
    logger.info(f"Prompt relevance score: {prompt_score:.1f}/25.0")
    score += prompt_score
    
    # 3. POPULARITY & QUALITY (20% of score) - Community validation
    quality_score = 0.0
    
    # Normalize metrics (use log scale for very high numbers)
    import math
    view_score = min(math.log10(max(views, 1)) * 2.0, 10.0)
    download_score = min(math.log10(max(downloads, 1)) * 3.0, 8.0) 
    like_score = min(math.log10(max(likes, 1)) * 4.0, 2.0)
    
    quality_score = view_score + download_score + like_score
    logger.info(f"Quality score: {quality_score:.1f}/20.0 (views: {views}, downloads: {downloads}, likes: {likes})")
    score += quality_score
    
    # 4. TECHNICAL SPECS (15% of score) - Duration and format suitability
    tech_score = 0.0
    
    # Duration scoring - prefer 5-30 second clips for YouTube Shorts
    if 5 <= duration <= 30:
        tech_score += 10.0
    elif 3 <= duration <= 60:
        tech_score += 7.0
    elif duration < 3:
        tech_score += 2.0  # Too short
    else:
        tech_score += 4.0  # Too long but usable
        
    # Video format preference (film > animation for most content)
    if video_type == 'film':
        tech_score += 5.0
    elif video_type == 'animation':
        tech_score += 3.0
        
    logger.info(f"Technical score: {tech_score:.1f}/15.0 (duration: {duration}s, type: {video_type})")
    score += tech_score
    
    # FINAL SCORE CALCULATION
    final_score = min(score, 100.0)
    logger.info(f"Final score for video {video.get('id')}: {final_score:.1f}/100.0")
    
    return final_score


def search_pixabay_videos(keywords: List[str], prompt: str, limit: int = 20) -> List[Dict]:
    """
    Search Pixabay for videos using multiple strategies and semantic keywords.
    
    Args:
        keywords: List of search keywords/phrases
        prompt: Original prompt for context
        limit: Maximum number of videos to return
    
    Returns:
        List of video objects with metadata
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
        PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
        
        if not PIXABAY_API_KEY or PIXABAY_API_KEY == "your_pixabay_api_key_here":
            logger.error("Pixabay API key not configured")
            return []
            
        all_videos = []
        seen_ids = set()
        
        # Try different search strategies
        search_queries = []
        
        # 1. Individual keywords
        for keyword in keywords[:3]:  # Top 3 keywords
            search_queries.append(keyword.strip())
            
        # 2. Keyword combinations
        if len(keywords) >= 2:
            search_queries.append(f"{keywords[0]} {keywords[1]}")
            
        # 3. Extract category-relevant terms from prompt
        categories = ['nature', 'business', 'technology', 'people', 'education', 
                     'health', 'travel', 'food', 'sports', 'music', 'science']
        for category in categories:
            if category in prompt.lower():
                search_queries.append(category)
                break
        
        logger.info(f"Pixabay search queries: {search_queries}")
        
        for query in search_queries:
            try:
                # Pixabay Video API parameters
                params = {
                    'key': PIXABAY_API_KEY,
                    'q': query,
                    'video_type': 'all',  # all, film, animation
                    'min_duration': 3,
                    'safesearch': 'true',
                    'order': 'popular',  # popular, latest
                    'per_page': min(20, 200),  # API max is 200
                    'page': 1
                }
                
                logger.info(f"Searching Pixabay for: '{query}'")
                response = requests.get(
                    'https://pixabay.com/api/videos/',
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                
                data = response.json()
                videos = data.get('hits', [])
                
                logger.info(f"Pixabay returned {len(videos)} videos for '{query}'")
                
                for video in videos:
                    video_id = video.get('id')
                    if video_id not in seen_ids:
                        seen_ids.add(video_id)
                        all_videos.append(video)
                        
                        # Log video details for debugging
                        tags = video.get('tags', 'No tags')
                        duration = video.get('duration', 0)
                        logger.info(f"Found video {video_id}: tags='{tags}', duration={duration}s")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error searching Pixabay for '{query}': {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error searching Pixabay for '{query}': {e}")
                continue
        
        logger.info(f"Total unique videos found: {len(all_videos)}")
        return all_videos[:limit]
        
    except Exception as e:
        logger.error(f"Failed to search Pixabay videos: {e}")
        return []


def select_best_videos(videos: List[Dict], keywords: List[str], prompt: str, count: int = 5) -> List[Dict]:
    """
    Select the best videos from search results using semantic scoring.
    
    Args:
        videos: List of video objects from Pixabay
        keywords: Search keywords for relevance scoring
        prompt: Original prompt for context
        count: Number of videos to select
    
    Returns:
        List of best videos sorted by relevance score
    """
    if not videos:
        logger.warning("No videos to select from")
        return []
    
    logger.info(f"Scoring {len(videos)} videos for selection...")
    
    # Score all videos
    scored_videos = []
    for video in videos:
        try:
            score = calculate_semantic_score(video, keywords, prompt)
            scored_videos.append((score, video))
        except Exception as e:
            logger.error(f"Error scoring video {video.get('id', 'unknown')}: {e}")
            continue
    
    # Sort by score (highest first)
    scored_videos.sort(key=lambda x: x[0], reverse=True)
    
    # Log top results
    logger.info("Top scored videos:")
    for i, (score, video) in enumerate(scored_videos[:min(10, len(scored_videos))]):
        video_id = video.get('id', 'unknown')
        tags = video.get('tags', 'No tags')
        duration = video.get('duration', 0)
        logger.info(f"  #{i+1}: Video {video_id} - Score: {score:.1f} - Tags: '{tags}' - Duration: {duration}s")
    
    # Return top videos
    selected = [video for score, video in scored_videos[:count]]
    logger.info(f"Selected {len(selected)} videos with scores: {[score for score, _ in scored_videos[:count]]}")
    
    return selected


def get_video_download_url(video: Dict, preferred_quality: str = 'medium') -> Optional[str]:
    """
    Extract the best download URL from Pixabay video object.
    
    Args:
        video: Pixabay video object
        preferred_quality: 'large', 'medium', 'small', 'tiny'
    
    Returns:
        Video download URL or None
    """
    try:
        videos_data = video.get('videos', {})
        
        # Quality preference order
        quality_order = [preferred_quality, 'medium', 'small', 'large', 'tiny']
        
        for quality in quality_order:
            if quality in videos_data:
                video_info = videos_data[quality]
                url = video_info.get('url')
                if url:
                    width = video_info.get('width', 0)
                    height = video_info.get('height', 0)
                    size = video_info.get('size', 0)
                    
                    logger.info(f"Selected {quality} quality: {width}x{height}, {size/1024/1024:.1f}MB")
                    return url
        
        logger.warning(f"No suitable video quality found for video {video.get('id')}")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting video URL: {e}")
        return None


def download_video(url: str, filename: str, max_retries: int = 3) -> bool:
    """
    Download video from URL with retry logic.
    
    Args:
        url: Video download URL
        filename: Local filename to save to
        max_retries: Maximum number of download attempts
    
    Returns:
        True if download successful, False otherwise
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Downloading video (attempt {attempt + 1}): {filename}")
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verify file was created and has content
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                logger.info(f"Successfully downloaded: {filename} ({os.path.getsize(filename)/1024/1024:.1f}MB)")
                return True
            else:
                logger.error(f"Downloaded file is empty or missing: {filename}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Download attempt {attempt + 1} failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during download attempt {attempt + 1}: {e}")
    
    logger.error(f"Failed to download video after {max_retries} attempts")
    return False


def video_fetcher_node(state: Dict) -> Dict:
    """
    Main video fetcher node - searches and downloads relevant videos using Pixabay API.
    
    Args:
        state: Pipeline state containing scenes and keywords
    
    Returns:
        Updated state with video_paths
    """
    logger.info("=== VIDEO FETCHER NODE (Pixabay API) ===")
    
    try:
        scenes = state.get('scenes', [])
        if not scenes:
            logger.error("No scenes found in state")
            return state
        
        video_paths = []
        temp_dir = "temp/videos"
        os.makedirs(temp_dir, exist_ok=True)
        
        for i, scene in enumerate(scenes):
            logger.info(f"\n--- Processing Scene {i+1}/{len(scenes)} ---")
            
            # Extract keywords and prompt from scene
            keywords = scene.get('keywords', [])
            prompt = scene.get('prompt', '')
            
            if not keywords and not prompt:
                logger.warning(f"Scene {i+1} has no keywords or prompt, skipping")
                video_paths.append(None)
                continue
            
            logger.info(f"Scene {i+1} keywords: {keywords}")
            logger.info(f"Scene {i+1} prompt: {prompt}")
            
            # Search for videos
            videos = search_pixabay_videos(keywords, prompt, limit=30)
            
            if not videos:
                logger.warning(f"No videos found for scene {i+1}")
                video_paths.append(None)
                continue
            
            # Select best video
            best_videos = select_best_videos(videos, keywords, prompt, count=1)
            
            if not best_videos:
                logger.warning(f"No suitable videos selected for scene {i+1}")
                video_paths.append(None)
                continue
            
            selected_video = best_videos[0]
            video_id = selected_video.get('id')
            
            # Get download URL
            download_url = get_video_download_url(selected_video, preferred_quality='medium')
            
            if not download_url:
                logger.error(f"No download URL found for video {video_id}")
                video_paths.append(None)
                continue
            
            # Download video
            video_filename = os.path.join(temp_dir, f"scene_{i+1}_video_{video_id}.mp4")
            
            if download_video(download_url, video_filename):
                video_paths.append(video_filename)
                logger.info(f"✓ Scene {i+1} video ready: {video_filename}")
                
                # Log attribution info for compliance
                video_tags = selected_video.get('tags', 'No tags')
                video_user = selected_video.get('user', 'Unknown')
                page_url = selected_video.get('pageURL', '')
                logger.info(f"Video attribution: '{video_tags}' by {video_user} from Pixabay ({page_url})")
            else:
                logger.error(f"Failed to download video for scene {i+1}")
                video_paths.append(None)
        
        # Update state
        state['video_paths'] = video_paths
        
        successful_downloads = sum(1 for path in video_paths if path is not None)
        logger.info(f"\n=== VIDEO FETCHER COMPLETE ===")
        logger.info(f"Successfully downloaded {successful_downloads}/{len(scenes)} videos")
        logger.info(f"Video paths: {video_paths}")
        
        return state
        
    except Exception as e:
        logger.error(f"Video fetcher node failed: {e}")
        import traceback
        traceback.print_exc()
        return state
