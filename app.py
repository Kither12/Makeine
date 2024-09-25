import os
from src.video_generator import generate_video
from dotenv import load_dotenv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from text.")
    parser.add_argument("-s", "--script", type=str,
                        help="The script for the video")
    args = parser.parse_args()
    load_dotenv()
    generate_video(args.script)
