# 🎬 AI-Powered Viral YouTube Shorts Generator

> **Status: Active Development** | **Resume-Ready Project** | **Interview Demo Available**

A fully automated, AI-powered video generation system that transforms text concepts into high-engagement YouTube Shorts with realistic voiceover, synchronized subtitles, semantically-matched visuals, and background music. Built for maximum viewer retention and viral potential.

## 🎯 **PROJECT HIGHLIGHTS - V4.0**

### 🔥 **VIRAL SCRIPT GENERATION ENGINE**
✅ **AI-POWERED SCRIPT CREATION** - Gemini 2.0 Thinking + viral research integration  
✅ **QUALITY CONTROL SYSTEM** - Iterative feedback loop with AI rater for viral potential  
✅ **VIRAL RESEARCH INTEGRATION** - Full VIRAL_CONTENT_RESEARCH.md context for hook optimization  
✅ **AUTOMATED SCRIPT PIPELINE** - No more manual input.txt - fully AI-generated scripts  

### 🎵 **BACKGROUND MUSIC INTEGRATION (NEW!)**
✅ **OPENVERSE API INTEGRATION** - Fetches royalty-free background music automatically  
✅ **INTELLIGENT MUSIC MATCHING** - Mood and content-aware music selection  
✅ **MULTI-SOURCE SUPPORT** - Freesound, Jamendo, and other Creative Commons sources  
✅ **QUALITY SCORING SYSTEM** - Advanced relevance scoring for optimal music selection  
🔄 **PIPELINE INTEGRATION** - Ready for integration into main video generation workflow  

### 🎙️ **ADVANCED TTS WITH VOICE CLONING**
✅ **COQUI XTTS V2 IMPLEMENTATION** - 2-5x better quality than Edge-TTS with emotion control  
✅ **GPU ACCELERATION** - CUDA support for faster, more realistic voiceover generation  
✅ **VOICE CLONING READY** - Custom voice training with 5-30 second samples  
✅ **HARDWARE OPTIMIZED** - RTX 3050 + 16GB RAM confirmed compatible  
🔄 **RAV UPGRADE PLANNED** - Research phase for next-generation voice cloning  

### 📊 **ROBUST PIPELINE ARCHITECTURE**
✅ **PERFECT AUDIO-VIDEO SYNC** - Audio-first architecture eliminates timing issues  
✅ **INTELLIGENT VIDEO MATCHING** - Pixabay semantic search with rich metadata scoring  
✅ **BRAND-AWARE CONTENT** - "Wealthier Everyday" context for financial education focus  
✅ **LANGGRAPH ORCHESTRATION** - Modular, fault-tolerant pipeline with comprehensive logging  
✅ **FUNCTION-BASED EFFICIENCY** - Streamlined architecture for optimal performance  

## ✨ Core Features

### 🤖 **AI-Powered Content Generation**
- **Viral Script Generation**: Automatic script creation with quality control and viral research
- **Scene Analysis**: Intelligent script breakdown with timing and mood detection
- **Prompt Engineering**: Brand-aware, context-rich search query generation
- **Content Optimization**: Financial education focus with emotional intelligence

### 🎵 **Multi-Media Processing**  
- **Advanced TTS**: Coqui XTTS v2 with emotion control and voice cloning
- **Background Music**: Openverse integration for royalty-free music matching
- **Video Fetching**: Pixabay semantic search with intelligent relevance scoring
- **Subtitle Generation**: Whisper-based transcription with precise timing

