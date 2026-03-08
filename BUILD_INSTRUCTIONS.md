# Инструкция по сборке APK

## Проблема
На Windows с Python 3.15 buildozer не работает напрямую.

## Решения:

### Вариант 1: GitHub Actions (РЕКОМЕНДУЕТСЯ)
1. Создайте репозиторий на GitHub
2. Загрузите все файлы проекта
3. GitHub автоматически соберет APK
4. Скачайте готовый APK из раздела Actions → Artifacts

### Вариант 2: Docker (если установлен Docker Desktop)
```bash
build-docker.bat
```

### Вариант 3: Установить WSL2
```powershell
wsl --install
# Перезагрузите компьютер
# Затем в WSL:
sudo apt update
sudo apt install python3-pip git
pip3 install buildozer
buildozer android debug
```

### Вариант 4: Использовать Python 3.10
1. Установите Python 3.10 с python.org
2. Создайте виртуальное окружение:
```bash
py -3.10 -m venv venv310
venv310\Scripts\activate
pip install buildozer
buildozer android debug
```

### Вариант 5: Онлайн-сервисы
- Google Colab (бесплатно)
- Replit (бесплатно)
- GitHub Codespaces

## Результат
APK файл будет в папке `bin/`
