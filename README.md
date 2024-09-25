# Introduction

Welcome to the Text-to-Video Generator! This tool is designed to transform your written script into engaging short-form videos, perfect for uploading into platforms like YouTube Shorts, TikTok, and more. It's perfect if you want to use AI to make some kind of brainrot video and earn passive income from it. If you don't have a script, AI will automatically generate one for you, so don't worry.

<p align="center">
  <img src="https://i.imgur.com/kLopbZ2.gif" alt="animated" />
</p>

# How to use

## Environment Setup

```
python -m venv .
bin/pip install -r requirements.txt
```

Rename the `.env.example` file to `.env` and fill the API key inside

- **Note:** The project used [MoviePy](https://pypi.org/project/moviepy/) to compose the video, which required [ImageMagick](https://imagemagick.org/index.php) to be installed in your machine
- **Another note:** It's required about 4 GB of RAM to run.

## Inference

You can simply run

```
bin/python app.py
```

then the script and video will auto generate for you.

Or using your own script

```
bin/python app.py -s "insert some funny story here"
```

## Showcase

Here is some demo videos which script is auto generate using AI

https://github.com/user-attachments/assets/bf629766-18bd-420b-9ab3-c061a9631baa

https://github.com/user-attachments/assets/09da3d9b-bffb-4b27-b422-33b7327229fd
