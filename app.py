import threading
import time

from flask import Flask
app = Flask(__name__)

heartbeat_status_lock = threading.Lock()
heartbeat_status = {}

@app.route('/')
def status():
    now =  time.time()
    with heartbeat_status_lock:
        return {
            key:now-value
            for key, value in heartbeat_status.items()
        }

def listen():
    import datetime
    import dateutil.tz
    import socket
    import time

    timezone = dateutil.tz.gettz()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5555))

    print('Listening...')
    while True:
        try:
            data, addr = sock.recvfrom(1024, socket.MSG_DONTWAIT)
            data = data.decode('utf-8')
            timestamp = time.time()
            # print(f'{datetime.datetime.fromtimestamp(timestamp, timezone)}: {data}')
            with heartbeat_status_lock:
                heartbeat_status[data] = timestamp
        except BlockingIOError as e:
            time.sleep(0.05)

import os.path
def heartbeat(interval: float = 1.0, name: str = os.path.basename(os.path.dirname(os.path.realpath(__file__)))) -> None:
    import socket
    import time

    name_bytes = bytes(name, 'utf-8')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    while True:
        sock.sendto(name_bytes, ('255.255.255.255', 5555))
        time.sleep(interval)

if __name__ == '__main__':
    listen_thread = threading.Thread(target=listen, daemon=True).start()
    threading.Thread(target=heartbeat, daemon=True).start()

    app.run(use_reloader=False, host='0.0.0.0', port=8080)