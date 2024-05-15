#!/bin/bash

# Обновление и установка необходимых пакетов
sudo apt-get update
sudo apt-get install -y curl gnupg2

# Добавление ключа и репозитория OpenResty
sudo apt-key adv --fetch-keys 'https://openresty.org/package/pubkey.gpg'
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y "deb http://openresty.org/package/ubuntu $(lsb_release -sc) main"

# Установка OpenResty
sudo apt-get update
sudo apt-get install -y openresty

# Установка pip и Flask для графического интерфейса
sudo apt-get install -y python3-pip
pip3 install -r requirements.txt

# Getting a list of IP addresses of the current node
node_ips="$(hostname -I)"
# Converting a string to an array
IFS=' ' read -ra ip_array <<< "$node_ips"
node_ip="${ip_array[0]}"

sudo mkdir -p /var/www/sparkline_creater
sudo cp ./index.html /var/www/sparkline_creater/
# Создание конфигурационного файла для OpenResty
sudo tee /usr/local/openresty/nginx/conf/nginx.conf > /dev/null <<EOL
worker_processes 1;
events {
    worker_connections 1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  $node_ip;

        location / {
            root   /var/www/sparkline_creater/;
            index  index.html index.htm;
        }

        location /api/ {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOL

# Перезапуск OpenResty
sudo systemctl restart openresty

cat << EOF | sudo tee /etc/systemd/system/sparkline_creater.service
[Unit]
Description=Sparkline Creater
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
PrivateTmp=true

WorkingDirectory=$(pwd)
ExecStart=/bin/python3 $(pwd)/src/app.py

User=$(whoami)
Group=$(id -gn)
StandardOutput=journal
StandardError=inherit
LimitNOFILE=65535
LimitNPROC=4096
LimitAS=infinity
LimitFSIZE=infinity
TimeoutStopSec=0
TimeoutStartSec=75

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable sparkline_creater
sudo systemctl start sparkline_creater
