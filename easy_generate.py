#!/usr/bin/env python3
"""
InVideo AI Quality Video Generator Interface for Wealthier Everyday
Professional-grade video generation with Google Gemini AI
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from ai_video_generator import ProfessionalAIVideoGenerator
    import config
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all requirements are installed:")
    print("   source ai_video_env/bin/activate")
    print("   pip install -r requirements.txt")
    sys.exit(1)

def setup_api_keys():
    """Setup API keys for enhanced functionality"""
    print("🔑 API Key Setup (Optional but Recommended)")
    print("=" * 50)
    
    # Check if config has real API keys
    gemini_key = getattr(config, 'GEMINI_API_KEY', 'your_gemini_api_key_here')
    
    if gemini_key == 'your_gemini_api_key_here' or not gemini_key:
        print("\n🤖 Google Gemini API Key Setup:")
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Create a free account")
        print("3. Generate an API key (FREE - 60 requests/minute)")
        print("4. Copy the key")
        
        use_gemini = input("\nDo you want to enter your Gemini API key now? (y/n): ").lower()
        if use_gemini in ['y', 'yes']:
            gemini_key = input("Enter your Gemini API key: ").strip()
            
            # Save to config file
            config_path = Path("config.py")
            content = config_path.read_text()
            content = content.replace('GEMINI_API_KEY = "your_gemini_api_key_here"', 
                                    f'GEMINI_API_KEY = "{gemini_key}"')
            config_path.write_text(content)
            print("✅ Gemini API key saved!")
        else:
            print("📝 Using fallback analysis (still works great!)")
            gemini_key = None
    
    return gemini_key

def get_user_input():
    """Get script and preferences from user"""
    print("\n🎬 InVideo AI Quality Video Generator!")
    print("=" * 50)
    
    print("\n📝 Enter your script (press Enter twice when done):")
    script_lines = []
    empty_line_count = 0
    
    while True:
        line = input()
        if line == "":
            empty_line_count += 1
            if empty_line_count >= 2 or (empty_line_count >= 1 and script_lines):
                break
        else:
            empty_line_count = 0
            script_lines.append(line)
    
    script = "\n".join(script_lines)
    
    if not script.strip():
        print("❌ No script provided!")
        return None, None
    
    print(f"\n📄 Your script: {len(script)} characters")
    print(f"💭 Words: {len(script.split())} words")
    print(f"⏱️ Estimated duration: {len(script.split()) * 0.4:.1f} seconds")
    
    video_title = input("\n🎯 Enter video title (or press Enter for auto-generated): ").strip()
    if not video_title:
        # Auto-generate title from first few words
        first_words = script.split()[:4]
        video_title = "_".join(first_words).replace(",", "").replace(".", "")
        video_title = ''.join(c for c in video_title if c.isalnum() or c == '_')
    
    return script, video_title

async def main():
    """Main function for professional video generation"""
    try:
        print("🎬 Welcome to InVideo AI Quality Video Generator!")
        print("🎯 Professional-grade faceless videos for YouTube Shorts")
        print("💯 Completely FREE with no watermarks!")
        
        # Setup API keys
        gemini_key = setup_api_keys()
        
        while True:
            # Get user input
            script, title = get_user_input()
            
            if not script:
                continue
            
            # Generate video
            print(f"\n🚀 Generating InVideo AI quality video: {title}")
            print("⏳ This may take 3-5 minutes for professional quality...")
            
            generator = ProfessionalAIVideoGenerator(gemini_api_key=gemini_key)
            video_path = await generator.generate_professional_video(script, title)
            
            print(f"\n✅ SUCCESS! Your professional video is ready!")
            print(f"📁 Location: {video_path}")
            print(f"📱 Perfect for YouTube Shorts upload!")
            print(f"🎯 Quality: InVideo AI Professional Grade")
            
            # Ask if user wants to generate another
            while True:
                another = input("\n🎬 Generate another video? (y/n): ").strip().lower()
                if another in ['y', 'yes']:
                    break
                elif another in ['n', 'no']:
                    print("\n🎉 Thanks for using InVideo AI Quality Video Generator!")
                    print("💚 Happy creating content for Wealthier Everyday!")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Video generation cancelled. See you next time!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Solutions:")
        print("1. Make sure all requirements are installed")
        print("2. Check your internet connection")
        print("3. Verify API keys if using Gemini")
        print("4. Try running: source ai_video_env/bin/activate")

if __name__ == "__main__":
    asyncio.run(main())
