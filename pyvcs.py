from argparse import Namespace
import array
from collections.abc import Iterable
import ctypes
import dis
from enum import IntEnum
import opcode
from pathlib import Path
import sys
import time

import numpy as np
import sdl2
import sdl2.ext

from state import GLOBAL_STATE

import inspect

WIDTH = 128
HEIGHT = 72
RESOLUTION = (WIDTH, HEIGHT)
FRAME = [0] * (RESOLUTION[0] * RESOLUTION[1] * 1)
FRAME = array.array('B', FRAME)
HBLANK = 64 # RESOLUTION[0] + HBLANK % 3 == 0 because the display does 3 steps per user instruction
VBLANK = 32

MV = memoryview(FRAME).cast("B")
FRAME_PTR = ctypes.c_void_p(FRAME.buffer_info()[0])


sdl2.ext.init()
window = sdl2.ext.Window("window", size=RESOLUTION, flags=sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
renderer = sdl2.ext.Renderer(window, logical_size=RESOLUTION, flags=sdl2.SDL_RENDERER_ACCELERATED)
surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, *RESOLUTION, 8, sdl2.SDL_PIXELFORMAT_RGB332)
texture = sdl2.SDL_CreateTexture(renderer.renderer, sdl2.SDL_PIXELFORMAT_RGB332, sdl2.SDL_TEXTUREACCESS_STREAMING, *RESOLUTION)

window.show()


class SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

BACKGROUND_COLOR = 0

def background(color):
    global BACKGROUND_COLOR
    HELL_YEAH = True
    BACKGROUND_COLOR = color

set_background = background

class PlayfieldMode(IntEnum):
    DUPLICATE = 0
    REFLECT = 1

