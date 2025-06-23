#!/usr/bin/env python3
"""
Complete LangGraph Pipeline for AI-Powered Video Generation
Orchestrates the entire workflow from script to YouTube Short

AUDIO-FIRST ARCHITECTURE FOR PERFECT SYNC:
1. Generate audio FIRST (master timeline)
2. Generate subtitles with precise timing
3. Analyze scenes using REAL audio timing
4. Generate prompts based on audio-timed scenes
5. Fetch videos to match real audio timing
6. Assemble with perfect sync
"""

import asyncio
import os
import sys
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
import logging
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all our working nodes
from nodes.scene_analyzer_node import SceneAnalyzerNode
from nodes.prompt_generator_node import PromptGeneratorNode
from nodes.video_fetcher_node import search_pixabay_videos, select_best_videos, get_video_download_url, download_video
from nodes.voiceover_node import VoiceoverNode
from nodes.professional_subtitle_node import ProfessionalSubtitleNode
from nodes.video_assembly_node import VideoAssemblyNode
from config import PEXELS_API_KEY

# Configure extensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler(f'pipeline_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class VideoGenerationState(TypedDict):
    """State shared across all nodes in the pipeline"""
    # Input
    script: str
    
    # Scene Analysis Results
    scenes: List[Dict[str, Any]]
    
    # Prompt Generation Results
    search_queries: List[Dict[str, Any]]
    
    # Video Fetching Results
    downloaded_videos: List[Dict[str, Any]]
    
    # Audio Generation Results
    audio_file: str
    audio_duration: float
    
    # Subtitle Generation Results
    subtitle_segments: List[Dict[str, Any]]
    
    # Final Output
    final_video_path: str
    
    # Error handling
    errors: List[str]
    
    # Progress tracking
    current_step: str
    total_steps: int
    completed_steps: int

