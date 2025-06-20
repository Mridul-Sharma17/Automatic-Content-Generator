# 🎬 AI-Powered Faceless Video Generator

A fully automated, AI-powered video generation system that transforms text scripts into professional YouTube Shorts with realistic voiceover, synchronized subtitles, and relevant stock footage.

## ✨ Features

- 🤖 **AI-Powered Scene Analysis** - Intelligent script breakdown using Google Gemini 2.5 Flash
- 🎵 **Realistic Voiceover** - High-quality AI voice synthesis with Edge-TTS
- 📹 **Stock Video Integration** - Automatic video fetching from Pexels API with smart querying
- 📝 **Professional Subtitles** - Whisper-based transcription with perfect timing synchronization
- 🎬 **Automated Assembly** - MoviePy-based video compilation with proper transitions
- 📱 **YouTube Shorts Ready** - Perfect 9:16 aspect ratio, optimized for vertical viewing
- 🔄 **LangGraph Orchestration** - Modular pipeline architecture for reliability and scalability

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg installed on your system
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

5. **Generate your first video**:
```bash
python langgraph_pipeline.py
```

## 📋 Configuration

### Required API Keys

1. **Google Gemini API** (Free tier: 60 requests/minute)
   - Get from: https://makersuite.google.com/app/apikey
   - Used for: AI scene analysis and script breakdown

2. **Pexels API** (Free tier: 200 requests/hour)
   - Get from: https://www.pexels.com/api/
   - Used for: Stock video footage

### Setup

1. Open `config.py`
2. Replace placeholder values with your actual API keys:

```python
GEMINI_API_KEY = "your_gemini_api_key_here"
PEXELS_API_KEY = "your_pexels_api_key_here"
```

## 📝 Usage

### Basic Usage

1. **Edit your script**: Open `input.txt` and write your video script
2. **Run the pipeline**: Execute `python langgraph_pipeline.py`
3. **Wait for processing**: The system will automatically:
   - Analyze your script with AI
   - Generate search queries for relevant videos
   - Download stock footage from Pexels
   - Create AI voiceover with Edge-TTS
   - Generate synchronized subtitles
   - Assemble the final video
4. **Find your video**: Check the `output/` directory for your generated video

### Example Script

```text
Did you know that 90% of millionaires invest in real estate? Here's why property investment is the secret to building lasting wealth. First, real estate provides passive income through rental payments. Second, property values typically appreciate over time. Third, you get tax benefits that reduce your overall tax burden. Start small with a single rental property and watch your wealth grow automatically.
```

## 🏗️ Architecture

The system uses a **LangGraph-based pipeline** with modular nodes:

### Pipeline Flow

```
📄 Script Input → 🤖 Scene Analysis → 🔍 Prompt Generation → 📹 Video Fetching
                                                                         ↓
🎬 Video Assembly ← 📝 Subtitle Generation ← 🎵 Voiceover Generation ←───┘
```

### Node Components

1. **Scene Analyzer Node** (`nodes/scene_analyzer_node.py`)
   - Uses Google Gemini 2.5 Flash for intelligent script analysis
   - Breaks script into timed scenes with descriptions and keywords
   - Determines mood, action type, and optimal duration

2. **Prompt Generator Node** (`nodes/prompt_generator_node.py`)
   - Creates optimized search queries for Pexels API
   - Generates primary and fallback search strategies
   - Categorizes content for better video matching

3. **Video Fetcher Node** (`nodes/video_fetcher_node.py`)
   - Downloads high-quality portrait videos (9:16 aspect ratio)
   - Implements rate limiting and quality preferences
   - Prevents duplicates with `used_video_ids` tracking

4. **Voiceover Node** (`nodes/voiceover_node.py`)
   - Generates realistic AI voiceover using Edge-TTS
   - Produces high-quality audio with perfect duration timing
   - Supports multiple voices and languages

5. **Professional Subtitle Node** (`nodes/professional_subtitle_node.py`)
   - Uses Whisper for accurate speech-to-text transcription
   - NLTK sentence segmentation for proper timing
   - Generates precise timing segments that sync with audio

6. **Video Assembly Node** (`nodes/video_assembly_node.py`)
   - MoviePy-based video compilation system
   - PIL-based subtitle rendering (no ImageMagick dependency)
   - Proper scene timing distribution and synchronization
   - YouTube Shorts optimization (1080x1920 resolution)

## 📁 Project Structure

```
ai-video-generator/
├── langgraph_pipeline.py      # Main orchestration pipeline
├── config.py                  # API keys configuration
├── input.txt                  # Script input file
├── requirements.txt           # Python dependencies
├── nodes/                     # Pipeline node modules
│   ├── __init__.py
│   ├── scene_analyzer_node.py
│   ├── prompt_generator_node.py
│   ├── video_fetcher_node.py
│   ├── voiceover_node.py
│   ├── professional_subtitle_node.py
│   └── video_assembly_node.py
├── output/                    # Generated videos (created automatically)
└── temp/                      # Temporary files (created automatically)
```

## 🔧 Customization

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
quality_preferences = ["hd", "sd"]  # Prefer HD, fallback to SD
orientation = "portrait"            # For YouTube Shorts (9:16)
duration_min = 10                   # Minimum video duration in seconds
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
- Pexels: 200 requests/hour (free tier)
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

- Financial tips and advice
- Investment strategies
- Wealth-building habits
- Money mistakes to avoid
- Success stories and case studies
- Market analysis and trends

## 📊 Performance

### Typical Processing Times

- **Script Analysis**: 10-15 seconds
- **Video Fetching**: 30-60 seconds (depends on file sizes)
- **Voiceover Generation**: 10-20 seconds
- **Subtitle Generation**: 15-30 seconds
- **Video Assembly**: 60-120 seconds

**Total**: ~2-5 minutes per video

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

- **Google Gemini** for AI-powered scene analysis
- **OpenAI Whisper** for accurate speech recognition
- **Microsoft Edge-TTS** for high-quality voice synthesis
- **Pexels** for providing free stock video content
- **LangGraph** for pipeline orchestration framework
- **MoviePy** for video processing capabilities

---

**Ready to create amazing AI-generated videos? Get started now!** 🚀
