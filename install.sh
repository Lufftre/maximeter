#!/bin/bash
export DIR="$( cd "$( dirname "$( dirname "${BASH_SOURCE[0]}" )" )" >/dev/null 2>&1 && pwd )"

cat << EOF > /etc/systemd/system/maximeter.service
[Unit]
Description=MaxiMeter

[Service]
Type=simple
Restart=always
RestartSec=3
WorkingDirectory=$DIR
ExecStart=$DIR/bin/python3 maximeter.py

[Install]
WantedBy=multi-user.target
EOF

chmod +x /etc/systemd/system/maximeter.service
systemctl enable maximeter
systemctl restart maximeter