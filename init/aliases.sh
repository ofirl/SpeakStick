alias ss-logs="sudo journalctl -u speakstick"
alias ss-server-logs="sudo journalctl -u speakstick-management-server"
alias ss-restart="sudo systemctl restart speakstick speakstick-management-server"

alias cdss="cd /opt/SpeakStick"
alias ss-update="git pull && ss-restart && echo \"service restarted\""