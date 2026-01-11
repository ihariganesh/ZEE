# Bluetooth Microphone Setup Guide for ZEE 🎧

## Problem Solved ✅
Your Bluetooth earbuds ("Immortal 181") were connected but:
1. ❌ Not set as default input device
2. ❌ **MUTED** by system
3. ❌ Volume was too low (100%)

## What Was Fixed 🔧

### 1. Set Bluetooth as Default Input
```bash
pactl set-default-source bluez_input.E1:2D:49:DB:67:10
```

### 2. Unmuted Microphone
```bash
pactl set-source-mute bluez_input.E1:2D:49:DB:67:10 0
```

### 3. Boosted Volume to 120%
```bash
pactl set-source-volume bluez_input.E1:2D:49:DB:67:10 120%
```

### 4. Updated ZEE Code
- Added ALSA error suppression (no more warnings)
- Optimized microphone settings for Bluetooth:
  - Energy threshold: 200 (high sensitivity)
  - Dynamic adjustment enabled
  - Shorter pause detection (0.8s)
- ZEE now uses system default microphone (respects PipeWire/PulseAudio settings)

## Current Status 🟢

✅ **Bluetooth microphone**: Set as default  
✅ **Mute status**: Unmuted  
✅ **Volume**: 120% (boosted for better detection)  
✅ **ZEE service**: Running and listening  
✅ **Audio detection**: Working! (ZEE is hearing audio)  

**Current behavior**: ZEE is detecting audio from your Bluetooth earbuds, showing "❌ Could not understand audio" which means:
- ✅ Microphone is working
- ✅ Audio is being captured
- ⚠️ Need to speak more clearly/loudly for Google Speech Recognition to transcribe

## Quick Commands 📝

### Check Bluetooth Mic Status
```bash
pactl list sources | grep -A 20 "bluez_input" | grep -E "Name:|State:|Volume:|Mute:"
```

### Run Setup Script (Auto-configure)
```bash
./setup_bluetooth_mic.sh
```

### Test Microphone
```bash
python test_microphone.py
```

### Restart ZEE Service
```bash
systemctl --user restart zee-service@$USER.service
```

### View ZEE Logs
```bash
tail -f ~/ZEE/logs/zee_service.log
```

## Tips for Best Results 🎯

### Speaking to ZEE
1. **Speak clearly and loudly** - Bluetooth mics are less sensitive than wired
2. **Get close to the mic** - 6-12 inches from earbuds is ideal
3. **Reduce background noise** - Quiet environment helps recognition
4. **Pronounce "Hey ZEE"** clearly - Wake word detection needs clear audio

### Testing Your Setup
Run the test script to verify everything works:
```bash
cd ~/ZEE
python test_microphone.py
```

This will:
- Check ambient noise levels
- Test voice recognition
- Verify wake word detection
- Show diagnostic information

### If ZEE Still Can't Hear You

1. **Check Bluetooth connection mode:**
   - Must be in "Headset" mode (with microphone)
   - Not just "Audio Sink" (music only)

2. **Test with system recorder:**
   ```bash
   # Record 5 seconds
   arecord -d 5 -f cd test.wav
   
   # Play it back
   aplay test.wav
   ```
   If you can't hear yourself, Bluetooth mic isn't working properly.

3. **Check PipeWire/PulseAudio:**
   ```bash
   # Verify Bluetooth source is running
   pactl list sources short | grep RUNNING
   
   # Should show: bluez_input.E1:2D:49:DB:67:10
   ```

4. **Restart Bluetooth service:**
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

5. **Reconnect earbuds:**
   - Disconnect Bluetooth earbuds
   - Wait 5 seconds
   - Reconnect in "Headset" profile
   - Run `./setup_bluetooth_mic.sh` again

## Automated Setup Script 🤖

The `setup_bluetooth_mic.sh` script automatically:
1. Finds your Bluetooth microphone
2. Sets it as default input
3. Unmutes it
4. Boosts volume to 120%
5. Shows confirmation

**Run after every reboot or when earbuds reconnect:**
```bash
./setup_bluetooth_mic.sh
```

## Permanent Solution (Auto-setup on Boot)

To automatically configure Bluetooth mic on startup, add to `~/.profile` or `~/.bash_profile`:

```bash
# Auto-configure Bluetooth microphone for ZEE
if [ -f "$HOME/ZEE/setup_bluetooth_mic.sh" ]; then
    bash "$HOME/ZEE/setup_bluetooth_mic.sh" > /dev/null 2>&1
fi
```

Or create a systemd user service to run the script before ZEE starts.

## What Changed in Code 📄

### voice_handler.py
- Added ALSA error suppression (ctypes handler)
- Removed device enumeration (caused PyAudio crashes)
- Uses `sr.Microphone()` default (respects system settings)
- Optimized for Bluetooth with lower energy threshold (200)
- Better error handling for calibration

### New Files
- **setup_bluetooth_mic.sh** - Auto-configure Bluetooth mic
- **test_microphone.py** - Diagnostic tool for testing mic

### Updated Files
- **README.md** - Added Bluetooth troubleshooting section

## Commit Details 📦
```
Commit: fcd3de2
Message: Add Bluetooth microphone support - unmute and volume boost
Files: 5 changed, 232 insertions(+), 15 deletions(-)
```

---

## Next Steps 🚀

1. **Test right now**: Say "Hey ZEE" out loud (speak clearly and loudly)
2. **Check logs**: `tail -f ~/ZEE/logs/zee_service.log`
3. **If not working**: Run `python test_microphone.py` to diagnose
4. **Adjust volume**: If still too quiet, increase to 150%:
   ```bash
   pactl set-source-volume bluez_input.E1:2D:49:DB:67:10 150%
   ```

## Support 💬

If you're still having issues:
1. Run diagnostics: `python test_microphone.py`
2. Check logs: `tail -50 ~/ZEE/logs/zee_service.log`
3. Verify Bluetooth: `pactl list sources | grep bluez -A 10`
4. Test with arecord: `arecord -d 3 test.wav && aplay test.wav`

---

**Your Bluetooth earbuds are now configured and ZEE is listening!** 🎉