class Playfield:
    def __init__(self):
        ### Constants that shouldn't change. ###
        # TODO: Should they be stored as globals?

        # Each bit given by the user
        self.bit_width = 4

        # The width of the internal representation of the playfield
        self._internal_width = RESOLUTION[0] // 2

        # The width of the external representation of the playfield
        self.width = self._internal_width / self.bit_width

        ### User changable values ###

        # The color of the playfield and the balls
        self.color = 0

        # The bits that represent which parts of the playfield are turned on
        self.bits = bytes([0,0])

        # Whether to draw the playfield at all
        self.enabled = False

        # Whether to duplicate or reflect the playfield on the right side of the screen
        self.mode = PlayfieldMode.DUPLICATE

    @property
    def bits(self):
        """
        This defines which parts of the playfield are turned on.
        It's given by the user as 24 bits wide and then converted to 96 bits internally
        This represents half of the width of the resolution.
        The other half is either duplicated or mirrored from this.
        """
        return [self._bits[i*self.bit_width] for i in range(self.width)]

    @bits.setter
    def bits(self, value):
        """
        bits can either be given as 3 bytes, in which case the individual bits are used or
        it can be given as an iterable of length 24 in which each value is truthy
        (0/1 or True/False).
        """
        full_len = self.width
        short_len = int(self.width // 8)

        assert len(value) == full_len or len(value) == short_len

        # If given the compressed version, convert to the full one
        if len(value) == short_len:
            bits = []
            for i in range(short_len):
                bits += [(value[i] >> bit) & 1 for bit in range(7, -1, -1)]
        else:
            bits = value

        # Store as a full representation where each bit is repeated bit_width times
        self._bits = []
        for bit in bits:
            self._bits += [bit]*self.bit_width

        # Also store a reverse representation to make it easier to display the mirrored mode
        self._reverse = self._bits[::-1]

    def enable(self, enabled=True):
        self.enabled = enabled

    def disable(self):
        self.enabled = False

playfield = Playfield()
#def __getattr__
#GLOBAL_STATE["playfield"] = playfield

#PLAYFIELD_COLOR = playfield.color

#PLAYFIELD_COLOR = 0
BALLS = []
X = -HBLANK
Y = -VBLANK


def write_color_to_frame(color):
    i = Y*RESOLUTION[0] + X
    FRAME[i] = color

class Ball:
    def __init__(self, width):
        self.width = width
        self.enabled = False
        self.x = 0
        BALLS.append(self)

    def enable(self, x=None):
        if x is None:
            self.x = max(X, 0)
        else:
            self.x = x
        self.enabled = True

    def disable(self):
        self.enabled = False

HSYNC = False
WAIT_FOR_HSYNC = False

VSYNC = False
WAIT_FOR_VSYNC = False

def wait_for_hsync():
    USER_CODE = True
    global HSYNC, WAIT_FOR_HSYNC
    WAIT_FOR_HSYNC = True
    HSYNC = False
    while not HSYNC:
        continue
    WAIT_FOR_HSYNC = False

def wait_for_vsync():
    USER_CODE = True
    global VSYNC, WAIT_FOR_VSYNC
    WAIT_FOR_VSYNC = True
    VSYNC = False
    while Y != -1:
        continue
    WAIT_FOR_VSYNC = False


KEYS = {
    sdl2.SDLK_UP: False,
    sdl2.SDLK_DOWN: False,
    sdl2.SDLK_LEFT: False,
    sdl2.SDLK_RIGHT: False,
    sdl2.SDLK_ESCAPE: False,
    sdl2.SDLK_q: False
}



def get_key_state(keycode):
    return KEYS[keycode]

START = time.time()

def display_step():
    global X, Y, START, HSYNC, VSYNC

    #playfield = GLOBAL_STATE["playfield"]

    pixel = None

    if X < 0:
        X += 1
        return

    if Y < 0:
        X += 1
        if X == RESOLUTION[0]:
            HSYNC = True
            X = -HBLANK
            Y += 1
        return

    wrote_pixel = False
    for ball in BALLS:
        if ball.enabled and (X >= ball.x) and (X < (ball.x + ball.width)):
            pixel = playfield.color
            break

    if playfield.enabled:
        # Left half
        if X < playfield._internal_width:
            if playfield._bits[X]:
                pixel = playfield.color
        else:
            if playfield.mode == PlayfieldMode.DUPLICATE:
                if playfield._bits[X - playfield._internal_width]:
                    pixel = playfield.color
            elif playfield.mode == PlayfieldMode.REFLECT:
                if playfield._reverse[X - playfield._internal_width]:
                    pixel = playfield.color


    # TODO: Fun feature, turn off background filling for painting program
    if pixel is None:
        pixel = BACKGROUND_COLOR

    write_color_to_frame(pixel)

    X += 1
    if X == RESOLUTION[0]:
        HSYNC = True
        X = -HBLANK
        Y += 1
        if Y == RESOLUTION[1]:
            Y = -VBLANK

            sdl2.SDL_UpdateTexture(texture.contents, None,FRAME_PTR, RESOLUTION[0])
            renderer.copy(texture.contents)
            renderer.present()
            renderer.clear()
            window.refresh()

            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_KEYDOWN:
                    KEYS[event.key.keysym.sym] = True
                    #print(KEY)
                    #break
                elif event.type == sdl2.SDL_KEYUP:
                    KEYS[event.key.keysym.sym] = False
                    #break
                #print(event)

            sys.stdout.write('\r')
            sys.stdout.write("%.2f" % (1 / (time.time() - START)))#, str(KEY).zfill(8)))
            sys.stdout.flush()
            START = time.time()
            #VSYNC = True
            #HSYNC = True
            #print("HYS  ", HSYNC)

def monitor(frame, event, arg):
    #global HYSNC, WAIT_FOR_HSYNC
    #if not hasattr(monitor, 'api_reference'):
    #    monitor.api_reference = None

    if "USER_CODE" not in frame.f_globals and "USER_CODE" not in frame.f_locals:# and (not frame.f_back or "USER_CODE" not in frame.f_back.f_globals):
    #if "USER_CODE" not in frame.f_globals:
        frame.f_trace_opcodes = False
        frame.f_trace = None
        return monitor

    frame.f_trace_opcodes = True

    if event != "opcode":
        return monitor

    if (HSYNC and WAIT_FOR_HSYNC) or (VSYNC and WAIT_FOR_VSYNC):
       return monitor

    # print(dir(frame))
    # print(frame.f_code)
    # print(dir(frame.f_code))

    code = frame.f_code
    offset = frame.f_lasti
    opcode_name = opcode.opname[code.co_code[offset]]

    # print(f" {id(frame)} | {event:10} | {str(arg):>4} |", end=' ')
    # print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
    # print(f"{opcode.opname[code.co_code[offset]]:<18} | {code.co_code[offset+1]} |", end=' ')
    # print(dis.disassemble(code, lasti=offset))
    #print(code.co_stacksize)
    #print(dis.stack_effect(code.co_code[offset]))
    #print(frame.f_code.co_names)
    #print(inspect.getsource(code.co_code))
    #print(inspect.stack()[0])

    # if opcode_name == "LOAD_NAME":
    #     arg_name = frame.f_code.co_names[code.co_code[offset+1]]
    #     #print(dis.stack_effect(code.co_code[offset], code.co_code[offset+1]))
    #     if arg_name == "pyvcs":
    #         display_step()
    #         display_step()
    #         display_step()
    #         #frame.f_trace_opcodes = False
    #         frame.f_trace = None
    #         return monitor

    # Interacting with the API should take one op code
    # TODO: This is still really rough, there should be a more consistent way to figure out
    # if this interacts with the api
    if (event == "opcode") and opcode_name in ["LOAD_NAME", "LOAD_ATTR", "LOAD_METHOD", "CALL_METHOD"]:
        arg_name = frame.f_code.co_names[code.co_code[offset+1]]

        # if (opcode_name == "LOAD_NAME") and (
        #     arg_name == "pyvcs"
        # ):
        #     #frame.f_trace_opcodes = False
        #     return monitor
        #
        # if opcode_name in ["LOAD_METHOD", "LOAD_ATTR"]:
        #     if arg_name in globals():
        #         monitor.api_reference = globals()[arg_name]
        #         return monitor
        #     else:
        #         monitor.api_reference = None

        if opcode_name in ["LOAD_NAME", "LOAD_ATTR", "LOAD_GLOBAL"]:
            if arg_name == "pyvcs":
                monitor.api_reference = globals()
                return monitor
            elif hasattr(monitor.api_reference, arg_name):
                monitor.api_reference = getattr(monitor.api_reference, arg_name)
                return monitor
            elif isinstance(monitor.api_reference, Iterable) and arg_name in monitor.api_reference:
                monitor.api_reference = monitor.api_reference[arg_name]
                return monitor

            #elif opcode_name == "LOAD_METHOD":
            #    monitor.api_reference = None
        elif opcode_name == "LOAD_METHOD":
            if isinstance(monitor.api_reference, Iterable) and arg_name in monitor.api_reference:
                monitor.api_method_count += 1
                return monitor
            elif hasattr(monitor.api_reference, arg_name):
                monitor.api_method_count += 1
                return monitor
        elif opcode_name == "CALL_METHOD" and monitor.api_method_count > 0:
            monitor.api_method_count -= 1
            return monitor

        #monitor.api_reference = None


    # print(f" {id(frame)} | {event:10} | {str(arg):>4} |", end=' ')
    # print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
    # print(f"{opcode.opname[code.co_code[offset]]:<18} | {code.co_code[offset+1]} |", end=' ')
    # # #print(frame.f_code)
    # # #print(frame.f_code.co_consts)
    # print(frame.f_code.co_names)
    # print(frame.f_code.co_freevars)
    # #print(monitor.api_reference)
    # #print(inspect.stack())
    # print()

    if event == "opcode":
        # Do three system steps and then return
        #for i in range(3):
            #if (HSYNC and WAIT_FOR_HSYNC) or (VSYNC and WAIT_FOR_VSYNC):
            #    return monitor
        #    display_step()
        display_step()
        display_step()
        display_step()

    return monitor

monitor.api_reference = None
monitor.api_method_count = 0

def _resolve_name(name):
    parts = name.lower().split("_")
    parent = globals()

    for part in parts[:-1]:
        if hasattr(parent, part):
            parent = getattr(parent, part)
        elif isinstance(parent, Iterable) and part in parent:
            parent = parent[part]

    return parent, parts[-1]

class PYVCS:
    def __getattr__(self, name):
        #if hasattr(self, name):
        #    return getattr(self, name)
        parent, part = _resolve_name(name)

        if hasattr(parent, part):
            return getattr(parent, part)
        else:
            return parent[part]

    def __setattr__(self, name, value):
        parent, part = _resolve_name(name)

        if hasattr(parent, part):
            setattr(parent, part, value)
        else:
            parent[part] = value



def main():
    # Flush events
    for event in sdl2.ext.get_events():
        pass

    with SetTrace(monitor):
        exec(open(sys.argv[1]).read(), {
            "USER_CODE": True,
            "pyvcs":  Namespace(**globals()),
            #"pyvcs": PYVCS(),
            "__name__": ".".join(Path(sys.argv[1].replace(".py", "")).parts)
        })

    sdl2.SDL_DestroyTexture(texture)
    sdl2.SDL_DestroyRenderer(renderer.renderer)
    sdl2.SDL_DestroyWindow(window.window)
    sdl2.ext.quit()
    print(X,Y)
    #print(PLAYFIELD_COLOR, playfield.color)

if __name__ == '__main__':
    main()