class AIVideoGenerator:
    """Complete AI-powered video generation pipeline using LangGraph"""
    
    def __init__(self):
        """Initialize the pipeline with all nodes"""
        logger.info("Initializing AI Video Generator Pipeline...")
        
        # Initialize all nodes
        self.scene_analyzer = SceneAnalyzerNode()
        self.prompt_generator = PromptGeneratorNode()
        # Video fetching now uses function-based approach with Pixabay
        self.voiceover_generator = VoiceoverNode()
        self.subtitle_generator = ProfessionalSubtitleNode()
        self.video_assembler = VideoAssemblyNode()
        
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()
        
        logger.info("Pipeline initialized successfully!")
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow connecting all nodes"""
        workflow = StateGraph(VideoGenerationState)
        
        # Add all nodes to the workflow
        workflow.add_node("analyze_scenes", self._analyze_scenes_wrapper)
        workflow.add_node("generate_prompts", self._generate_prompts_wrapper)
        workflow.add_node("fetch_videos", self._fetch_videos_wrapper)
        workflow.add_node("generate_voiceover", self._generate_voiceover_wrapper)
        workflow.add_node("generate_subtitles", self._generate_subtitles_wrapper)
        workflow.add_node("assemble_video", self._assemble_video_wrapper)
        
        # Define the workflow edges (AUDIO-FIRST pipeline for perfect sync)
        workflow.set_entry_point("generate_voiceover")
        workflow.add_edge("generate_voiceover", "generate_subtitles")
        workflow.add_edge("generate_subtitles", "analyze_scenes")
        workflow.add_edge("analyze_scenes", "generate_prompts")
        workflow.add_edge("generate_prompts", "fetch_videos")
        workflow.add_edge("fetch_videos", "assemble_video")
        workflow.add_edge("assemble_video", END)
        
        return workflow.compile()
    
    def _update_progress(self, state: VideoGenerationState, step_name: str) -> VideoGenerationState:
        """Update progress tracking"""
        state["current_step"] = step_name
        state["completed_steps"] += 1
        progress_percent = (state["completed_steps"] / state["total_steps"]) * 100
        logger.info(f"Progress: {progress_percent:.1f}% - {step_name}")
        return state
    
    async def _analyze_scenes_wrapper(self, state: VideoGenerationState) -> VideoGenerationState:
        """Wrapper for scene analysis node - NOW USES AUDIO TIMING"""
        try:
            state = self._update_progress(state, "Analyzing scenes with REAL audio timing...")
            
            logger.info("🎬 Starting audio-driven scene analysis...")
            
            # Use the NEW audio-aware method
            scenes = await self.scene_analyzer.analyze_scenes_with_audio_timing(
                state["script"], 
                state["audio_duration"], 
                state["subtitle_segments"]
            )
            state["scenes"] = scenes
            
            logger.info(f"✅ Audio-synced scene analysis complete! Generated {len(scenes)} scenes")
            for i, scene in enumerate(scenes, 1):
                logger.info(f"  Scene {i}: {scene['timing']['start']:.1f}s-{scene['timing']['end']:.1f}s \"{scene.get('text', '')[:40]}...\"")
                
        except Exception as e:
            error_msg = f"Scene analysis failed: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            
        return state
    
    async def _generate_prompts_wrapper(self, state: VideoGenerationState) -> VideoGenerationState:
        """Wrapper for prompt generation node"""
        try:
            state = self._update_progress(state, "Generating search queries...")
            
            logger.info("🔍 Generating optimized search queries...")
            search_queries = await self.prompt_generator.generate_search_queries(state["scenes"])
            state["search_queries"] = search_queries
            
            logger.info(f"✅ Search query generation complete! Generated {len(search_queries)} queries")
            for i, query in enumerate(search_queries, 1):
                logger.info(f"  Query {i}: {query.get('primary_query', 'No query')}")
                
        except Exception as e:
            error_msg = f"Prompt generation failed: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            
        return state
    
    async def _fetch_videos_wrapper(self, state: VideoGenerationState) -> VideoGenerationState:
        """Wrapper for video fetching using new Pixabay semantic search"""
        try:
            state = self._update_progress(state, "Downloading videos from Pixabay...")
            
            logger.info("📥 Downloading videos using Pixabay semantic search...")
            
            scenes = state.get("scenes", [])
            search_queries = state.get("search_queries", [])
            
            if not scenes or not search_queries:
                logger.error("Missing scenes or search queries for video fetching")
                state["errors"].append("Missing scenes or search queries")
                return state
            
            downloaded_videos = []
            temp_dir = "temp/videos"
            os.makedirs(temp_dir, exist_ok=True)
            
            for i, (scene, query_data) in enumerate(zip(scenes, search_queries)):
                logger.info(f"\n--- Fetching video for Scene {i+1}/{len(scenes)} ---")
                
                # Extract keywords and prompt
                keywords = []
                primary_query = query_data.get('primary_query', '')
                fallback_queries = query_data.get('fallback_queries', [])
                
                if primary_query:
                    keywords.append(primary_query)
                keywords.extend(fallback_queries[:2])  # Add top 2 fallback queries
                
                # Use scene description as prompt context
                prompt = scene.get('description', primary_query)
                
                if not keywords:
                    logger.warning(f"No keywords for scene {i+1}, skipping")
                    downloaded_videos.append({"success": False, "error": "No keywords"})
                    continue
                
                logger.info(f"Scene {i+1} keywords: {keywords}")
                logger.info(f"Scene {i+1} prompt: {prompt}")
                
                try:
                    # Search for videos
                    videos = search_pixabay_videos(keywords, prompt, limit=30)
                    
                    if not videos:
                        logger.warning(f"No videos found for scene {i+1}")
                        downloaded_videos.append({"success": False, "error": "No videos found"})
                        continue
                    
                    # Select best video
                    best_videos = select_best_videos(videos, keywords, prompt, count=1)
                    
                    if not best_videos:
                        logger.warning(f"No suitable videos selected for scene {i+1}")
                        downloaded_videos.append({"success": False, "error": "No suitable videos"})
                        continue
                    
                    selected_video = best_videos[0]
                    video_id = selected_video.get('id')
                    
                    # Get download URL
                    download_url = get_video_download_url(selected_video, preferred_quality='medium')
                    
                    if not download_url:
                        logger.error(f"No download URL found for video {video_id}")
                        downloaded_videos.append({"success": False, "error": "No download URL"})
                        continue
                    
                    # Download video
                    video_filename = os.path.join(temp_dir, f"scene_{i+1}_video_{video_id}.mp4")
                    
                    if download_video(download_url, video_filename):
                        downloaded_videos.append({
                            "success": True,
                            "scene_id": i + 1,
                            "video_id": video_id,
                            "file_info": {"path": video_filename},
                            "metadata": {
                                "tags": selected_video.get('tags', ''),
                                "duration": selected_video.get('duration', 0),
                                "views": selected_video.get('views', 0),
                                "downloads": selected_video.get('downloads', 0)
                            }
                        })
                        logger.info(f"✓ Scene {i+1} video ready: {video_filename}")
                    else:
                        logger.error(f"Failed to download video for scene {i+1}")
                        downloaded_videos.append({"success": False, "error": "Download failed"})
                        
                except Exception as scene_error:
                    logger.error(f"Error processing scene {i+1}: {scene_error}")
                    downloaded_videos.append({"success": False, "error": str(scene_error)})
            
            state["downloaded_videos"] = downloaded_videos
            
            successful_downloads = [v for v in downloaded_videos if v.get("success", False)]
            logger.info(f"✅ Video download complete! Downloaded {len(successful_downloads)}/{len(scenes)} videos")
            
        except Exception as e:
            error_msg = f"Video fetching failed: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            
        return state
    
    async def _generate_voiceover_wrapper(self, state: VideoGenerationState) -> VideoGenerationState:
        """Wrapper for voiceover generation node"""
        try:
            state = self._update_progress(state, "Generating AI voiceover...")
            
            logger.info("🎙️ Generating AI voiceover with Edge-TTS...")
            audio_result = await self.voiceover_generator.generate_voiceover(state["script"])
            
            state["audio_file"] = audio_result["audio_file"]
            state["audio_duration"] = audio_result["duration"]
            
            logger.info(f"✅ Voiceover generation complete! Duration: {audio_result['duration']:.2f}s")
            
        except Exception as e:
            error_msg = f"Voiceover generation failed: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            
        return state
    
    async def _generate_subtitles_wrapper(self, state: VideoGenerationState) -> VideoGenerationState:
        """Wrapper for subtitle generation node"""
        try:
            state = self._update_progress(state, "Generating synchronized subtitles...")
            
            logger.info("📝 Generating professional subtitles...")
            subtitle_result = await self.subtitle_generator.generate_subtitles(
                state["audio_file"], 
                state["script"]
            )
            
            state["subtitle_segments"] = subtitle_result["segments"]
            
            logger.info(f"✅ Subtitle generation complete! Generated {len(subtitle_result['segments'])} segments")
            
        except Exception as e:
            error_msg = f"Subtitle generation failed: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            
        return state
    
    async def _assemble_video_wrapper(self, state: VideoGenerationState) -> VideoGenerationState:
        """Wrapper for video assembly node"""
        try:
            state = self._update_progress(state, "Assembling final video...")
            
            logger.info("🎬 Assembling final YouTube Short...")
            
            # Prepare scene videos with proper duration data from scenes
            scene_videos = []
            download_results = state["downloaded_videos"]
            
            for i, video_result in enumerate(download_results):
                if video_result.get("success"):
                    # Get the corresponding scene data for proper duration
                    scene_data = state["scenes"][i] if i < len(state["scenes"]) else {}
                    scene_duration = scene_data.get("duration", 5.0)
                    scene_start = scene_data.get("timing", {}).get("start", i * scene_duration)
                    
                    scene_videos.append({
                        "scene_id": i + 1,
                        "file_path": video_result.get("file_info", {}).get("path", ""),
                        "duration": scene_duration,  # Use actual scene duration
                        "start_time": scene_start,
                        "end_time": scene_start + scene_duration
                    })
            
            logger.info(f"📹 Prepared {len(scene_videos)} scene videos with proper durations")
            for sv in scene_videos:
                logger.info(f"  Scene {sv['scene_id']}: {sv['duration']:.1f}s ({os.path.basename(sv['file_path'])})")
            
            # Use the correct method signature
            assembly_result = await self.video_assembler.assemble_video(
                scene_videos=scene_videos,
                audio_path=state["audio_file"],
                subtitles=state["subtitle_segments"],
                script=state["script"],
                title="AI_Generated_YouTube_Short"
            )
            
            if assembly_result.success:
                state["final_video_path"] = assembly_result.output_path
                logger.info(f"✅ Video assembly complete! Final video: {assembly_result.output_path}")
            else:
                error_msg = f"Video assembly failed: {assembly_result.error}"
                logger.error(error_msg)
                state["errors"].append(error_msg)
            
        except Exception as e:
            error_msg = f"Video assembly failed: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            
        return state
    
    async def generate_video(self, input_file: str = "input.txt") -> Dict[str, Any]:
        """
        Generate a complete YouTube Short from input script
        
        Args:
            input_file: Path to the input script file
            
        Returns:
            Dict containing generation results
        """
        try:
            # Read input script
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file not found: {input_file}")
                
            with open(input_file, 'r', encoding='utf-8') as f:
                script = f.read().strip()
                
            if not script:
                raise ValueError("Input script is empty")
                
            logger.info(f"📄 Loaded script from {input_file} ({len(script)} characters)")
            
            # Initialize state
            initial_state: VideoGenerationState = {
                "script": script,
                "scenes": [],
                "search_queries": [],
                "downloaded_videos": [],
                "audio_file": "",
                "audio_duration": 0.0,
                "subtitle_segments": [],
                "final_video_path": "",
                "errors": [],
                "current_step": "Starting...",
                "total_steps": 6,
                "completed_steps": 0
            }
            
            logger.info("🚀 Starting AI video generation pipeline...")
            
            # Execute the workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Check for errors
            if final_state["errors"]:
                logger.error("❌ Pipeline completed with errors:")
                for error in final_state["errors"]:
                    logger.error(f"  - {error}")
                return {
                    "success": False,
                    "errors": final_state["errors"],
                    "final_video_path": final_state.get("final_video_path")
                }
            
            logger.info("🎉 AI video generation pipeline completed successfully!")
            logger.info(f"📹 Final video available at: {final_state['final_video_path']}")
            
            return {
                "success": True,
                "final_video_path": final_state["final_video_path"],
                "audio_duration": final_state["audio_duration"],
                "scenes_count": len(final_state["scenes"]),
                "videos_downloaded": len([v for v in final_state["downloaded_videos"] if v.get("success", False)]),
                "subtitle_segments": len(final_state["subtitle_segments"])
            }
            
        except Exception as e:
            error_msg = f"Pipeline execution failed: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }

async def main():
    """Main function to run the complete pipeline"""
    try:
        # Initialize the AI video generator
        generator = AIVideoGenerator()
        
        # Generate video from input.txt
        result = await generator.generate_video("input.txt")
        
        if result["success"]:
            print("\n" + "="*60)
            print("🎉 VIDEO GENERATION COMPLETED SUCCESSFULLY!")
            print("="*60)
            print(f"📹 Final Video: {result['final_video_path']}")
            print(f"⏱️  Audio Duration: {result['audio_duration']:.2f} seconds")
            print(f"🎬 Scenes Generated: {result['scenes_count']}")
            print(f"📥 Videos Downloaded: {result['videos_downloaded']}")
            print(f"📝 Subtitle Segments: {result['subtitle_segments']}")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ VIDEO GENERATION FAILED!")
            print("="*60)
            if "errors" in result:
                for error in result["errors"]:
                    print(f"❌ {error}")
            elif "error" in result:
                print(f"❌ {result['error']}")
            print("="*60)
            
    except KeyboardInterrupt:
        print("\n⚠️ Pipeline interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())