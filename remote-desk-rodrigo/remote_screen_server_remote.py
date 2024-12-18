
from flask_cors import CORS
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import pyautogui
import cv2
import numpy as np
import base64
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button as ClickControler

app = Flask(__name__)

CORS(app) 
socketio = SocketIO(app, cors_allowed_origins="*") 

mouse = MouseController()
keyboard = KeyboardController()

@app.route('/')
def index():
    return send_from_directory('.', 'remote_screen_client_remote.html')

def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

@socketio.on('request_frame')
def handle_frame_request():
    frame = capture_screen()
    emit('frame', {'image': frame})

@socketio.on('keyboard_input')
def handle_keyboard_input(data):
    try:
        key = data['key']
        keyboard.press(key)
        keyboard.release(key)
    except Exception as e:
        print(f"Error handling keyboard input: {e}")

@socketio.on('mouse_input')
def handle_mouse_input(data):
    try:
        x, y = data['x'], data['y']
        mouse.position = (x, y)
    except Exception as e:
        print(f"Error handling mouse input: {e}")

@socketio.on('message')
def handle_mouse_click(data):
    x, y, click = data['x'], data['y'], data['click']
    mouse.position = (x, y)

    if(click == 'left'):
        mouse.click(ClickControler.left)
    elif(click == 'rigth'):
        mouse.click(ClickControler.right)
    else:
        return
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
