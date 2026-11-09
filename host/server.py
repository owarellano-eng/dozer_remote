"""Dozer Remote LAN host. Local-network only; no internet relay or firewall bypass."""
from __future__ import annotations
import secrets
import socket
import threading
import time
from functools import wraps

from flask import Flask, Response, jsonify, request, session, send_from_directory
import mss
from PIL import Image
import io
import pyautogui

app = Flask(__name__, static_folder="web", static_url_path="")
app.secret_key = secrets.token_bytes(32)
PAIR_CODE = f"{secrets.randbelow(1_000_000):06d}"
LOCK = threading.Lock()
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.02

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

def paired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("paired"):
            return jsonify(error="Pair this browser first."), 401
        return fn(*args, **kwargs)
    return wrapper

@app.get("/")
def home():
    return send_from_directory("web", "index.html")

@app.post("/api/pair")
def pair():
    data = request.get_json(silent=True) or {}
    if not secrets.compare_digest(str(data.get("code", "")), PAIR_CODE):
        return jsonify(error="Incorrect pairing code."), 403
    session.clear()
    session["paired"] = True
    return jsonify(ok=True)

@app.post("/api/unpair")
def unpair():
    session.clear()
    return jsonify(ok=True)

@app.get("/api/status")
@paired
def status():
    return jsonify(ok=True, width=pyautogui.size().width, height=pyautogui.size().height)

@app.get("/api/screen.jpg")
@paired
def screen():
    with mss.mss() as grabber:
        shot = grabber.grab(grabber.monitors[1])
        image = Image.frombytes("RGB", shot.size, shot.rgb)
        image.thumbnail((1440, 900))
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=65, optimize=True)
    return Response(output.getvalue(), mimetype="image/jpeg", headers={"Cache-Control":"no-store"})

@app.post("/api/mouse")
@paired
def mouse():
    data = request.get_json(silent=True) or {}
    width, height = pyautogui.size()
    x = max(0, min(width - 1, int(float(data.get("x", 0)) * width)))
    y = max(0, min(height - 1, int(float(data.get("y", 0)) * height)))
    with LOCK:
        pyautogui.moveTo(x, y)
        if data.get("click") in ("left", "right"):
            pyautogui.click(button=data["click"])
    return jsonify(ok=True)

@app.post("/api/input")
@paired
def input_action():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    with LOCK:
        if action == "type":
            value = str(data.get("text", ""))[:500]
            pyautogui.write(value, interval=0.005)
        elif action == "key":
            key = str(data.get("key", ""))[:24]
            allowed = {"enter","esc","tab","backspace","delete","space","up","down","left","right","home","end","pageup","pagedown","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"}
            if key not in allowed:
                return jsonify(error="Key not allowed."), 400
            pyautogui.press(key)
        else:
            return jsonify(error="Unknown action."), 400
    return jsonify(ok=True)

if __name__ == "__main__":
    ip = local_ip()
    print("\nDozer Remote LAN host")
    print(f"Open http://{ip}:8765 on a device on the SAME trusted network.")
    print(f"Pairing code: {PAIR_CODE}")
    print("Keep this terminal private. Press Ctrl+C to stop.\n")
    app.run(host="0.0.0.0", port=8765, threaded=True, debug=False)
