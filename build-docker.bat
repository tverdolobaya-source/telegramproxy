@echo off
echo Building APK using Docker...
docker build -t telegram-proxy-builder .
docker run -v "%cd%:/app" telegram-proxy-builder
echo APK should be in bin/ folder
pause
