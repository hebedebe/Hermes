splashtext = ["Importing libraries..."]

version = 1.2

g_domain = "https://hebedebe.github.io/Hermes"

logo = [
    "",
    ",--.  ,--.",
    "|  '--'  | ,---. ,--.--.,--,--,--. ,---.  ,---.",
    "|  .--.  || .-. :|  .--'|        || .-. :(  .-'",
    "|  |  |  |\   --.|  |   |  |  |  |\   --..-'  `)",
    "`--'  `--' `----'`--'   `--`--`--' `----'`----'",
    ""
    ]

patchnotes = """

Patch Notes
 - Fixed pressing the windows button crashing the program

"""

def addsplash(text):
    global splashtext
    splashtext.insert(0,"     "+text+"     ")

import os
import threading
from enum import Enum, auto
from sys import platform
import sys
try:
    import curses
except:
    addsplash("Installing windows-curses")
    os.system("pip3 install windows-curses")
    import curses
addsplash("Importing requests")
try:
    import requests
except:
    addsplash("Installing requests module")
    os.system("pip3 install requests")
    import requests
addsplash("Importing time")
import time
addsplash("Importing pickle")
import pickle
addsplash("Importing colorama")
try:
    import colorama
except:
    addsplash("Installing colorama")
    os.system("pip3 install colorama")
    import colorama
addsplash("Importing urllib.request")
try:
    import urllib.request
except:
    addsplash("Installing urllib")
    os.system("pip3 install urllib")
    import urllib.request
addsplash("Importing deepcopy from copy")
from copy import deepcopy
addsplash("Importing random")
import random
addsplash("Importing atexit")
import atexit
addsplash("Importing urllib")
import urllib

try:
    import ssl
except:
    addsplash("Installing ssl")
    os.system("pip3 install ssl")
    import ssl

try:
    import certifi
except:
    addsplash("Installing certifi")
    os.system("pip3 install certifi")
    import certifi

from urllib.request import urlopen

v = True
if platform == "darwin":
    logo = ""
    v=False
    addsplash("Verification disabled")

sec = context=ssl.create_default_context(cafile=certifi.where())

class Page(Enum):
    LOADING = auto()
    UPDATEPROMPT = auto()
    UPDATE = auto()
    MENU = auto()
    CHAT = auto()

page = Page.LOADING

addsplash("Initialising curses terminal")

stdscr = curses.initscr()

addsplash("Disabling curses echo")

curses.noecho()

addsplash("Initialising curses terminal")

curses.cbreak()

addsplash("Hiding terminal cursor")

curses.curs_set(False)

#addsplash("Enabling keypad support")

#curses.keypad(stdscr, true);

def resizeHandler():
    global stdscr
    y, x = stdscr.getmaxyx()
    print(y,x)
    minx = 120
    miny = 30
    if y < miny:
        y = miny
    if x < minx:
        x = minx
    while True:
        resize = curses.is_term_resized(y, x)
        if resize is True:
            y, x = stdscr.getmaxyx()
            stdscr.clear()
            curses.resize_term(y, x)
            stdscr.refresh()

addsplash("Starting resizeHandler")
threading.Thread(target=resizeHandler, daemon=True).start()

addsplash("Loading curses colour pairs")

if curses.has_colors():
    curses.start_color()
    curses.use_default_colors()
    try:
        for i in range(0, curses.COLOR_PAIRS-1):
            curses.init_pair(i + 1, i, -1)
    except:
        for i in range(0, curses.COLORS-1):
            curses.init_pair(i + 1, i, -1)
    if ("debug" in sys.argv):
        try:
            for i in range(0, 255):
                stdscr.addstr(str(i), curses.color_pair(i))
        except curses.ERR:
            pass
        stdscr.refresh()
        time.sleep(5)

def clear():
    global stdscr
    for y in range(curses.LINES):
        for x in range(curses.COLS-1):
            stdscr.addstr(y, x, " ")

