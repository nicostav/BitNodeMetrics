#!/bin/bash

# Create service user / System User - No Home - No Login
sudo useradd -r -M -s /usr/sbin/nologin bitnodemetrics

# Create etc directories needed
sudo mkdir /etc/bitnodeui
sudo mkdir /etc/bitnodeuimetrics
sudo chown bitnodemetrics:bitnodemetrics /etc/bitnodeui/metrics

# Copy python
sudo cp source/metrics-service.py /etc/bitnodeui/metrics/
sudo chown bitnodemetrics:bitnodemetrics /etc/bitnodeui/metrics/metrics-service.py
sudo chmod +x /etc/bitnodeui/metrics/metrics-service.py
sudo touch /etc/bitnodeui/metrics/metrics.db
sudo chown bitnodemetrics:bitnodemetrics /etc/bitnodeui/metrics/metrics.db

# Configure Service
sudo cp source/bitnode-metrics.service source/bitnode-metrics.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bitnode-metrics.timer
sudo systemctl start bitnode-metrics.timer