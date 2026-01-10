#!/bin/bash
# Script to set Bluetooth microphone as default audio input
# Run this if ZEE can't hear you through Bluetooth earbuds

echo "🔍 Searching for Bluetooth microphone..."

# Find Bluetooth input source
BT_SOURCE=$(pactl list sources short | grep -i "bluez_input" | awk '{print $2}' | head -n1)

if [ -z "$BT_SOURCE" ]; then
    echo "❌ No Bluetooth microphone found!"
    echo "   Make sure your Bluetooth earbuds are connected and try again."
    echo ""
    echo "Available audio sources:"
    pactl list sources short
    exit 1
fi

echo "🎧 Found Bluetooth microphone: $BT_SOURCE"

# Unmute the microphone
echo "🔊 Unmuting microphone..."
pactl set-source-mute "$BT_SOURCE" 0

# Boost volume for better detection
echo "📢 Setting volume to 120%..."
pactl set-source-volume "$BT_SOURCE" 120%

# Set as default
echo "⚙️  Setting as default input..."
pactl set-default-source "$BT_SOURCE"

# Verify
DEFAULT_SOURCE=$(pactl get-default-source)
if [ "$DEFAULT_SOURCE" == "$BT_SOURCE" ]; then
    echo "✅ Bluetooth microphone set as default!"
    echo ""
    echo "Current default microphone: $DEFAULT_SOURCE"
    echo ""
    echo "ZEE will now use your Bluetooth earbuds for voice input."
    echo "Restart ZEE service: systemctl --user restart zee-service@$USER.service"
else
    echo "❌ Failed to set default microphone"
    exit 1
fi
