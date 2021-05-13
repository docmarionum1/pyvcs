import dis
import opcode
import sys
import threading
import time

HZ = 1190000
SECONDS_PER_TICK = 1 / HZ
TICKS_PER_CYCLE = 100

#target = start + 1
#previous = start
ticks = 0
current_ticks = 0
user_ticks = 0

run_timekeepr = True

lock = threading.Lock()
#lock = threading.Condition()

start = time.time()
previous = start

# def timekeeper():
#     start = time.time()
#     previous = start
#
#     global ticks
#     while run_timekeepr:
#         #with lock:
#             #print("hi")
#             #lock.wait_for(lambda: user_ticks == ticks)
#         if user_ticks >= ticks:
#             ticks = ticks + TICKS_PER_CYCLE
#             #previous = time.time()
#             if ticks % HZ == 0:
#                 current = time.time()
#                 print("tk %.20f" % (1- ( current - previous)))
#                 previous = current
#                 #start = time.time()
#                 #ticks = 0
#
#             sleep = (ticks / HZ) - (time.time() - start)# - .00001
#             if sleep > 0:
#                 time.sleep(sleep)
#         else:
#         #if ticks >= user_ticks:
#             time.sleep((ticks - user_ticks) / HZ)
#             #lock.notifyAll()

class SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

num_sleeps = 0
delta_ticks_total = 0

def monitor(frame, event, arg):
    if "USER_CODE" not in frame.f_globals and (not frame.f_back or "USER_CODE" not in frame.f_back.f_globals):
        frame.f_trace_opcodes = False
        return monitor

    #if "USER_CODE" not in frame.f_globals:
    #    frame.f_globals["USER_CODE"] = True

    # if frame.f_globals.get("__name__").startswith("_"):
    #     return monitor
    # if "__name__" in frame.f_globals and frame.f_globals["__name__"] == "__main__":
    #     print("boop")
    #     frame.f_trace_opcodes = False
    #     return monitor

    code = frame.f_code
    offset = frame.f_lasti

    #print(f"| {event:10} | {str(arg):>4} |", end=' ')
    #print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
    #print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
    #print(frame.f_globals)



    global user_ticks
    global ticks
    global previous
    global current_ticks
    global num_sleeps
    global delta_ticks_total
    frame.f_trace_opcodes = True




    if event == "opcode":
        # print(event, frame.f_globals.keys())
        # print(frame.f_locals.keys())
        # print(frame.f_globals["__name__"])
        # print(frame.f_globals["__package__"])
        # print(frame.f_globals["__cached__"])




        # try:
        #     print(event, frame.f_locals)
        # except:
        #     pass
        # if "self" in frame.f_locals:
        #     return monitor

        #a = 1
        #b = 1 + a
        #c = a * b
        #ticks += 1
        current_ticks += 1
        ticks += 1

        if current_ticks % TICKS_PER_CYCLE == 0:
            current = time.time()
            #ticks += TICKS_PER_CYCLE
            #code = frame.f_code
            #offset = frame.f_lasti

            if current_ticks > HZ:
                print("tk %.20f" % (1- ( current - previous)))
                previous = current
                #ticks += current_ticks
                current_ticks = current_ticks % HZ

                #start = time.time()
                #ticks = 0

            sleep = (ticks / HZ) - (current - start)# - .00001
            if sleep > 0:
                num_sleeps += 1
                time.sleep(sleep)
            # else:
            #    delta_ticks = int(abs(sleep) * HZ / TICKS_PER_CYCLE) * TICKS_PER_CYCLE
            #    delta_ticks_total += delta_ticks
            #    current_ticks += delta_ticks
            #    ticks += delta_ticks

        #user_ticks += 1

    return monitor



#monitor.ticks = 0

#timekeeper_thread = threading.Thread(target=timekeeper)
#imekeeper_thread.start()
#with lock:
#    lock.notifyAll()
def main():
    with SetTrace(monitor):
       #print("hi")
       #print(foo())
       #print("cya!")
       USER_CODE = True
       exec(open(sys.argv[1]).read(), {"USER_CODE": True})

    print("ticks", ticks)
    print("num_sleeps", num_sleeps)
    print("delta_ticks_total", delta_ticks_total)
    print("user_ticks", ticks - delta_ticks_total)
#run_timekeepr = False
#timekeeper_thread.join()

#print("Bye")
#print("cya!")

if __name__ == '__main__':
    main()
