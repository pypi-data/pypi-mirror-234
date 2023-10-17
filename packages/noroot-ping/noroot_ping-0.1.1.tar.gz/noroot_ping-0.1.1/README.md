# noroot_ping
Simple python bindings to rust's tokio tcp ping function.

## Installation
```
pip install noroot_ping
```

## Usage
```
from noroot_ping import ping_tcp

if ping_tcp(ip, port):
    # if ping was successful
else:
    # if ping was NOT successful
```
