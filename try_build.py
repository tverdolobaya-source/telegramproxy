#!/usr/bin/env python3
"""
Скрипт для попытки сборки APK с разными версиями Python
"""
import subprocess
import sys
import os

def check_python_version(version):
    """Проверяет доступность версии Python"""
    try:
        result = subprocess.run(
            [f'py', f'-{version}', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def try_build_with_version(version):
    """Пытается собрать APK с указанной версией Python"""
    print(f"\n🔧 Попытка сборки с Python {version}...")
    
    venv_name = f"venv{version.replace('.', '')}"
    
    try:
        # Создаем виртуальное окружение
        print(f"Создание виртуального окружения {venv_name}...")
        subprocess.run([f'py', f'-{version}', '-m', 'venv', venv_name], check=True)
        
        # Активируем и устанавливаем buildozer
        pip_path = os.path.join(venv_name, 'Scripts', 'pip.exe')
        print("Установка buildozer...")
        subprocess.run([pip_path, 'install', 'buildozer', 'cython==0.29.33'], check=True)
        
        # Запускаем сборку
        buildozer_path = os.path.join(venv_name, 'Scripts', 'buildozer.exe')
        print("Запуск сборки APK...")
        subprocess.run([buildozer_path, 'android', 'debug'], check=True)
        
        print(f"\n✅ Сборка успешна! APK в папке bin/")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при сборке: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def main():
    print("🚀 Автоматическая сборка Telegram Proxy APK")
    print("=" * 50)
    
    # Проверяем текущую версию
    print(f"\nТекущая версия Python: {sys.version}")
    
    # Список версий для попытки (от новых к старым)
    versions_to_try = ['3.11', '3.10', '3.9', '3.8']
    
    print("\n🔍 Поиск подходящих версий Python...")
    available_versions = []
    
    for version in versions_to_try:
        if check_python_version(version):
            print(f"✅ Python {version} найден")
            available_versions.append(version)
        else:
            print(f"❌ Python {version} не найден")
    
    if not available_versions:
        print("\n⚠️ Подходящие версии Python не найдены!")
        print("\n📋 Рекомендации:")
        print("1. Установите Python 3.10 с https://www.python.org/downloads/")
        print("2. Или используйте Google Colab (build_on_colab.ipynb)")
        print("3. Или используйте GitHub Actions (загрузите проект на GitHub)")
        return
    
    # Пробуем собрать с первой доступной версией
    for version in available_versions:
        if try_build_with_version(version):
            break
    else:
        print("\n❌ Не удалось собрать APK ни с одной версией Python")
        print("\n📋 Используйте альтернативные методы из README.md")

if __name__ == '__main__':
    main()
