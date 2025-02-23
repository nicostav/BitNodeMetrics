#!/bin/bash

# Check if run with root rights
if [ "$EUID" -ne 0 ]
  then echo "[!] Please run as root"
  exit
fi

# Create service user / System User - No Home - No Login
user_exists(){ id -u "bitnodemetrics" &>/dev/null; } 
if user_exists "$1"; code=$?; then 
    echo 'User bitnodemetrics already exists'
else
    sudo useradd -r -M -s /usr/sbin/nologin bitnodemetrics
    echo "[*] User bitnodemetrics created"
fi

# Create etc directories needed
if [ -d "/etc/bitnodeui" ]; then
    echo "[?] Directory /etc/bitnodeui/ already exists"
else
    sudo mkdir /etc/bitnodeui
    echo "[*] Directory /etc/bitnodeui/ created"
fi

if [ -d "/etc/bitnodeui/metrics" ]; then
    echo "[?] Directory /etc/bitnodeui/metrics already exists"
else
    sudo mkdir /etc/bitnodeui/metrics
    echo "[*] Directory /etc/bitnodeui/metrics created"
fi
sudo chown bitnodemetrics:bitnodemetrics /etc/bitnodeui/metrics

# Copy python
if [ -f "source/metrics-service.py" ]; then
    if [ -f "/etc/bitnodeui/metrics/metrics-service.py" ]; then
        echo "[?] File /etc/bitnodeui/metrics/metrics-service.py already exists"
    else
        sudo cp source/metrics-service.py /etc/bitnodeui/metrics/
        sudo chown bitnodemetrics:bitnodemetrics /etc/bitnodeui/metrics/metrics-service.py
        sudo chmod +x /etc/bitnodeui/metrics/metrics-service.py
        echo "[*] File /etc/bitnodeui/metrics/metrics-service.py created"
    fi
else
    echo "[!] Source file for metrics-service.py does not exist"
    exit
fi

if [ -f "source/metrics.db" ]; then
    if [ -f "/etc/bitnodeui/metrics/metrics.db" ]; then
        echo "[?] File /etc/bitnodeui/metrics/metrics.db already exists"
    else
        sudo cp source/metrics.db /etc/bitnodeui/metrics/
        sudo chown bitnodemetrics:bitnodemetrics /etc/bitnodeui/metrics/metrics.db
        echo "[*] File /etc/bitnodeui/metrics/metrics.db created"
    fi
else
    echo "[!] Source file for metrics.db does not exist"
    exit
fi

# Configure Service
if [ -f "source/bitnode-metrics.service" ]; then
    if [ -f "/etc/systemd/system/bitnode-metrics.service" ]; then
        echo "[?] File /etc/systemd/system/bitnode-metrics.service already exists"
    else
        sudo cp source/bitnode-metrics.service /etc/systemd/system
        echo "[*] File /etc/systemd/system/bitnode-metrics.service created"
    fi
else
    echo "[!] Source file for bitnode-metrics.service does not exist"
    exit
fi

if [ -f "source/bitnode-metrics.timere" ]; then
    if [ -f "/etc/systemd/system/bitnode-metrics.timer" ]; then
        echo "[?] File /etc/systemd/system/bitnode-metrics.timer already exists"
    else
        sudo cp source/bitnode-metrics.timer /etc/systemd/system
        echo "[*] File /etc/systemd/system/bitnode-metrics.timer created"
    fi
else
    echo "[!] Source file for bitnode-metrics.timer does not exist"
    exit
fi

# Reload and enable/start service
sudo systemctl daemon-reload
sudo systemctl enable bitnode-metrics.timer
sudo systemctl start bitnode-metrics.timer