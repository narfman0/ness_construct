import ctypes, pytesseract, re, time
import win32api, win32con, win32gui
from PIL import Image, ImageGrab
from input import SendInput, KEYEVENTF_KEYUP, Keyboard, KEY_A, VK_LEFT, VK_RIGHT, VK_UP, VK_DOWN

hWnd = 0
bbox = []
debug = False
#directions = {0: VK_UP, 1: VK_RIGHT, 2: VK_DOWN, 3: VK_LEFT}
directions = {0: VK_LEFT, 1: VK_RIGHT}
steps_max = 30
steps_current = steps_max

def send_key(key):
    """ emulate win32api keypresses, down then up per input """
    SendInput(Keyboard(key))
    time.sleep(0.1)
    SendInput(Keyboard(key, KEYEVENTF_KEYUP))

def window_enumerate(hwnd, extra):
    """ win32 callback enumerating all windows, need to get hwnd """
    if 'Snes9X' in win32gui.GetWindowText(hwnd):
        global hWnd
        global bbox
        hWnd = hwnd
        bbox = win32gui.GetWindowRect(hwnd)

if __name__ == '__main__':
    win32gui.EnumWindows(window_enumerate, None)
    direction = 0
    while 1:
        im = ImageGrab.grab(bbox=bbox)
        result = pytesseract.image_to_string(im)
        if debug and result:
            print result
        # before input ensure window is activated
        win32gui.SetForegroundWindow(hWnd)
        if 'gained' in result:
            send_key(KEY_A)
            print 'post combat, gg noobs'
        elif 'engage' in result:
            print 'engaged oh noez'
        elif 'Bash' in result:
            # make sure Goods isnt selected. if there's any funky character
            # between bash and goods, select other move
            result = re.search('Bash(.*)Goods', result)
            if result and result.group(1):
                print "there's some dumb character between bash and goods %s, changing!" % result.group(1)
                send_key(VK_RIGHT)
            # select BASH
            send_key(KEY_A)
            # select mob to attack
            send_key(KEY_A)
            print 'omg combat!'
        else:
            steps_current -= 1
            if steps_current <= 0:
                direction = (direction + 1) % len(directions)
                steps_current = steps_max
            send_key(directions[direction])
        time.sleep(.1)
