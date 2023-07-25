# checkport
A simple API for retrieving the client's IP and checking if the IP:port is accessible.

# systemd service

[Unit]
Documentation=https://github.com/elab100/checkport
Description=CheckPort Service
After=network.target

[Service]
Type=simple
DynamicUser=yes
WorkingDirectory=/opt/checkport
ExecStart=/opt/checkport/checkport.py

[Install]
WantedBy=multi-user.target