def startup():
    global version, splashtext, logo, page, stdscr
    logo_col = 35
    logo_line = 5
    splashoffset = logo_line+8
    n = 0
    TPS = 0
    while True:
        if page == Page.LOADING:
            start_time = time.time() # start time of the loop
            clear()
            n+=1
            stdscr.addstr(0, 0, f"Hermes V{str(version)}")
            stdscr.addstr(1, 0, f"Platform: {platform}")
            stdscr.addstr(2, 0, f"n: {str(n)}")
            stdscr.addstr(3, 0, f"TPS: {str(round(TPS))}")

            _ = 0
            for i in logo:
                stdscr.addstr(logo_line+_, logo_col, i, curses.color_pair(7))
                _+= 1

            offset = 0
            for i in splashtext:
                if offset+splashoffset > curses.LINES-1:
                    continue
                i_ = i
                stdscr.addstr(offset+splashoffset, round((curses.COLS/2)-(len(i_)/2)), i_, curses.color_pair(7))
                offset += 1

            stdscr.refresh()
            TPS=(1.0 / ((time.time() - start_time)+0.01))

threading.Thread(target=startup, daemon=True).start()

#addsplash("Initialising Colorama")
#colorama.init()

addsplash(f"Hermes version {str(version)}")

addsplash(f"Running on {str(platform)}")

addsplash("Retrieving JSON data...")

#time.sleep(2)

data = requests.get(f"{g_domain}/hermes_data.json", verify=v).json()

servers = data["servers"]

addsplash(f"Server list recieved")

notifications = data["notifications"]

addsplash(f"Downloaded notifications")

latestver = data["latestversion"]
latestverstable = data["stable"]
latestverurgent = data["urgent"]

addsplash(f"Got latest version ({latestver})")

selection_ = 0

#stdscr.nodelay(1)

def updateinput():
    global page, selection_, stdscr
    while page == Page.UPDATEPROMPT:
        c = stdscr.getch()
        if c == ord("d"):
            selection_ = 1
        elif c == ord("a"):
            selection_ = 0
        if c == ord("\n") or c == ord(" "):
            if selection_ == 0:
                page = Page.UPDATE
            else:
                clear()
                stdscr.refresh()
                #threading.Thread(target=startup, daemon=True).start()
                page = Page.LOADING

if (latestver > version):
    page = Page.UPDATEPROMPT
    if latestverurgent:
        page = Page.UPDATE
    else:
        selected = curses.init_pair(255, curses.COLOR_BLACK, curses.COLOR_WHITE)
        umsg = f"Your installation of Hermes (V{version}) is outdated. Install V{latestver}?"
        threading.Thread(target=updateinput, daemon=True).start()
        clear()
        while page == Page.UPDATEPROMPT:
            stdscr.addstr(round(curses.LINES*0.3),round(curses.COLS/2-(len(umsg)/2)), umsg)
            if selection_ == 0:
                stdscr.addstr(round(curses.LINES*0.3)+3,round(curses.COLS/2)-4-9, "[INSTALL]", curses.color_pair(255))
                stdscr.addstr(round(curses.LINES*0.3)+3,round(curses.COLS/2)+4, "[POSTPONE]")
            elif selection_ == 1:
                stdscr.addstr(round(curses.LINES*0.3)+3,round(curses.COLS/2)-4-9, "[INSTALL]")
                stdscr.addstr(round(curses.LINES*0.3)+3,round(curses.COLS/2)+4, "[POSTPONE]", curses.color_pair(255))
            stdscr.refresh()
    if page == Page.UPDATE:
        clear()
        stdscr.addstr(0,0,f"Downloading Hermes V{latestver}... (this may take a while)")
        stdscr.refresh()
        path = os.path.dirname(__file__)
        ftype_ = "Hermes.exe"
        if platform == "darwin" or platform == "linux" or platform == "linux2":
            ftype_ = "Hermes.py"
        with urllib.request.urlopen(f"{g_domain}/{ftype_}") as upd:
            with open(path+"/"+ftype_, "wb+") as f:
                stdscr.addstr(1,0,f"Writing program to {path+'/'+ftype_}")
                stdscr.refresh()
                f.write(upd.read())
        #urllib.request.urlretrieve("https://hebedebe.github.io/chess2.0/Hermes.exe", "Hermes.exe")
        stdscr.addstr(2,0,"The program will now restart to complete installation.")
        stdscr.refresh()
        time.sleep(1)
        try:
            if platform == "win32":
                os.system("cls")
                os.system(path+'\\'+ftype_)
            else:
                os.system("clear")
                try:
                    os.system(f"python {path+'/'+ftype_}")
                except:
                    os.system(f"python3 {path+'/'+ftype_}")
        except:
            stdscr.addstr(1,0,"Program failed to execute. Please restart the program manually")
            stdscr.refresh()
            time.sleep(3)
        exit()

