# 🚀 Telegram Local Proxy - APK Builder

## 📱 О приложении
Локальный SOCKS5 прокси для Telegram без root-доступа.

## ⚠️ Проблема сборки на Windows
Buildozer не работает на Windows с Python 3.15. Используйте один из методов ниже.

## 🎯 БЫСТРЫЙ СПОСОБ: Google Colab (5 минут)

1. Откройте https://colab.research.google.com/
2. Загрузите файл `build_on_colab.ipynb`
3. Загрузите `main.py` и `buildozer.spec` через Files (слева)
4. Запустите все ячейки (Runtime → Run all)
5. Скачайте готовый APK

## 🐙 GitHub Actions (автоматическая сборка)

1. Создайте репозиторий на GitHub
2. Загрузите все файлы
3. Перейдите в Actions
4. Запустите workflow "Build APK"
5. Скачайте APK из Artifacts

## 🐳 Docker (если установлен)

```bash
docker build -t telegram-proxy-builder .
docker run -v "%cd%:/app" telegram-proxy-builder
```

APK будет в папке `bin/`

## 🐧 WSL2 (Linux на Windows)

```powershell
# Установка WSL
wsl --install

# После перезагрузки в WSL:
sudo apt update
sudo apt install -y python3-pip git openjdk-17-jdk
pip3 install buildozer cython==0.29.33
buildozer android debug
```

## 📦 Альтернатива: Python 3.10

Если у вас есть Python 3.10:

```bash
py -3.10 -m venv venv310
venv310\Scripts\activate
pip install buildozer
buildozer android debug
```

## 📋 Что делает приложение

- Создает локальный SOCKS5 прокси на порту 9050
- Работает без root
- Простой интерфейс на Kivy
- Логирование подключений

## 🔧 Настройка в Telegram

1. Запустите приложение
2. Нажмите "Запустить прокси"
3. В Telegram: Настройки → Данные и память → Прокси
4. Добавить прокси → SOCKS5
5. Сервер: 127.0.0.1, Порт: 9050

## 📝 Файлы проекта

- `main.py` - основной код приложения
- `buildozer.spec` - конфигурация сборки
- `build_on_colab.ipynb` - для сборки в Google Colab
- `.github/workflows/build-apk.yml` - для GitHub Actions
- `Dockerfile` - для Docker

## 💡 Рекомендация

Самый простой способ - использовать **Google Colab**. Не требует установки ничего на ваш компьютер.
