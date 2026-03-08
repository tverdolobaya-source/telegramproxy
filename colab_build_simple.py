"""
Скопируйте этот код в Google Colab и запустите
Затем загрузите main.py и buildozer.spec через Files
"""

# Ячейка 1: Установка зависимостей
print("📦 Установка зависимостей...")
!apt-get update -qq
!apt-get install -y -qq openjdk-17-jdk
!pip install -q buildozer cython==0.29.33

# Ячейка 2: Проверка файлов
print("\n📁 Проверка файлов...")
import os
if os.path.exists('main.py') and os.path.exists('buildozer.spec'):
    print("✅ Файлы найдены!")
else:
    print("❌ Загрузите main.py и buildozer.spec через Files слева!")
    print("Нажмите на значок папки 📁 → Upload")

# Ячейка 3: Сборка APK
print("\n🔨 Сборка APK (это займет 10-15 минут)...")
!buildozer android debug

# Ячейка 4: Скачивание APK
print("\n📥 Скачивание APK...")
from google.colab import files
import os

if os.path.exists('bin'):
    apk_files = [f for f in os.listdir('bin') if f.endswith('.apk')]
    if apk_files:
        apk_path = f'bin/{apk_files[0]}'
        print(f"✅ APK готов: {apk_files[0]}")
        files.download(apk_path)
    else:
        print("❌ APK не найден в папке bin/")
else:
    print("❌ Папка bin/ не создана. Проверьте ошибки сборки выше.")