colour = str(random.randint(2,32))
addsplash("Randomised user colour")

if len(colour) < len("10"):
    colour = "0"+colour
    addsplash("Corrected user colour")

domain = None
addsplash("Set domain to None")

connected = False

addsplash("Setting GET request timeout to 1.5 seconds")
timeout_ = 1.5

addsplash(f"Connecting to servers...")

for i in servers:
    domain = i
    addsplash(f"Attempting connection to server {domain}... ({servers.index(i)+1} of {len(servers)})")
    try:
        r_ = requests.get(domain, timeout=1.5)
        if r_.status_code != 200:
            addsplash(f"Recieved error code <{r_.status_code}>")
        elif r_.status_code == 200:
            addsplash(f"Connected successfully!")
            connected = True
            break
    except Exception as e:
        addsplash("Connection failed.")
        #print(e)

if not connected:
    addsplash("Could not connect to any servers. Please try again later")
    while True:
        pass

keylen = 32

addsplash("Loading user key...")

try:
    if os.path.isfile("key.txt"):
        f = open("key.txt", "r")
        key = f.read()
        f.close()
        addsplash("Key retrieved")
    else:
        addsplash("No key file detected")
        addsplash("Creating key file")
        f = open("key.txt", "x")
        f.close()
        f = open("key.txt", "w")
        key = ""
        addsplash("Generating user key")
        for i in range(keylen):
            chnum = random.randint(33,126)
            while chnum == 34 or chnum == 96 or ch(chnum) == "\\":
                chnum = random.randint(33,126)
            key = key+chr(chnum)
        addsplash("Writing key to key file")
        f.write(key)
        f.close()
        addsplash("Key generation complete")
except:
    addsplash("Key generation/detection failed.")
    key = None

addsplash(f"Key: {key}\n")

print(f"\nNotifications\n{patchnotes}\n")

username = ""

def usernameinput():
    global username, stdscr, page
    while page == Page.MENU:
        try:
            chcode = stdscr.getch()
            keypressed = chr(chcode)
            if keypressed == "\n":
                page = Page.CHAT
            elif keypressed == "\b" or chcode == 127:
                username = username[:len(username)-1]
            else:
                if chcode == 34:
                    username = username+'"'
                else:
                    username = username+keypressed
        except:
            pass


time.sleep(0.5)
page = Page.MENU
threading.Thread(target=usernameinput, daemon=True).start()
clear()
logo_col = 35
logo_line = 5
username = ""
while page == Page.MENU:
    stdscr.addstr(0, 0, f"Hermes V{str(version)}")
    stdscr.addstr(1, 0, f"Platform: {platform}")
    _ = 0
    for i in logo:
        stdscr.addstr(logo_line+_, logo_col, i, curses.color_pair(7))
        _+= 1
    username_ = "     "+username+"_     "
    stdscr.addstr(round(curses.LINES*0.3+7),round(curses.COLS/2-(len("Enter Username:")/2)), "Enter Username:")
    stdscr.addstr(round(curses.LINES*0.3+10),round(curses.COLS/2-(len(username_)/2)), username_)
    stdscr.addstr(curses.LINES-1, 0, f"Key: {key}")

    stdscr.refresh()

clear()

stdscr.addstr(0, 0, f"Hermes V{str(version)}")
stdscr.addstr(1, 0, f"Platform: {platform}")
_ = 0
for i in logo:
    stdscr.addstr(logo_line+_, logo_col, i, curses.color_pair(7))
    _+= 1
username_ = "     "+username+"_     "
stdscr.addstr(round(curses.LINES*0.3+7),round(curses.COLS/2-(len("Loading...")/2)), "Loading...")
stdscr.addstr(curses.LINES-1, 0, f"Key: {key}")

stdscr.refresh()

channel = "main"

if len(username) > 16:
    username = username[:16]

