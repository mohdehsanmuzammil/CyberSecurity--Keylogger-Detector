import psutil
from pynput import keyboard
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

# Suspicious keywords
suspicious_keywords = ["keylogger", "spy", "logger", "hack"]

# Keyboard counter
key_count = 0
KEY_THRESHOLD = 50

running = False

# GUI update function
def log_message(msg):
    output_box.insert(tk.END, msg + "\n")
    output_box.see(tk.END)

# Process monitoring
def monitor_processes():
    global running
    while running:
        for process in psutil.process_iter(['pid', 'name']):
            try:
                name = process.info['name'].lower()
                for keyword in suspicious_keywords:
                    if keyword in name:
                        log_message(f"⚠️ Suspicious process: {name}")
            except:
                pass
        time.sleep(5)

# Keyboard monitoring
def on_press(key):
    global key_count
    key_count += 1
    
    if key_count > KEY_THRESHOLD:
        log_message("⚠️ High keyboard activity detected!")
        key_count = 0

def monitor_keyboard():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start button
def start_monitoring():
    global running
    running = True
    log_message("🚀 Monitoring Started...")
    
    threading.Thread(target=monitor_processes, daemon=True).start()
    threading.Thread(target=monitor_keyboard, daemon=True).start()

# Stop button
def stop_monitoring():
    global running
    running = False
    log_message("🛑 Monitoring Stopped.")

# GUI window
root = tk.Tk()
root.title("Cyber Security Tool - Keylogger Detector")
root.geometry("600x400")

# Buttons
start_btn = tk.Button(root, text="Start", command=start_monitoring, bg="green", fg="white")
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop", command=stop_monitoring, bg="red", fg="white")
stop_btn.pack(pady=5)

# Output box
output_box = scrolledtext.ScrolledText(root, width=70, height=20)
output_box.pack(pady=10)

root.mainloop()