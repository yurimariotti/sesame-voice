#!/usr/bin/env bash
# Custom build script for Render
pip install --upgrade pip
pip install --no-deps -r requirements.txt
pip install flask gunicorn requests websocket-client numpy
