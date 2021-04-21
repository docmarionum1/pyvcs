import dis
import opcode
import sys
import threading
import time

HZ = 3580000
SECONDS_PER_TICK = 1 / HZ
TICKS_PER_CYCLE = 10000

#target = start + 1
#previous = start
ticks = 6510000
user_ticks = 0

run_timekeepr = True

lock = threading.Lock()
#lock = threading.Condition()

def timekeeper():
    start = time.time()
    previous = start

    global ticks
    while run_timekeepr:
        #with lock:
            #print("hi")
            #lock.wait_for(lambda: user_ticks == ticks)
        if user_ticks >= ticks:
            ticks = ticks + TICKS_PER_CYCLE
            #previous = time.time()
            if ticks % HZ == 0:
                current = time.time()
                print("tk %.20f" % (1- ( current - previous)))
                previous = current
                #start = time.time()
                #ticks = 0

            sleep = (ticks / HZ) - (time.time() - start)# - .00001
            if sleep > 0:
                time.sleep(sleep)
        else:
        #if ticks >= user_ticks:
            time.sleep((ticks - user_ticks) / HZ)
            #lock.notifyAll()

class SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

def monitor(frame, event, arg):
    global user_ticks
    frame.f_trace_opcodes = True
    #print(frame, event, arg)
    #print(frame.f_lasti, frame.f_lineno)
    #print(dir(frame))
    #print(frame.f_code)
    #print(frame.f_code.co_code)
    #print(dis.dis(frame.f_code.co_code))
    #print(list(dis.findlinestarts(frame.f_code.co_code)))
    #print(list(dis.get_instructions(frame.f_code, first_line=frame.f_lineno)))
    #print(frame.f_trace)
    #print(frame.f_trace_lines)
    #print(frame.f_trace_opcodes)
    #if event == "line":
    #    print('hello')
        # print(frame.f_globals)
        # print(frame.f_locals)

    # Don't do anything for system code; only do user code
    while True:
        if user_ticks < ticks:
            #with lock:
                #lock.wait()
                #lock.wait_for(lambda: user_ticks < ticks)

                if "self" in frame.f_locals:
                    return monitor

                if event == "opcode":
                    code = frame.f_code
                    offset = frame.f_lasti

                    #print(f"| {event:10} | {str(arg):>4} |", end=' ')
                    #print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
                    #print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")

                    #while monitor.ticks >= ticks:
                    #    #time.sleep(.00000001)
                    #    continue

                    user_ticks += 1

                return monitor
        else:
            time.sleep(1/HZ)

#monitor.ticks = 0

timekeeper_thread = threading.Thread(target=timekeeper)
timekeeper_thread.start()
#with lock:
#    lock.notifyAll()
with SetTrace(monitor):
   #print("hi")
   #print(foo())
   #print("cya!")

   exec(open(sys.argv[1]).read())

print("tickle", ticks, user_ticks)
run_timekeepr = False
timekeeper_thread.join()

#print("Bye")
#print("cya!")
