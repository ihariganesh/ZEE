#!/bin/bash
# ZEE AI Launcher Script

# Check if ZEE service is running
if systemctl --user is-active --quiet zee-service@${USER}.service; then
    # Service is running, show status
    notify-send "ZEE AI" "ZEE is already running! 🎤" -i audio-input-microphone
    
    # Ask user what to do
    ACTION=$(zenity --list --title="ZEE AI Control" \
        --text="ZEE is currently running. What would you like to do?" \
        --column="Action" \
        "View Logs" \
        "Restart ZEE" \
        "Stop ZEE" \
        --width=300 --height=250 2>/dev/null)
    
    case "$ACTION" in
        "View Logs")
            kitty -e tail -f ~/ZEE/logs/zee_service.log &
            ;;
        "Restart ZEE")
            systemctl --user restart zee-service@${USER}.service
            notify-send "ZEE AI" "ZEE is restarting..." -i audio-input-microphone
            ;;
        "Stop ZEE")
            systemctl --user stop zee-service@${USER}.service
            notify-send "ZEE AI" "ZEE has been stopped" -i audio-input-microphone
            ;;
    esac
else
    # Service is not running, start it
    notify-send "ZEE AI" "Starting ZEE... 🚀" -i audio-input-microphone
    systemctl --user start zee-service@${USER}.service
    sleep 2
    
    # Check if it started successfully
    if systemctl --user is-active --quiet zee-service@${USER}.service; then
        notify-send "ZEE AI" "ZEE is ready! Say 'Hey ZEE' to activate 🎤" -i audio-input-microphone -t 5000
    else
        notify-send "ZEE AI" "Failed to start ZEE. Check logs for details." -i error -u critical
    fi
fi
