import time

from framework.hub import Hub
from framework.client import Client

h = Hub('0.0.0.0', 8485)
c1 = Client('127.0.0.1', 8485, client_id=101)
c2 = Client('127.0.0.1', 8485, client_id=102)
c3 = Client('127.0.0.1', 8485, client_id=103)

c1.send(b'hi')
c2.send(b'how are you?')
c3.send(b'hello world')
time.sleep(1)
print(c2.clients_data)  # Shows data received from c1(101) and c3(103)
print(c3.clients_data)  # Shows data received from c2(102) and c1(101)
