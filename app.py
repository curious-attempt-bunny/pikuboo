import time
import threading
import dateutil.tz

from flask import Flask
app = Flask(__name__)

timezone = dateutil.tz.gettz()

heartbeat_status_lock = threading.Lock()
heartbeat_status = {}

@app.route('/')
def status():
    with heartbeat_status_lock:
        return heartbeat_status


def listen():
    import datetime
    import socket
    import time

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5555))

    print('Listening...')
    while globals().get('__file__', None):
        try:
            data, addr = sock.recvfrom(1024, socket.MSG_DONTWAIT)
            data = data.decode('utf-8')
            timestamp = time.time()
            # print(f'{datetime.datetime.fromtimestamp(timestamp, timezone)}: {data}')
            with heartbeat_status_lock:
                heartbeat_status[data] = timestamp
        except BlockingIOError as e:
            time.sleep(0.05)

    print('Done listening.')

def heartbeat(interval: float) -> None:
    import socket
    import time

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while globals().get('__file__', None):
        sock.sendto(bytes(__file__, 'utf-8'), ('0.0.0.0', 5555))
        time.sleep(interval)
    print('Done heartbeating.')


if __name__ == '__main__':
    threading.Thread(target=listen).start()
    threading.Thread(target=heartbeat, args=[1]).start()

    app.run(use_reloader=False, host='0.0.0.0', port=8080)