### 🎬 **Professional Video Assembly**
- **Audio-First Sync**: Generate audio → subtitles → scenes for perfect timing
- **YouTube Shorts Optimization**: 9:16 aspect ratio, engagement-focused formatting  
- **Dynamic Assembly**: MoviePy-based compilation with safety validation
- **Quality Control**: Comprehensive error handling and fallback strategies

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (3.11+ recommended)
- FFmpeg installed on your system
- CUDA-compatible GPU (optional, for faster TTS)
- API keys (see [Configuration](#configuration))

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd ai-video-generator
```

2. **Create virtual environment**:
```bash
python -m venv ai_video_env
source ai_video_env/bin/activate  # On Windows: ai_video_env\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure API keys** (see [Configuration](#configuration))

5. **Test the music node** (optional):
```bash
python nodes/music_node.py
```

6. **Generate your first video**:
```bash
python langgraph_pipeline.py
```

## 📋 Configuration

### Required API Keys

1. **Google Gemini API** (Free tier: 60 requests/minute)
   - Get from: https://makersuite.google.com/app/apikey
   - Used for: AI scene analysis, script generation, and content optimization

2. **Pixabay API** (Free tier: 5,000 requests/hour)
   - Get from: https://pixabay.com/api/docs/
   - Used for: High-quality stock video footage with semantic matching

### Optional Services

3. **Openverse API** (No API key required!)
   - Automatic royalty-free music fetching
   - Creative Commons licensed content
   - No rate limits for standard usage

### Setup

1. Open `config.py`
2. Replace placeholder values with your actual API keys:

```python
GEMINI_API_KEY = "your_gemini_api_key_here"
PIXABAY_API_KEY = "your_pixabay_api_key_here"
```

## 📝 Usage

### Fully Automated Generation (Recommended)

```bash
python langgraph_pipeline.py
```

**What happens automatically:**
1. 🔥 **Viral Script Generation** - AI creates engaging scripts with quality control
2. 🎙️ **Advanced Voiceover** - Coqui XTTS v2 generates realistic audio with emotions
3. 📝 **Precise Subtitles** - Whisper transcription with perfect timing alignment
4. 🎬 **Scene Analysis** - Audio-driven breakdown for optimal video matching
5. 🔍 **Smart Video Search** - Pixabay semantic matching with relevance scoring
6. 📥 **Video Download** - High-quality 9:16 clips perfectly timed to scenes
7. 🎵 **Background Music** - *(Coming Soon)* Automatic music selection and mixing
8. 🎬 **Final Assembly** - Professional compilation with synchronized elements

### Custom Script Mode

1. **Edit your script**: Open `input.txt` and write your video script
2. **Run with existing script**: Choose option 2 when prompted
3. **Same automated processing** for the rest of the pipeline

### Testing Individual Components

**Test Music Node:**
```bash
python nodes/music_node.py
```

**Test Voiceover Generation:**
```bash
python nodes/voiceover_node.py
```

## 🏗️ Architecture

### Pipeline Flow

```
🔥 Viral Script → 🎙️ Voiceover → 📝 Subtitles → 🎬 Scene Analysis → 🔍 Prompts → 📹 Videos → 🎵 Music → 🎬 Assembly
```

### Node Components

| Node | Function | Status | Technology |
|------|----------|--------|------------|
| **Viral Script Generator** | AI-powered script creation with quality control | ✅ Complete | Gemini 2.0 Thinking |
| **Voiceover Node** | Advanced TTS with emotion control | ✅ Complete | Coqui XTTS v2 |
| **Subtitle Generator** | Precise speech-to-text transcription | ✅ Complete | OpenAI Whisper |
| **Scene Analyzer** | Audio-timed scene breakdown | ✅ Complete | Gemini 2.5 Flash |
| **Prompt Generator** | Brand-aware search query creation | ✅ Complete | Gemini + Context |
| **Video Fetcher** | Semantic video matching and download | ✅ Complete | Pixabay API |
| **Music Node** | Royalty-free background music | ✅ Complete | Openverse API |
| **Video Assembly** | Professional final video compilation | ✅ Complete | MoviePy + PIL |

### 📁 Project Structure

```
ai-video-generator/
├── langgraph_pipeline.py      # Main orchestration pipeline
├── config.py                  # API keys configuration  
├── input.txt                  # Optional script input (auto-generated available)
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── HARDWARE_ASSESSMENT.md     # System compatibility analysis
├── VIRAL_CONTENT_RESEARCH.md  # Viral content patterns and strategies
├── nodes/                     # Pipeline node modules
│   ├── __init__.py
│   ├── viral_script_generator_node.py  # AI script generation
│   ├── voiceover_node.py      # Advanced TTS with XTTS v2
│   ├── professional_subtitle_node.py   # Whisper transcription
│   ├── scene_analyzer_node.py # Audio-timed scene analysis  
│   ├── prompt_generator_node.py        # Brand-aware search queries
│   ├── video_fetcher_node.py  # Pixabay semantic matching
│   ├── music_node.py          # Openverse music fetching (NEW!)
│   └── video_assembly_node.py # Professional video compilation
├── debug/                     # Generation logs and session data
│   ├── script_generation/     # Viral script generation debugging
│   └── voiceovers/           # TTS generation history
├── output/                    # Generated videos (created automatically)
├── temp/                      # Temporary files (created automatically)
│   ├── music/                # Downloaded background music
│   └── videos/               # Downloaded scene videos
└── mcp-gemini-server/         # Model Context Protocol server (optional)
```

## 🔧 Advanced Configuration

### Hardware Optimization

**System Specifications (Confirmed Compatible):**
- ✅ AMD Ryzen 5 5600H (6C/12T) - Excellent for AI workloads
- ✅ 16GB RAM - Sufficient for advanced models  
- ✅ NVIDIA RTX 3050 (4GB VRAM) - Perfect for CUDA acceleration
- ✅ Fast NVMe SSD with 252GB available space

**Performance Optimizations:**
- GPU acceleration for TTS generation (2-5x faster)
- Parallel video processing and downloads
- Intelligent caching for repeated operations
- Memory-efficient audio processing

### Voice Customization

**Current XTTS v2 Options:**
```python
# Available professional voices
voices = [
    "female_professional",  # Ana Florence (default)
    "male_professional",    # Andrew Chipper  
    "female_friendly",      # Claribel Dervla
    "male_authoritative",   # Damien Black
]

# Emotion control
emotions = ["neutral", "happy", "sad", "angry", "surprised"]
```

**Voice Cloning Setup:**
1. Create `voice_samples/` directory
2. Add 5-30 second voice samples (WAV format)
3. Reference in generation call:
```python
node.generate_voiceover(
    text="Your script text",
    output_path="output.wav",
    cloned_voice="voice_samples/your_voice.wav"
)
```

### Music Customization

**Mood and Genre Options:**
```python
# Available moods
moods = ["upbeat", "calm", "professional", "energetic", "inspiring"]

# Available genres  
genres = ["instrumental", "electronic", "acoustic", "orchestral", "ambient"]

# Content themes
themes = ["business", "education", "lifestyle", "finance", "technology"]
```

**Music Selection:**
```python
from nodes.music_node import MusicNode

music_node = MusicNode()
music_path = await music_node.fetch_background_music(
    mood="professional",
    genre="instrumental", 
    content_theme="business"
)
```

## 📊 Performance Metrics

### Typical Processing Times

| Stage | Duration | Notes |
|-------|----------|-------|
| **Viral Script Generation** | 60-180s | Includes quality iterations |
| **Voiceover Generation** | 5-15s | XTTS v2 with GPU acceleration |
| **Subtitle Generation** | 15-30s | Whisper processing |
| **Scene Analysis** | 10-15s | Gemini API processing |
| **Video Fetching** | 30-60s | Depends on file sizes |
| **Music Fetching** | 10-20s | Openverse download |
| **Video Assembly** | 60-120s | Final compilation |

**Total Pipeline**: ~3-6 minutes per video

### Resource Usage

- **RAM**: 2-4 GB during processing
- **Storage**: ~500MB per generated video  
- **CPU**: Intensive during video processing
- **GPU**: XTTS v2 generation (when available)
- **Network**: ~100-300MB downloads per video

## 🔄 TODO List & Roadmap

### 🎵 Background Music Integration
- [ ] **Pipeline Integration** - Add music node to main workflow
- [ ] **Dynamic Mixing** - Automatic volume balancing with voiceover
- [ ] **Fade Effects** - Professional music transitions
- [ ] **User Preferences** - Customizable music selection criteria

### 🎙️ Advanced Voice Technology  
- [ ] **RAV Integration** - Research and implement Real-time Audio Variational model
- [ ] **Custom Voice Training** - Streamlined voice cloning workflow
- [ ] **Multi-Language Support** - Expand beyond English TTS
- [ ] **Voice Style Transfer** - Advanced prosody and emotion control

### 🤖 AI Enhancement
- [ ] **GPT-4 Vision Integration** - Visual content analysis for better video matching
- [ ] **Dynamic Prompt Optimization** - Self-improving search query generation
- [ ] **A/B Testing Framework** - Automated content performance testing
- [ ] **Viral Trend Analysis** - Real-time social media trend integration

### 🎬 Production Features
- [ ] **Batch Generation** - Multiple videos from topic lists
- [ ] **Brand Customization** - Custom logos, colors, and styling
- [ ] **Social Media Export** - Optimized formats for different platforms
- [ ] **Analytics Integration** - Performance tracking and optimization

### 🔧 Technical Improvements
- [ ] **Docker Containerization** - Easy deployment and scaling
- [ ] **API Endpoint** - RESTful API for external integrations
- [ ] **Web Interface** - User-friendly GUI for non-technical users
- [ ] **Cloud Deployment** - AWS/GCP integration for scalable processing

## 🚨 Troubleshooting

### Common Issues

**Module not found errors**:
```bash
source ai_video_env/bin/activate
pip install -r requirements.txt
```

**FFmpeg not found**:
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`  
- **Windows**: Download from https://ffmpeg.org/

**CUDA not detected** (for GPU acceleration):
```bash
# Check CUDA installation
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

**Music download failures**:
- Check internet connection
- Verify Openverse API accessibility
- Review temp/music/ directory permissions

**API rate limits**:
- Pixabay: 5,000 requests/hour (free tier)
- Gemini: 60 requests/minute (free tier)  
- Wait or upgrade to higher tiers if needed

## 🎯 Best Practices

### Script Writing Tips

- **Hook viewers immediately**: Start with compelling statistics or questions
- **Keep sentences short**: 5-10 words per subtitle segment  
- **Use specific numbers**: "90% of millionaires" vs "most millionaires"
- **Include actionable advice**: Give viewers something they can do
- **End with engagement**: Ask questions or provide calls-to-action

### Content Strategy

**Financial Education Focus:**
- Investment strategies and wealth-building habits
- Personal finance tips and budgeting strategies
- Real estate investment and market analysis
- Business growth and passive income streams
- Behavioral finance and decision-making psychology

**Viral Content Elements:**
- Compelling hooks in first 3 seconds
- Clear value propositions
- Relatable examples and case studies  
- Strong calls-to-action
- Trending topics and timely relevance

## 🤝 Contributing

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest tests/

# Format code  
black .
```

### Code Standards

- **Type hints** for all function parameters and returns
- **Comprehensive logging** for debugging and monitoring
- **Error handling** with graceful fallbacks
- **Documentation** for all public methods and classes

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Google Gemini** for AI-powered content analysis and generation
- **Coqui TTS** for advanced voice synthesis technology
- **OpenAI Whisper** for accurate speech recognition
- **Openverse** for royalty-free music and media content
- **Pixabay** for high-quality stock video footage
- **LangGraph** for pipeline orchestration framework
- **MoviePy** for video processing capabilities

---

**🚀 Ready to create amazing AI-generated videos for your resume and interviews!** 

*This project demonstrates advanced AI integration, pipeline orchestration, multi-modal processing, and production-ready software development practices.*
PIXABAY_API_KEY = "your_pixabay_api_key_here"
```

## 📝 Usage

### Basic Usage

**Option 1: Fully Automated (Recommended)**
1. **Run the viral pipeline**: Execute `python langgraph_pipeline.py`
2. **Watch the magic**: The system will automatically:
   - Generate viral scripts using AI with quality control
   - Analyze scripts with brand context for maximum engagement
   - Create emotionally-intelligent search queries for relevant videos
   - Download high-quality stock footage from Pixabay with semantic matching
   - Generate realistic AI voiceover with advanced TTS
   - Create synchronized subtitles with perfect timing
   - Assemble the final video with flawless sync
3. **Find your video**: Check the `output/` directory for your generated video

**Option 2: Custom Script Input**
1. **Edit your script**: Open `input.txt` and write your video script
2. **Run the pipeline**: Execute `python langgraph_pipeline.py`
3. **Same automated processing** as above but with your custom script

### Example Script

```text
Did you know that 90% of millionaires invest in real estate? Here's why property investment is the secret to building lasting wealth. First, real estate provides passive income through rental payments. Second, property values typically appreciate over time. Third, you get tax benefits that reduce your overall tax burden. Start small with a single rental property and watch your wealth grow automatically.
```

## 🏗️ Architecture

The system uses a **LangGraph-based pipeline** with modular nodes:

### Pipeline Flow

```
� Script Generation → 🤖 Scene Analysis → 🔍 Prompt Generation → 📹 Video Fetching
                                                                         ↓
🎬 Video Assembly ← 📝 Subtitle Generation ← 🎵 Voiceover Generation ←───┘
```

### Node Components

1. **Viral Script Generator Node** (`nodes/viral_script_generator_node.py`) **NEW!**
   - Uses Gemini 2.0 Thinking for intelligent script creation
   - Integrates full viral content research patterns and strategies
   - Implements iterative quality control with AI feedback loop
   - Progressive quality thresholds with variety tracking
   - Automatic session saving and detailed logging

2. **Scene Analyzer Node** (`nodes/scene_analyzer_node.py`)
   - Uses Google Gemini 2.5 Flash for intelligent script analysis
   - Breaks script into timed scenes with descriptions and keywords
   - Determines mood, action type, and optimal duration

3. **Prompt Generator Node** (`nodes/prompt_generator_node.py`)
   - Creates brand-aware, context-rich search queries for Pixabay API
   - Includes full "Wealthier Everyday" project context and financial education focus
   - Implements emotional intelligence and visual storytelling strategies
   - Generates primary and fallback search strategies with semantic scoring

4. **Video Fetcher Node** (`nodes/video_fetcher_node.py`)
   - Function-based Pixabay integration with semantic tag scoring
   - Downloads high-quality portrait videos (9:16 aspect ratio) 
   - Implements intelligent video selection based on relevance scoring
   - Robust error handling and fallback strategies

5. **Voiceover Node** (`nodes/voiceover_node.py`) **UPGRADING TO XTTS v2!**
   - Current: Edge-TTS for realistic AI voiceover generation
   - Upgrading to: Coqui XTTS v2 for emotion control and voice cloning
   - GPU acceleration ready with CUDA support
   - 2-5x better quality with custom voice training capability

6. **Professional Subtitle Node** (`nodes/professional_subtitle_node.py`)
   - Uses Whisper for accurate speech-to-text transcription
   - NLTK sentence segmentation for proper timing
   - Generates precise timing segments that sync with audio

7. **Video Assembly Node** (`nodes/video_assembly_node.py`)
   - MoviePy-based video compilation system
   - PIL-based subtitle rendering (no ImageMagick dependency)
   - Proper scene timing distribution and synchronization
   - YouTube Shorts optimization (1080x1920 resolution)

## 📁 Project Structure

```
ai-video-generator/
├── langgraph_pipeline.py      # Main orchestration pipeline (with viral script integration)
├── config.py                  # API keys configuration
├── input.txt                  # Script input file (optional - auto-generated now)
├── requirements.txt           # Python dependencies
├── HARDWARE_ASSESSMENT.md     # Complete system hardware analysis
├── VIRAL_CONTENT_RESEARCH.md  # Viral content patterns and strategies
├── nodes/                     # Pipeline node modules
│   ├── __init__.py
│   ├── viral_script_generator_node.py  # NEW: AI-powered script generation
│   ├── scene_analyzer_node.py
│   ├── prompt_generator_node.py
│   ├── video_fetcher_node.py
│   ├── voiceover_node.py      # Upgrading to XTTS v2
│   ├── professional_subtitle_node.py
│   └── video_assembly_node.py
├── debug/                     # Generation logs and session data
│   └── script_generation/     # Viral script generation debugging
├── output/                    # Generated videos (created automatically)
└── temp/                      # Temporary files (created automatically)
```

## 🔧 Customization

### Hardware Assessment & TTS Upgrade

The system includes a comprehensive hardware assessment (`HARDWARE_ASSESSMENT.md`) confirming compatibility with advanced TTS models:

**Your System Specifications:**
- ✅ AMD Ryzen 5 5600H (6C/12T) - Excellent for AI workloads
- ✅ 16GB RAM - More than sufficient for advanced models
- ✅ NVIDIA RTX 3050 (4GB VRAM) - Perfect for CUDA acceleration
- ✅ Fast NVMe SSD with 252GB available space

**Coqui XTTS v2 Upgrade Ready:**
- 2-5x better audio quality than current Edge-TTS
- Emotion control and voice cloning capabilities  
- GPU acceleration for faster generation
- Custom voice training with 5-30 second samples

### Viral Script Generation

The new AI-powered script generator creates engaging content automatically:

```python
# Test the viral script generator
from nodes.viral_script_generator_node import ViralScriptGeneratorNode

generator = ViralScriptGeneratorNode()
result = await generator.generate_viral_script(
    topic="passive income investing",
    target_duration=45,
    audience="millennials seeking financial freedom"
)
```

**Features:**
- Iterative quality improvement with AI feedback
- Viral research pattern integration
- Progressive quality thresholds (80% → 95%)
- Variety tracking to prevent repetition
- Detailed session logging for debugging

### Voice Options

Edit the voiceover node to change voice characteristics:

```python
# Available Edge-TTS voices
voices = [
    "en-US-AriaNeural",      # Female, American
    "en-US-JennyNeural",     # Female, American  
    "en-US-GuyNeural",       # Male, American
    "en-GB-SoniaNeural",     # Female, British
    "en-AU-NatashaNeural",   # Female, Australian
]
```

### Video Quality Settings

Modify video fetcher preferences:

```python
# In video_fetcher_node.py
def search_pixabay_videos(query, api_key, max_results=20):
    # Quality preferences: HD first, then lower quality
    # Orientation: vertical for YouTube Shorts (9:16)
    # Duration: minimum 10 seconds
    # Category: automatically determined by content analysis
```

### Subtitle Styling

Customize subtitle appearance:

```python
# In video_assembly_node.py
subtitle_style = {
    "font_size": 60,
    "font_color": "white",
    "stroke_color": "black",
    "stroke_width": 3,
    "position": "bottom"
}
```

## 🚨 Troubleshooting

### Common Issues

**Module not found errors**:
```bash
source ai_video_env/bin/activate
pip install -r requirements.txt
```

**FFmpeg not found**:
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/

**API rate limits**:
- Pixabay: 5,000 requests/hour (free tier)
- Gemini: 60 requests/minute (free tier)
- Wait or upgrade to higher tiers if needed

**Video generation slow**:
- First run downloads AI models (normal)
- Subsequent generations are much faster
- Processing time: ~2-5 minutes per video

**Subtitle sync issues**:
- Ensure audio file exists before subtitle generation
- Check Whisper model installation
- Verify NLTK data is downloaded

### Debug Mode

Enable verbose logging:

```bash
python langgraph_pipeline.py --debug
```

## 🎯 Best Practices

### Script Writing Tips

- **Hook viewers immediately**: Start with compelling statistics or questions
- **Keep sentences short**: 5-10 words per subtitle segment
- **Use specific numbers**: "90% of millionaires" vs "most millionaires"
- **Include actionable advice**: Give viewers something they can do
- **End with engagement**: Ask questions or provide calls-to-action

### Content Ideas

- **Financial Education**: Investment strategies, wealth-building habits, compound interest
- **Personal Finance**: Budgeting tips, saving strategies, debt elimination
- **Real Estate**: Property investment, market analysis, rental income strategies  
- **Business Growth**: Entrepreneurship, passive income, scaling strategies
- **Market Psychology**: Behavioral finance, decision-making, risk management
- **Success Stories**: Case studies, millionaire habits, transformation journeys

## 📊 Performance

### Typical Processing Times

- **Viral Script Generation**: 60-180 seconds (includes quality iterations)
- **Script Analysis**: 10-15 seconds
- **Video Fetching**: 30-60 seconds (depends on file sizes)
- **Voiceover Generation**: 10-20 seconds (Edge-TTS) / 5-15 seconds (XTTS v2)
- **Subtitle Generation**: 15-30 seconds
- **Video Assembly**: 60-120 seconds

**Total**: ~3-6 minutes per video (including viral script generation)

### Resource Usage

- **RAM**: 2-4 GB during processing
- **Storage**: ~500MB per generated video
- **CPU**: Intensive during video processing
- **Network**: ~100-300MB downloads per video

## 🔄 Updates and Maintenance

### Keeping Dependencies Updated

```bash
pip install --upgrade -r requirements.txt
```

### Model Updates

- Whisper models update automatically
- Gemini API improvements are applied server-side
- Edge-TTS voices may be updated by Microsoft

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest tests/

# Format code
black .
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Google Gemini** for AI-powered scene analysis and brand intelligence
- **OpenAI Whisper** for accurate speech recognition
- **Microsoft Edge-TTS** for high-quality voice synthesis
- **Pixabay** for providing premium stock video content with rich metadata
- **LangGraph** for pipeline orchestration framework
- **MoviePy** for video processing capabilities

---

**Ready to create amazing AI-generated financial education videos? Get started now!** 🚀💰
