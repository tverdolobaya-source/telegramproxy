"""
Telegram Local Proxy - Готовое приложение
Версия 1.0 - Полностью рабочая, без root
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import threading
import socket
import select
import struct
import time
from datetime import datetime

Window.size = (400, 700)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

class LocalSOCKS5Proxy:
    def __init__(self, local_port=9050, callback=None):
        self.local_port = local_port
        self.running = False
        self.server_socket = None
        self.callback = callback
        self.connections = 0
        
    def log(self, message):
        if self.callback:
            self.callback(message)
    
    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind(('127.0.0.1', self.local_port))
            self.server_socket.listen(50)
            self.log("✅ Прокси запущен на порту 9050")
            
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    self.connections += 1
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except:
                    break
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        self.log("⏹️ Прокси остановлен")
    
    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(262)
            if not data or len(data) < 2 or data[0] != 0x05:
                return
            
            client_socket.send(b'\x05\x00')
            
            data = client_socket.recv(4)
            if not data or len(data) < 4:
                return
            
            addr_type = data[3]
            
            if addr_type == 0x01:
                addr = socket.inet_ntoa(client_socket.recv(4))
            elif addr_type == 0x03:
                addr_len = client_socket.recv(1)[0]
                addr = client_socket.recv(addr_len).decode()
            else:
                return
            
            port = struct.unpack('>H', client_socket.recv(2))[0]
            self.log(f"📡 Подключение к {addr}:{port}")
            
            response = struct.pack('!BBBx', 0x05, 0x00, 0x00) + \
                      struct.pack('!B', 0x01) + \
                      socket.inet_aton('127.0.0.1') + \
                      struct.pack('!H', self.local_port)
            client_socket.send(response)
            
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((addr, port))
            
            sockets = [client_socket, remote]
            
            while self.running:
                r, w, e = select.select(sockets, [], [], 1)
                
                for sock in r:
                    data = sock.recv(4096)
                    if not data:
                        return
                    
                    if sock == client_socket:
                        remote.send(data)
                    else:
                        client_socket.send(data)
                        
        except Exception as e:
            self.log(f"⚠️ Ошибка: {str(e)[:30]}")
        finally:
            try:
                client_socket.close()
                remote.close()
                self.connections -= 1
            except:
                pass

class TelegramProxyApp(App):
    def build(self):
        self.proxy = None
        self.proxy_thread = None
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text="🚀 Telegram Proxy",
            font_size='32sp',
            bold=True,
            color=(0.2, 0.6, 1, 1),
            size_hint_y=0.15
        )
        main_layout.add_widget(title)
        
        self.status_label = Label(
            text="🔴 Прокси остановлен",
            font_size='24sp',
            bold=True,
            color=(1, 0.2, 0.2, 1),
            size_hint_y=0.1
        )
        main_layout.add_widget(self.status_label)
        
        self.connections_label = Label(
            text="Соединений: 0",
            font_size='18sp',
            size_hint_y=0.1
        )
        main_layout.add_widget(self.connections_label)
        
        buttons_layout = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=12)
        
        self.start_btn = Button(
            text="▶️ ЗАПУСТИТЬ ПРОКСИ",
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='18sp',
            bold=True,
            size_hint_y=0.4
        )
        self.start_btn.bind(on_press=self.start_proxy)
        buttons_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text="⏹️ ОСТАНОВИТЬ",
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='18sp',
            bold=True,
            size_hint_y=0.4,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_proxy)
        buttons_layout.add_widget(self.stop_btn)
        
        main_layout.add_widget(buttons_layout)
        
        instruction = TextInput(
            text=(
                "📱 НАСТРОЙКА TELEGRAM:\n\n"
                "1. Запустите прокси кнопкой выше\n"
                "2. Откройте Telegram\n"
                "3. Настройки → Данные и память\n"
                "4. Прокси → Добавить прокси\n"
                "5. Выберите SOCKS5\n"
                "6. Сервер: 127.0.0.1\n"
                "7. Порт: 9050\n"
                "8. Нажмите ✅"
            ),
            multiline=True,
            readonly=True,
            size_hint_y=0.3,
            background_color=(0.95, 0.95, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        main_layout.add_widget(instruction)
        
        self.log_output = TextInput(
            text="Готов к работе. Нажмите 'Запустить прокси'\n",
            multiline=True,
            readonly=True,
            size_hint_y=0.2,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0, 1, 0, 1)
        )
        main_layout.add_widget(self.log_output)
        
        return main_layout
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        Clock.schedule_once(lambda dt: self._update_log(f"[{timestamp}] {message}"))
    
    def _update_log(self, message):
        self.log_output.text += f"{message}\n"
        lines = self.log_output.text.split('\n')
        if len(lines) > 50:
            self.log_output.text = '\n'.join(lines[-50:])
    
    def start_proxy(self, instance):
        self.log("▶️ Запуск прокси...")
        
        def run():
            self.proxy = LocalSOCKS5Proxy(callback=self.log)
            Clock.schedule_once(lambda dt: self.on_proxy_start())
            self.proxy.start()
        
        self.proxy_thread = threading.Thread(target=run)
        self.proxy_thread.daemon = True
        self.proxy_thread.start()
        
        Clock.schedule_interval(self.update_stats, 1)
    
    def on_proxy_start(self):
        self.status_label.text = "🟢 Прокси запущен"
        self.status_label.color = (0, 1, 0, 1)
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.log("✅ Прокси готов к работе")
    
    def update_stats(self, dt):
        if self.proxy:
            self.connections_label.text = f"Соединений: {self.proxy.connections}"
        return self.proxy is not None
    
    def stop_proxy(self, instance):
        self.log("⏹️ Остановка прокси...")
        if self.proxy:
            self.proxy.stop()
            self.proxy = None
        
        self.status_label.text = "🔴 Прокси остановлен"
        self.status_label.color = (1, 0.2, 0.2, 1)
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.connections_label.text = "Соединений: 0"
        self.log("✅ Прокси остановлен")
        return False

if __name__ == '__main__':
    TelegramProxyApp().run()