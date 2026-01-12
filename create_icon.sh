#!/bin/bash
# Create a simple ZEE icon using ImageMagick

if command -v convert &> /dev/null; then
    # Create a 256x256 icon with ZEE text
    convert -size 256x256 xc:'#4A90E2' \
        -gravity center \
        -pointsize 120 -font "DejaVu-Sans-Bold" \
        -fill white -annotate +0+0 'Z' \
        -pointsize 60 \
        -fill '#E8F4FF' -annotate +0+80 'AI' \
        ~/ZEE/zee_icon.png
    
    echo "✅ Icon created: ~/ZEE/zee_icon.png"
else
    echo "⚠️  ImageMagick not found. Using default microphone icon."
    echo "Install: sudo pacman -S imagemagick"
fi
