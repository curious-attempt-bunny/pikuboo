# Pikuboo

Are your [piku](https://github.com/piku/piku) apps running on your raspberry pi(s)? Deploy `pikuboo` to a piku server to track the last heartbeat time for all the piku apps on your local network.

# Deploy to piku

```bash
git remote add piku $PIKU_SERVER:pikuboo
git push piku master
```

See [Using piku](https://github.com/piku/piku#using-piku).

# Send a heartbeat

```python
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

import threading
threading.Thread(target=heartbeat, daemon=True).start()
```

# Running locally

```
python3 -m venv .venv
source .venv/bin/activate
python app.py
```

