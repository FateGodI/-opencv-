import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageGrab, Image, ImageTk
import cv2
import numpy as np
import requests
from io import BytesIO
import threading
import time
import re

class QRScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("桌面二维码扫描器 (OpenCV版)")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.last_data = None
        self.running = True

        # 初始化 OpenCV 二维码检测器
        self.qr_detector = cv2.QRCodeDetector()

        self.create_widgets()
        self.scan_thread = threading.Thread(target=self.scan_loop, daemon=True)
        self.scan_thread.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """构建界面（同前）"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5, fill=tk.X)

        self.status_label = tk.Label(control_frame, text="状态：正在扫描...", fg="green")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(control_frame, text="停止扫描", command=self.stop_scan)
        self.btn_stop.pack(side=tk.RIGHT, padx=10)

        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.display_frame, wrap=tk.WORD, font=("微软雅黑", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.pack_forget()

        self.image_label = tk.Label(self.display_frame, bg="#f0f0f0")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.image_label.pack_forget()

        self.hint_label = tk.Label(self.display_frame, text="等待识别二维码...", font=("微软雅黑", 14), fg="gray")
        self.hint_label.pack(fill=tk.BOTH, expand=True)

    def scan_loop(self):
        """循环截屏并检测二维码（使用 OpenCV）"""
        while self.running:
            try:
                # 截取全屏
                screenshot = ImageGrab.grab()
                # 转换为 OpenCV 格式 (BGR)
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                # 检测二维码
                data, points, _ = self.qr_detector.detectAndDecode(frame)

                if data and data.strip():
                    if data != self.last_data:
                        self.last_data = data
                        self.root.after(0, self.handle_data, data)
                else:
                    if self.last_data is not None:
                        self.last_data = None
                        self.root.after(0, self.show_hint)

                time.sleep(1)
            except Exception as e:
                print(f"扫描出错: {e}")
                time.sleep(2)

    # 以下 handle_data、is_image_url、show_text、show_image_from_url、show_hint、stop_scan、on_closing 方法与之前完全相同
    def handle_data(self, data):
        self.status_label.config(text="状态：已识别", fg="blue")
        if self.is_image_url(data):
            self.show_image_from_url(data)
        else:
            self.show_text(data)

    def is_image_url(self, text):
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
        base_url = text.split('?')[0].lower()
        return base_url.endswith(image_extensions)

    def show_text(self, text):
        self.image_label.pack_forget()
        self.hint_label.pack_forget()
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)

    def show_image_from_url(self, url):
        try:
            response = requests.get(url, timeout=5)
            img_data = response.content
            pil_image = Image.open(BytesIO(img_data))
            pil_image.thumbnail((500, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(pil_image)

            self.text_area.pack_forget()
            self.hint_label.pack_forget()
            self.image_label.pack(fill=tk.BOTH, expand=True)

            self.image_label.config(image=photo)
            self.image_label.image = photo
        except Exception as e:
            self.show_text(f"图片加载失败：{str(e)}\n原始内容：{url}")

    def show_hint(self):
        self.text_area.pack_forget()
        self.image_label.pack_forget()
        self.hint_label.pack(fill=tk.BOTH, expand=True)
        self.status_label.config(text="状态：正在扫描...", fg="green")

    def stop_scan(self):
        self.running = False
        self.status_label.config(text="状态：已停止", fg="red")
        self.btn_stop.config(state=tk.DISABLED)

    def on_closing(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QRScannerApp(root)
    root.mainloop()