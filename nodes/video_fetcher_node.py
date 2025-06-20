"""
Video Fetcher Node - Pexels API Integration for Stock Video Download
Downloads high-quality portrait videos optimized for YouTube Shorts
"""

import asyncio
import aiohttp
import json
import logging
import os
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse
import hashlib
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VideoResult:
    """Represents a downloaded video with metadata"""
    scene_id: int
    video_id: str
    file_path: str
    original_url: str
    duration: Optional[float]
    width: int
    height: int
    file_size: int
    query_used: str
    download_time: float
    source: str = "pexels"

class VideoFetcherNode:
    """
    Fetches and downloads stock videos from Pexels API
    Optimized for vertical YouTube Shorts format (9:16 aspect ratio)
    """
    
    def __init__(self, api_key: str, download_dir: str = "temp/videos"):
        """Initialize the Video Fetcher with Pexels API"""
        self.api_key = api_key
        self.download_dir = download_dir
        self.base_url = "https://api.pexels.com/videos"
        
        # Create download directory
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Rate limiting (Pexels: 200 requests/hour)
        self.request_count = 0
        self.request_window_start = time.time()
        self.max_requests_per_hour = 180  # Leave some buffer
        
        # Video quality preferences (in order of preference)
        self.quality_preferences = ['hd', 'sd']
        
        # Minimum video requirements for YouTube Shorts
        self.min_width = 720
        self.min_height = 1280  # 9:16 aspect ratio
        self.preferred_aspect_ratio = 9/16
        self.aspect_ratio_tolerance = 0.15
        
        # Track used videos to avoid duplicates
        self.used_video_ids = set()
        
        # Fallback search queries for variety
        self.variety_queries = [
            'professional business', 'modern office', 'corporate meeting',
            'financial planning', 'investment success', 'business growth',
            'professional handshake', 'money concept', 'wealth building',
            'real estate', 'property investment', 'financial chart'
        ]

    async def fetch_videos_for_scenes(self, scene_queries: List[Dict]) -> Dict[str, Any]:
        """
        Fetch videos for all scenes using their search queries
        
        Args:
            scene_queries: List of scene query dictionaries from PromptGeneratorNode
            
        Returns:
            Dictionary containing download results for each scene
        """
        try:
            logger.info(f"Fetching videos for {len(scene_queries)} scenes...")
            
            # Create session with proper headers (no "Bearer " prefix)
            connector = aiohttp.TCPConnector(limit=10)
            timeout = aiohttp.ClientTimeout(total=300)  # 5 minutes total timeout
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    'Authorization': self.api_key,  # Direct API key, no Bearer prefix
                    'User-Agent': 'AI-Video-Generator/1.0'
                }
            ) as session:
                
                download_results = []
                
                for i, scene_query in enumerate(scene_queries):
                    logger.info(f"Processing scene {i+1}/{len(scene_queries)}: {scene_query['scene_id']}")
                    
                    # Check rate limits
                    await self._check_rate_limit()
                    
                    # Fetch video for this scene
                    result = await self._fetch_scene_video(session, scene_query)
                    
                    if result['success']:
                        download_results.append(result)
                        logger.info(f"✅ Successfully downloaded video for scene {scene_query['scene_id']}")
                    else:
                        logger.warning(f"⚠️ Failed to download video for scene {scene_query['scene_id']}: {result['error']}")
                        download_results.append(result)
                    
                    # Small delay to be respectful to the API
                    await asyncio.sleep(0.5)
                
                return {
                    'success': True,
                    'total_scenes': len(scene_queries),
                    'successful_downloads': len([r for r in download_results if r['success']]),
                    'failed_downloads': len([r for r in download_results if not r['success']]),
                    'results': download_results
                }
                
        except Exception as e:
            logger.error(f"Error in video fetching pipeline: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'results': []
            }

    async def _fetch_scene_video(self, session: aiohttp.ClientSession, scene_query: Dict) -> Dict[str, Any]:
        """Fetch and download a video for a single scene"""
        try:
            query_data = scene_query['query_data']
            scene_id = scene_query['scene_id']
            
            # Try primary query first
            search_result = await self._search_videos(session, query_data.primary_query)
            
            if not search_result['success'] or not search_result['videos']:
                # Try fallback queries
                for fallback_query in query_data.fallback_queries:
                    logger.info(f"Trying fallback query: {fallback_query}")
                    search_result = await self._search_videos(session, fallback_query)
                    if search_result['success'] and search_result['videos']:
                        break
            
            # If still no results, try variety queries for uniqueness
            if not search_result['success'] or not search_result['videos']:
                for variety_query in self.variety_queries:
                    logger.info(f"Trying variety query: {variety_query}")
                    search_result = await self._search_videos(session, variety_query)
                    if search_result['success'] and search_result['videos']:
                        break
            
            if not search_result['success'] or not search_result['videos']:
                return {
                    'success': False,
                    'scene_id': scene_id,
                    'error': 'No suitable videos found for any queries'
                }
            
            # Find the best video for YouTube Shorts (avoiding duplicates)
            best_video = self._select_best_video(search_result['videos'])
            
            if not best_video:
                # If no unique video found, try with increased search results
                logger.info("No unique video found, expanding search...")
                search_result = await self._search_videos(session, query_data.primary_query, per_page=20)
                if search_result['success']:
                    best_video = self._select_best_video(search_result['videos'])
            
            if not best_video:
                return {
                    'success': False,
                    'scene_id': scene_id,
                    'error': 'No unique videos meet YouTube Shorts requirements'
                }
            
            # Download the video
            download_result = await self._download_video(session, best_video, scene_id, query_data.primary_query)
            
            return download_result
            
        except Exception as e:
            logger.error(f"Error fetching video for scene {scene_query['scene_id']}: {str(e)}")
            return {
                'success': False,
                'scene_id': scene_query['scene_id'],
                'error': str(e)
            }

    async def _search_videos(self, session: aiohttp.ClientSession, query: str, per_page: int = 10) -> Dict[str, Any]:
        """Search for videos using Pexels API"""
        try:
            search_url = f"{self.base_url}/search"
            params = {
                'query': query,
                'orientation': 'portrait',  # Essential for YouTube Shorts
                'size': 'medium',  # Full HD quality
                'per_page': per_page  # Get multiple options
            }
            
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Found {len(data.get('videos', []))} videos for query: {query}")
                    
                    return {
                        'success': True,
                        'videos': data.get('videos', []),
                        'total_results': data.get('total_results', 0)
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Search failed (status {response.status}): {error_text}")
                    return {
                        'success': False,
                        'error': f"API error: {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"Search request failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _select_best_video(self, videos: List[Dict]) -> Optional[Dict]:
        """Select the best video for YouTube Shorts from search results, avoiding duplicates"""
        suitable_videos = []
        
        for video in videos:
            video_id = video.get('id')
            
            # Skip if we've already used this video
            if video_id in self.used_video_ids:
                continue
                
            # Check if video meets basic requirements
            width = video.get('width', 0)
            height = video.get('height', 0)
            duration = video.get('duration', 0)
            
            # Must be portrait and meet minimum dimensions
            if height > width and width >= self.min_width and height >= self.min_height:
                # Check aspect ratio (should be close to 9:16)
                aspect_ratio = width / height if height > 0 else 0
                if abs(aspect_ratio - self.preferred_aspect_ratio) <= self.aspect_ratio_tolerance:
                    # Check if it has suitable video files
                    video_files = video.get('video_files', [])
                    best_file = self._get_best_video_file(video_files)
                    
                    if best_file:
                        suitable_videos.append({
                            'video': video,
                            'file': best_file,
                            'score': self._calculate_video_score(video, best_file)
                        })
        
        if not suitable_videos:
            logger.warning("No new videos meet YouTube Shorts requirements")
            return None
        
        # Sort by score (higher is better) and return the best
        suitable_videos.sort(key=lambda x: x['score'], reverse=True)
        best = suitable_videos[0]
        
        # Mark this video as used
        self.used_video_ids.add(best['video']['id'])
        
        logger.info(f"Selected video: {best['video']['id']} "
                   f"({best['file']['width']}x{best['file']['height']}, "
                   f"{best['video']['duration']}s, score: {best['score']:.2f})")
        
        return {
            'video_data': best['video'],
            'video_file': best['file']
        }

    def _get_best_video_file(self, video_files: List[Dict]) -> Optional[Dict]:
        """Select the best video file based on quality preferences"""
        # Group files by quality
        quality_groups = {}
        for vf in video_files:
            quality = vf.get('quality', 'sd')
            if quality not in quality_groups:
                quality_groups[quality] = []
            quality_groups[quality].append(vf)
        
        # Try preferred qualities in order
        for preferred_quality in self.quality_preferences:
            if preferred_quality in quality_groups:
                files = quality_groups[preferred_quality]
                # Within the same quality, prefer higher resolution
                files.sort(key=lambda x: (x.get('width', 0) * x.get('height', 0)), reverse=True)
                return files[0]
        
        # Fallback to any available file
        if video_files:
            return video_files[0]
        
        return None

    def _calculate_video_score(self, video: Dict, video_file: Dict) -> float:
        """Calculate a score for video quality and suitability"""
        score = 0.0
        
        # Resolution score (prefer higher resolution)
        width = video_file.get('width', 0)
        height = video_file.get('height', 0)
        resolution_score = (width * height) / (1080 * 1920)  # Normalize to ideal YouTube Shorts res
        score += min(resolution_score, 1.0) * 30
        
        # Aspect ratio score (prefer 9:16)
        if height > 0:
            aspect_ratio = width / height
            aspect_diff = abs(aspect_ratio - self.preferred_aspect_ratio)
            aspect_score = max(0, 1 - (aspect_diff / self.aspect_ratio_tolerance))
            score += aspect_score * 25
        
        # Duration score (prefer moderate lengths for scenes)
        duration = video.get('duration', 0)
        if 5 <= duration <= 30:
            score += 20
        elif 3 <= duration <= 45:
            score += 15
        elif duration > 0:
            score += 10
        
        # Quality preference score
        quality = video_file.get('quality', 'sd')
        if quality == 'hd':
            score += 15
        elif quality == 'sd':
            score += 10
        
        # File format preference
        file_type = video_file.get('file_type', '')
        if 'mp4' in file_type:
            score += 10
        
        return score

    async def _download_video(self, session: aiohttp.ClientSession, best_video: Dict, scene_id: int, query: str) -> Dict[str, Any]:
        """Download the selected video"""
        try:
            video_data = best_video['video_data']
            video_file = best_video['video_file']
            
            video_id = video_data['id']
            download_url = video_file['link']
            
            # Generate filename
            filename = f"scene_{scene_id}_video_{video_id}.mp4"
            file_path = os.path.join(self.download_dir, filename)
            
            # Download the video
            start_time = time.time()
            
            async with session.get(download_url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                    
                    file_size = os.path.getsize(file_path)
                    download_time = time.time() - start_time
                    
                    # Create result object
                    result = VideoResult(
                        scene_id=scene_id,
                        video_id=str(video_id),
                        file_path=file_path,
                        original_url=video_data.get('url', ''),
                        duration=video_data.get('duration'),
                        width=video_file.get('width', 0),
                        height=video_file.get('height', 0),
                        file_size=file_size,
                        query_used=query,
                        download_time=download_time
                    )
                    
                    logger.info(f"Downloaded {file_size} bytes in {download_time:.2f}s")
                    
                    return {
                        'success': True,
                        'scene_id': scene_id,
                        'video_result': result,
                        'video_data': video_data,
                        'file_info': {
                            'path': file_path,
                            'size': file_size,
                            'duration': video_data.get('duration'),
                            'dimensions': f"{video_file.get('width')}x{video_file.get('height')}"
                        }
                    }
                else:
                    error_text = await response.text()
                    return {
                        'success': False,
                        'scene_id': scene_id,
                        'error': f"Download failed: {response.status} - {error_text}"
                    }
                    
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            return {
                'success': False,
                'scene_id': scene_id,
                'error': str(e)
            }

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        current_time = time.time()
        
        # Reset counter if an hour has passed
        if current_time - self.request_window_start > 3600:
            self.request_count = 0
            self.request_window_start = current_time
        
        # Check if we're approaching the limit
        if self.request_count >= self.max_requests_per_hour:
            wait_time = 3600 - (current_time - self.request_window_start)
            if wait_time > 0:
                logger.warning(f"Rate limit reached. Waiting {wait_time:.0f} seconds...")
                await asyncio.sleep(wait_time)
                self.request_count = 0
                self.request_window_start = time.time()
        
        self.request_count += 1

    def get_download_summary(self, results: List[Dict]) -> str:
        """Generate a human-readable summary of download results"""
        if not results:
            return "No download results available."
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        summary_lines = [
            f"Video Download Summary ({len(results)} scenes):",
            "-" * 60,
            f"✅ Successful Downloads: {len(successful)}",
            f"❌ Failed Downloads: {len(failed)}",
            ""
        ]
        
        if successful:
            summary_lines.append("Successful Downloads:")
            total_size = 0
            total_duration = 0
            
            for result in successful:
                if result.get('video_result'):
                    vr = result['video_result']
                    size_mb = vr.file_size / (1024 * 1024)
                    total_size += vr.file_size
                    total_duration += vr.duration or 0
                    
                    summary_lines.append(
                        f"  Scene {vr.scene_id}: {vr.width}x{vr.height}, "
                        f"{vr.duration}s, {size_mb:.1f}MB ({vr.query_used})"
                    )
            
            total_size_mb = total_size / (1024 * 1024)
            summary_lines.extend([
                "",
                f"📊 Total: {total_size_mb:.1f}MB, {total_duration:.1f}s of video content"
            ])
        
        if failed:
            summary_lines.extend([
                "",
                "Failed Downloads:"
            ])
            for result in failed:
                summary_lines.append(f"  Scene {result['scene_id']}: {result.get('error', 'Unknown error')}")
        
        return "\n".join(summary_lines)

# Example usage and testing
async def test_video_fetcher():
    """Test the Video Fetcher Node"""
    from config import PEXELS_API_KEY
    
    # Initialize fetcher
    fetcher = VideoFetcherNode(PEXELS_API_KEY)
    
    # Create test scene queries (simulating output from PromptGeneratorNode)
    test_scene_queries = [
        {
            'scene_id': 1,
            'scene_description': 'Person looking worried about money',
            'query_data': type('obj', (object,), {
                'primary_query': 'business stress',
                'fallback_queries': ['office work', 'professional', 'business'],
                'category': 'business'
            })(),
            'timing': {'start_time': 0.0, 'end_time': 5.0, 'duration': 5.0}
        },
        {
            'scene_id': 2,
            'scene_description': 'Investment and money growth concepts',
            'query_data': type('obj', (object,), {
                'primary_query': 'investment money',
                'fallback_queries': ['finance', 'money growth', 'wealth'],
                'category': 'finance'
            })(),
            'timing': {'start_time': 5.0, 'end_time': 10.0, 'duration': 5.0}
        }
    ]
    
    # Test video fetching
    result = await fetcher.fetch_videos_for_scenes(test_scene_queries)
    
    if result['success']:
        print("✅ Video Fetching Successful!")
        print(fetcher.get_download_summary(result['results']))
        return result
    else:
        print(f"❌ Video Fetching Failed: {result['error']}")
        return None

if __name__ == "__main__":
    asyncio.run(test_video_fetcher())