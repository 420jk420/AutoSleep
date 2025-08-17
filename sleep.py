import time
import os
import ctypes
from ctypes import wintypes
from pynput import mouse, keyboard
from threading import Timer
from tkinter import Tk, Label, Button
from colorama import init, Fore, Back

# Initialize colorama for console color handling
init()

# Set console colors to dark mode
os.system('color 07')  # This sets white text on a black background
print(Fore.LIGHTGREEN_EX + Back.BLACK + "Dark mode activated!" + Fore.RESET + Back.RESET)

# Time limit for inactivity (in seconds)
IDLE_TIME_LIMIT = 5400
NOTIFICATION_TIMEOUT = 60  # Time limit for user to respond to notification (in seconds)

# Global variables to keep track of the timer and notification state
timer = None
notification_active = False

# FLASHWINFO structure for FlashWindowEx
class FLASHWINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.wintypes.UINT),
        ("hwnd", ctypes.wintypes.HWND),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("uCount", ctypes.wintypes.UINT),
        ("dwTimeout", ctypes.wintypes.DWORD),
    ]

# Function to make the window flash orange (for Windows only)
def flash_window():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        FLASHW_ALL = 3  # Flash both caption and taskbar
        flash_info = FLASHWINFO(
            cbSize=ctypes.sizeof(FLASHWINFO),
            hwnd=hwnd,
            dwFlags=FLASHW_ALL,
            uCount=5,
            dwTimeout=0
        )
        ctypes.windll.user32.FlashWindowEx(ctypes.byref(flash_info))

# Function to create a dark-themed notification window
def show_notification_and_wait():
    global notification_active
    if notification_active:
        return False  # Prevent multiple notifications

    notification_active = True

    def on_ok():
        global notification_active
        notification_active = False
        root.destroy()
        put_pc_to_sleep()

    def on_cancel():
        global notification_active
        notification_active = False
        root.destroy()
        reset_timer()

    root = Tk()
    root.title("Sleep Notification")
    root.configure(bg="black")
    root.geometry("300x150")
    root.resizable(False, False)

    hwnd = ctypes.windll.user32.FindWindowW(None, "Sleep Notification")
    if hwnd:
        FLASHW_ALL = 3  # Flash both caption and taskbar
        flash_info = FLASHWINFO(
            cbSize=ctypes.sizeof(FLASHWINFO),
            hwnd=hwnd,
            dwFlags=FLASHW_ALL,
            uCount=5,
            dwTimeout=0
        )
        ctypes.windll.user32.FlashWindowEx(ctypes.byref(flash_info))

    Label(
        root,
        text="System is about to sleep.\nClick OK to proceed or Cancel to abort.",
        fg="gray",
        bg="black",
        wraplength=300,
        justify="center"
    ).pack(pady=20)

    Button(root, text="OK", command=on_ok, bg="black", fg="white").pack(side="left", padx=15, pady=1)
    Button(root, text="Cancel", command=on_cancel, bg="black", fg="white").pack(side="right", padx=15, pady=10, ipadx=25, ipady=25)

    root.protocol("WM_DELETE_WINDOW", on_cancel)  # Treat window close as cancel
    root.mainloop()

# Function to put the PC to sleep using a cancellable method
def put_pc_to_sleep():
    print("Sleep mode is now active.")
    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

# Function to reset the inactivity timer
def reset_timer():
    global timer
    if timer is not None:
        timer.cancel()
    # Combine idle time and notification timeout for a single countdown
    timer = Timer(IDLE_TIME_LIMIT, handle_inactivity)
    timer.start()

# Function to handle inactivity before showing the notification
def handle_inactivity():
    global timer
    print("Inactivity detected. Waiting for user response.")
    notif_timer = Timer(NOTIFICATION_TIMEOUT, force_sleep)
    notif_timer.start()
    show_notification_and_wait()
    notif_timer.cancel()  # Stop the force sleep timer if the user responds

# Function to force sleep if no response to the notification
def force_sleep():
    global notification_active
    if notification_active:
        print("No response received. Forcing sleep mode.")
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

# Mouse event handlers
def on_move(x, y):
    reset_timer()

def on_click(x, y, button, pressed):
    reset_timer()

def on_scroll(x, y, dx, dy):
    reset_timer()

# Keyboard event handlers
def on_press(key):
    reset_timer()

def on_release(key):
    reset_timer()

# Start the mouse listener
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
mouse_listener.start()

# Start the keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

# Initialize the timer
reset_timer()

try:
    # Keep the program running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    if timer:
        timer.cancel()
    mouse_listener.stop()
    keyboard_listener.stop()
    print("Program terminated.")
