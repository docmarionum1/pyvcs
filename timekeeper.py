import time
#print(time.time())
#print("%.20f" % time.time())

MHZ = 1190000
SECONDS_PER_TICK = 1 / MHZ
start = time.time()
previous = start
#target = start + 1
#previous = start
ticks = 0
while True:
    ticks = ticks + 1
    #previous = time.time()
    if ticks % MHZ == 0:
        current = time.time()
        print("%.20f" % (1- ( current - previous)))
        previous = current
        #start = time.time()
        #ticks = 0

    sleep = (ticks / MHZ) - (time.time() - start)# - .00001
    if sleep > 0:
        time.sleep(sleep)
    #current = time.time()
    #delta = current - previous
    #if current - previous