messages = []

def get_msg():
    global domain, messages
    response = requests.get(domain+f"/{channel}")
    data = response.json()
    messages = data["messages"]

def send_msg(msg):
    global channel, messages, colour, inpt
    if msg.split()[0] == "|CMD|":
        response = requests.post(domain+f"/{channel}", data=(f"{key}{colour}{msg}".encode(encoding="UTF-8")))
        inpt = ""
        stdscr.addstr(curses.LINES-3, 0, " "*curses.COLS)
        stdscr.addstr(curses.LINES-1, 0, f"Sent admin command                                ")
    elif msg[0] != "!":
        response = requests.post(domain+f"/{channel}", data=(f"{key}{colour}[{username}] {msg}".encode(encoding="UTF-8")))
    else:
        if msg == "!version":
            stdscr.addstr(curses.LINES-1, 0, f"Hermes v{version}")
        elif msg[0:4] == "!key":
            stdscr.addstr(curses.LINES-1, 0, 'Key: "'+key+'"')
        elif msg[0:8] == "!channel":
            requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} left the channel.)".encode(encoding="UTF-8")))
            channel = msg[8:].strip()
            requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} entered the channel.)".encode(encoding="UTF-8")))
            stdscr.addstr(curses.LINES-1, 0, f"Switched to channel {channel}                             ")
            messages = ["00Loading channel...","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]
        elif msg[0:7] == "!colour":
            colour_ = deepcopy(colour)
            colour = msg.split()[1]
            if len(colour) < len("10"):
                colour = "0"+colour
            if len(colour) < len("1") or len(colour) > len("10"):
                colour = colour_
            stdscr.addstr(curses.LINES-1, 0, f"Changed colour to index <#{colour}>                             ")
        elif msg[0:3] == "!dm":
            pass #send a dm

def msghandler():
    while __name__ == "__main__":
        get_msg()
        time.sleep(1)

inpt = ""

def inputhandler():
    global inpt, stdscr
    while __name__ == "__main__":
        try:
            chcode = stdscr.getch()
            keypressed = chr(chcode)
            if keypressed == "\n":
                send_msg(inpt)
                stdscr.addstr(curses.LINES-3, 0, " "*curses.COLS)
                inpt = ""
            elif keypressed == "\b" or chcode == 127:
                inpt = inpt[:len(inpt)-1]
            else:
                if chcode == 34:
                    inpt = inpt+'"'
                else:
                    inpt = inpt+keypressed
        except:
            pass

requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} joined.)".encode(encoding="UTF-8")))
get_msg()

def exit_handler():
    requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} disconnected.)".encode(encoding="UTF-8")))

atexit.register(exit_handler)

threading.Thread(target=msghandler, daemon=True).start()
#threading.Thread(target=inputhandler, daemon=True).start()

page = Page.CHAT

clear()

stdscr.nodelay(1)

while __name__ == "__main__":
    try:
        try:
            chcode = stdscr.getch()
            keypressed = chr(chcode)
            if keypressed == "\n":
                send_msg(inpt)
                stdscr.addstr(curses.LINES-3, 0, " "*curses.COLS)
                inpt = ""
            elif keypressed == "\b" or chcode == 127:
                inpt = inpt[:len(inpt)-1]
            else:
                if chcode == 34:
                    inpt = inpt+'"'
                else:
                    inpt = inpt+keypressed
        except:
            pass

        stdscr.addstr(0, 0, f"//{channel}          ")
        stdscr.addstr(curses.LINES-4, 0, "-"*curses.COLS)
        stdscr.addstr(curses.LINES-3, 0, "> "+inpt+" "*(curses.COLS-len("> "+inpt)-1))

        for i in range(len(messages))[:curses.LINES-5]:
            if len(messages[i]) > curses.COLS-2:
                messages[i] = messages[i][:curses.COLS-2]
            stdscr.addstr(curses.LINES-5-i, 0, messages[i][2:]+" "*(curses.COLS-len(messages[i])-1), curses.color_pair(int(messages[i][:2])))
    except:
        if b'\x00' in inpt.encode("utf-8"):
            inpt = inpt[:len(inpt)-1]

    stdscr.refresh()
