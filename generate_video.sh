#!/bin/bash

# Activate virtual environment and run AI video generator
echo "🎬 Starting AI Video Generator for Wealthier Everyday..."
echo "=================================================="

# Activate the virtual environment
source ai_video_env/bin/activate

# Check if Python packages are available
python -c "import moviepy, edge_tts, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required packages not found. Installing..."
    pip install -r requirements.txt
fi

# Run the AI video generator
echo "🚀 Generating your video..."
python ai_video_generator.py

echo "✅ Video generation complete!"
echo "📁 Check the 'output' folder for your video"
