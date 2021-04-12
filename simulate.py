from socketcan import CanRawSocket
from can import iso_address_claim, polar_performance
import random
import time
s = CanRawSocket('can0')

iso_address_claim_frame = iso_address_claim()

i = 0
performance = 95
while True:
    i += 1
    if i % 10 == 0:
        s.send(iso_address_claim_frame)

    x = random.randint(0, 1) - 0.5
    performance += x
    print(performance)
    polar_performance_frame = polar_performance(performance)
    s.send(polar_performance_frame)

    time.sleep(0.5)
