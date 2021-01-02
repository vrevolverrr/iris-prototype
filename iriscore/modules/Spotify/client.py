import win32gui
import win32api
import win32con

class Client:
    @classmethod
    def start_playback(cls):
        hwnd = win32gui.FindWindow(None, "Spotify Premium")
        if hwnd == 0:
            raise Exception("Spotify not running")
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.SetForegroundWindow(hwnd)
        win32api.keybd_event(0x20, 0, 0, 0)
        win32api.keybd_event(0x20, 0, win32con.KEYEVENTF_KEYUP, 0)