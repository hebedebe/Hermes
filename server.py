#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from copy import deepcopy
import socket
import github

version = 0.4

token = #insert token

print(f"Hermes server version {version}")

IP = socket.gethostbyname(socket.gethostname())

print(f"Hosting on IP {IP}")

default_messages = ["00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]

g_domain = "https://hebedebe.github.io/Hermes"

print("retrieving admin keys from admin_keys.json")
admin_keys = requests.get(f"{g_domain}/admin_keys.json").json()["keys"]
print(admin_keys)

print("retrieving banned keys from banned_keys.json")
banned_keys = requests.get(f"{g_domain}/banned_keys.json").json()["keys"]
print(banned_keys)

print("retrieving server data from hermes_data.json")
server_data = requests.get(f"{g_domain}/hermes_data.json").json()
print(server_data)

g = github.Github(token)

repo = g.get_user().get_repo("Hermes")
file = repo.get_contents("hermes_data.json")

sha = file.sha

if f"http://{IP}:80" in server_data["servers"]:
    server_data["servers"].remove(f"http://{IP}:80")

server_data["servers"].insert(0, f"http://{IP}:80")


repo.update_file("hermes_data.json", "Added ip to server list", json.dumps(server_data), sha)
print("Added IP to list")

messages = {
    "main":deepcopy(default_messages)
}

keylen = 32

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def log_message(self, format, *args):
        return

    def do_GET(self):
        global messages
        self._set_headers()
        if self.path == "/":
            return
        channel = self.path[1:]
        try:
            msg_ = messages[channel]
        except:
            print(f"Created channel {channel}")
            messages[channel] = deepcopy(default_messages)
            msg_ = messages[channel]
        self.wfile.write(json.dumps({"messages":messages[channel][:25]}).encode(encoding="UTF-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        global messages, banned_keys, admin_keys
        if self.path == "/":
            return
        channel = self.path[1:]
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode(encoding="UTF-8")
        print(post_data)
        key = post_data[:keylen]
        #print(key)
        if key in banned_keys:
            return
        if key in admin_keys:
            msg_ = post_data[keylen+2:].split()
            #print(msg_)
            if msg_[0] == "|CMD|":
                cmd = msg_[1]
                try:
                    args = msg_[2:]
                except:
                    args = False
                if cmd == "ban":
                    for i in args:
                        banned_keys.append(i)
                        print(f"Banned ({i})")
                if cmd == "unban":
                    for i in args:
                        banned_keys.remove(i)
                        print(f"Unbanned ({i})")
                elif cmd == "listadmins":
                    for i in admin_keys:
                        messages[channel].insert(0,"00"+i)
                elif cmd == "clear":
                    if args:
                        for i in args:
                            messages[i] = deepcopy(default_messages)
                    else:
                        messages[channel] = deepcopy(default_messages)
                return

        try:
            msg_ = messages[channel]
        except:
            print(f"Created channel {channel}")
            messages[channel] = deepcopy(default_messages)
            msg_ = messages[channel]
        colour = post_data[keylen:keylen+2]
        try:
            colour = int(colour)
        except:
            post_data = post_data[:keylen]+"00"+post_data[keylen+2:]
        if key in admin_keys:
            messages[channel].insert(0,post_data[keylen:keylen+2]+"☣ "+post_data[keylen+2:])
        else:
            messages[channel].insert(0,post_data[keylen:])
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
