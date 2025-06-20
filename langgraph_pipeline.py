#!/usr/bin/env python3
"""
Complete LangGraph Pipeline for AI-Powere               # Initialize all nodes
        self.scene_analyzer = SceneAnalyzerNode()
        self.prompt_generator = PromptGeneratorNode()
        self.video_fetcher = VideoFetcherNod            # Prepare scene videos with proper duration data from scenes
            scene_videos = []
            for i, video_result in enumerate(download_results):
                if video_result.get("success"):
                    # Get the corresponding scene data for proper duration
                    scene_data = state["scenes"][i] if i < len(state["scenes"]) else {}
                    scene_duration = scene_data.get("duration", 5.0)
                    scene_start = scene_data.get("start_time", i * scene_duration)
                    
                    scene_videos.append({
                        "scene_id": i + 1,
                        "file_path": video_result.get("file_info", {}).get("path", ""),
                        "duration": scene_duration,  # Use actual scene duration
                        "start_time": scene_start,
                        "end_time": scene_start + scene_duration
                    })I_KEY)  # Pass required API key
        self.voiceover_generator = VoiceoverNode()
        self.subtitle_generator = ProfessionalSubtitleNode()
        self.video_assembler = VideoAssemblyNode()ialize all nodes
        self.scene_analyzer = SceneAnalyzerNode()
        self.prompt_generator = PromptGeneratorNode()
        self.video_fetcher = VideoFetcherNode(PEXELS_API_KEY)  # Pass required API key
        self.voiceover_generator = VoiceoverNode()
        self.subtitle_generator = ProfessionalSubtitleNode()
        self.video_assembler = VideoAssemblyNode()ess Video Generation
Orchestrates the entire workflow from script to YouTube Short
"""

import asyncio
import os
import sys
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
import logging

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all our working nodes
from nodes.scene_analyzer_node import SceneAnalyzerNode
from nodes.prompt_generator_node import PromptGeneratorNode
from nodes.video_fetcher_node import VideoFetcherNode
from nodes.voiceover_node import VoiceoverNode
from nodes.professional_subtitle_node import ProfessionalSubtitleNode
from nodes.video_assembly_node import VideoAssemblyNode
from config import PEXELS_API_KEY
from config import PEXELS_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
        self.video_fetcher = VideoFetcherNode(PEXELS_API_KEY)
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
        
        # Define the workflow edges (sequential pipeline)
        workflow.set_entry_point("analyze_scenes")
        workflow.add_edge("analyze_scenes", "generate_prompts")
        workflow.add_edge("generate_prompts", "fetch_videos")
        workflow.add_edge("fetch_videos", "generate_voiceover")
        workflow.add_edge("generate_voiceover", "generate_subtitles")
        workflow.add_edge("generate_subtitles", "assemble_video")
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
        """Wrapper for scene analysis node"""
        try:
            state = self._update_progress(state, "Analyzing scenes with AI...")
            
            logger.info("🎬 Starting scene analysis...")
            scenes = await self.scene_analyzer.analyze_scenes(state["script"])
            state["scenes"] = scenes
            
            logger.info(f"✅ Scene analysis complete! Generated {len(scenes)} scenes")
            for i, scene in enumerate(scenes, 1):
                logger.info(f"  Scene {i}: {scene.get('description', 'No description')[:50]}...")
                
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
        """Wrapper for video fetching node"""
        try:
            state = self._update_progress(state, "Downloading videos from Pexels...")
            
            logger.info("📥 Downloading videos from Pexels API...")
            
            # Create the scene queries format expected by VideoFetcherNode
            scene_queries = []
            for i, (scene, query_data) in enumerate(zip(state["scenes"], state["search_queries"])):
                scene_query = {
                    'scene_id': i + 1,
                    'scene_description': scene.get('description', ''),
                    'query_data': type('obj', (object,), {
                        'primary_query': query_data.get('primary_query', ''),
                        'fallback_queries': query_data.get('fallback_queries', []),
                        'category': query_data.get('category', 'business')
                    })(),
                    'timing': {
                        'start_time': scene.get('timing', {}).get('start', 0),
                        'end_time': scene.get('timing', {}).get('end', 5),
                        'duration': scene.get('duration', 5)
                    }
                }
                scene_queries.append(scene_query)
            
            # Use the correct method name
            fetch_result = await self.video_fetcher.fetch_videos_for_scenes(scene_queries)
            state["downloaded_videos"] = fetch_result.get("results", [])
            
            successful_downloads = [v for v in state["downloaded_videos"] if v.get("success", False)]
            logger.info(f"✅ Video download complete! Downloaded {len(successful_downloads)}/{len(state['downloaded_videos'])} videos")
            
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